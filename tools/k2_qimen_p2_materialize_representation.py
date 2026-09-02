#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
COMPONENT_FIELDS = (
    "world_variable_manifest",
    "symbol_vocabulary",
    "feature_extraction_manifest",
    "eligible_rule_pool",
    "prediction_schema",
)
SOURCE_FIELDS = ("representation_id",) + COMPONENT_FIELDS
MATERIALIZED_FIELDS = {
    "artifact_kind",
    "representation_id",
    "canonical_serialization",
    "hash_algorithm",
    "shared_manifests",
    "shared_manifest_hashes",
    "shared_representation_sha256",
    "lane_bindings",
    "representation_parity",
}
PARITY_CONTRACT = {
    "world_variable_manifest_shared": True,
    "lane_specific_world_variable_addition_forbidden": True,
    "symbol_vocabulary_shared": True,
    "feature_extraction_manifest_shared": True,
    "eligible_rule_pool_shared": True,
    "prediction_schema_shared": True,
    "lane_specific_representation_addition_forbidden": True,
}
SHA64_RE = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def canonical_bytes(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_source(source):
    require(isinstance(source, dict), "representation source must be object")
    require(set(source) == set(SOURCE_FIELDS), "representation source fields drift")
    representation_id = source.get("representation_id")
    require(
        isinstance(representation_id, str) and representation_id.strip(),
        "representation_id missing",
    )
    for field in COMPONENT_FIELDS:
        component = source.get(field)
        require(isinstance(component, dict) and component, f"{field} must be non-empty object")


def materialize_representation(source):
    validate_source(source)
    shared_manifests = {
        field: copy.deepcopy(source[field]) for field in COMPONENT_FIELDS
    }
    shared_manifest_hashes = {
        field: canonical_sha256(shared_manifests[field]) for field in COMPONENT_FIELDS
    }
    shared_representation_sha256 = canonical_sha256(
        {
            "representation_id": source["representation_id"],
            "shared_manifest_hashes": shared_manifest_hashes,
        }
    )
    lane_bindings = [
        {
            "lane_id": lane_id,
            "shared_manifest_hashes": copy.deepcopy(shared_manifest_hashes),
            "shared_representation_sha256": shared_representation_sha256,
        }
        for lane_id in LANE_IDS
    ]
    result = {
        "artifact_kind": "P2_SHARED_REPRESENTATION_MANIFEST",
        "representation_id": source["representation_id"],
        "canonical_serialization": "UTF8_JSON_SORT_KEYS_COMPACT",
        "hash_algorithm": "SHA256",
        "shared_manifests": shared_manifests,
        "shared_manifest_hashes": shared_manifest_hashes,
        "shared_representation_sha256": shared_representation_sha256,
        "lane_bindings": lane_bindings,
        "representation_parity": copy.deepcopy(PARITY_CONTRACT),
    }
    validate_materialized(result)
    return result


def validate_materialized(value):
    require(isinstance(value, dict), "materialized representation must be object")
    require(set(value) == MATERIALIZED_FIELDS, "materialized representation fields drift")
    require(
        value.get("artifact_kind") == "P2_SHARED_REPRESENTATION_MANIFEST",
        "artifact_kind drift",
    )
    representation_id = value.get("representation_id")
    require(
        isinstance(representation_id, str) and representation_id.strip(),
        "materialized representation_id missing",
    )
    require(
        value.get("canonical_serialization") == "UTF8_JSON_SORT_KEYS_COMPACT",
        "canonical serialization drift",
    )
    require(value.get("hash_algorithm") == "SHA256", "hash algorithm drift")

    shared_manifests = value.get("shared_manifests")
    require(
        isinstance(shared_manifests, dict)
        and set(shared_manifests) == set(COMPONENT_FIELDS),
        "shared manifest set drift",
    )
    for field in COMPONENT_FIELDS:
        require(
            isinstance(shared_manifests[field], dict) and shared_manifests[field],
            f"materialized {field} must be non-empty object",
        )

    shared_manifest_hashes = value.get("shared_manifest_hashes")
    require(
        isinstance(shared_manifest_hashes, dict)
        and set(shared_manifest_hashes) == set(COMPONENT_FIELDS),
        "shared manifest hash set drift",
    )
    expected_hashes = {
        field: canonical_sha256(shared_manifests[field]) for field in COMPONENT_FIELDS
    }
    require(
        shared_manifest_hashes == expected_hashes,
        "shared manifest content/hash binding drift",
    )
    require(
        all(isinstance(x, str) and SHA64_RE.match(x) for x in shared_manifest_hashes.values()),
        "shared manifest hash format invalid",
    )

    expected_representation_hash = canonical_sha256(
        {
            "representation_id": representation_id,
            "shared_manifest_hashes": expected_hashes,
        }
    )
    require(
        value.get("shared_representation_sha256") == expected_representation_hash,
        "shared representation hash drift",
    )

    lane_bindings = value.get("lane_bindings")
    require(
        isinstance(lane_bindings, list) and len(lane_bindings) == len(LANE_IDS),
        "lane binding cardinality drift",
    )
    require(
        [row.get("lane_id") for row in lane_bindings] == list(LANE_IDS),
        "lane binding identity/order drift",
    )
    for row in lane_bindings:
        require(
            isinstance(row, dict)
            and set(row)
            == {
                "lane_id",
                "shared_manifest_hashes",
                "shared_representation_sha256",
            },
            "lane binding fields drift",
        )
        require(
            row.get("shared_manifest_hashes") == expected_hashes,
            f"lane representation hash parity drift: {row.get('lane_id')}",
        )
        require(
            row.get("shared_representation_sha256") == expected_representation_hash,
            f"lane representation identity drift: {row.get('lane_id')}",
        )

    require(
        value.get("representation_parity") == PARITY_CONTRACT,
        "representation parity contract drift",
    )


def load_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Materialize one shared P2 representation manifest for all lanes."
    )
    parser.add_argument("--input", required=True, help="Source JSON path")
    parser.add_argument("--output", help="Output JSON path; omit with --check-only")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    if not args.check_only and not args.output:
        parser.error("--output is required unless --check-only is used")

    try:
        source = load_json(args.input)
        result = materialize_representation(source)
        if args.output:
            Path(args.output).write_bytes(canonical_bytes(result) + b"\n")
    except ValidationError as exc:
        print(f"k2-qimen-p2-materialize-representation: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "k2-qimen-p2-materialize-representation: PASS "
        f"lanes={len(LANE_IDS)} shared_components={len(COMPONENT_FIELDS)} "
        f"representation_sha256={result['shared_representation_sha256']}"
    )


if __name__ == "__main__":
    main()
