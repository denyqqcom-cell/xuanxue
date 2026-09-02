#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
ATOMIC_CONTEXT_LAYERS = ("奇仪", "八门", "八神", "九星", "九宫")
DERIVED_COMPOSITES = ("格局",)
COMPONENT_FIELDS = (
    "world_variable_manifest",
    "symbol_vocabulary",
    "feature_extraction_manifest",
    "eligible_rule_pool",
    "prediction_schema",
    "priority_policy_schema",
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
    "shared_atomic_context_universe",
    "derived_composites",
    "lane_bindings",
    "representation_parity",
}
PRIORITY_POLICY_FORMS = (
    "FIXED_RANKED_SUBSET_WITH_VISIBLE_UNRANKED_CONTEXT",
    "QUESTION_DOMAIN_CONDITIONED_PARTIAL_PRIORITY_OR_PRIMARY_LAYER",
)
PARITY_CONTRACT = {
    "same_feature_universe_all_lanes": True,
    "lane_specific_feature_vocabulary_forbidden": True,
    "atomic_context_layer_add_or_drop_forbidden": True,
    "derived_composite_promoted_to_atomic_layer_forbidden": True,
    "priority_policy_schema_shared": True,
    "lane_specific_rule_pool_addition_forbidden": True,
    "shared_representation_digest_all_lanes": True,
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


def validate_symbol_vocabulary(value):
    require(isinstance(value, dict), "symbol_vocabulary must be object")
    require(
        set(value) == {"atomic_context_layers", "derived_composites", "visibility"},
        "symbol_vocabulary fields drift",
    )
    require(
        value.get("atomic_context_layers") == list(ATOMIC_CONTEXT_LAYERS),
        "shared atomic context universe drift",
    )
    require(
        value.get("derived_composites") == list(DERIVED_COMPOSITES),
        "derived composite set drift",
    )
    require(value.get("visibility") == "ALL_LANES", "feature visibility must be ALL_LANES")
    require("九宫" in value["atomic_context_layers"], "九宫 must remain first-class atomic context")
    require("格局" not in value["atomic_context_layers"], "格局 cannot be atomic context layer")


def validate_priority_policy_schema(value):
    require(isinstance(value, dict), "priority_policy_schema must be object")
    require(
        set(value)
        == {
            "policy_forms",
            "ranked_subset_may_be_partial",
            "visible_unranked_context_required_when_not_ranked",
            "unsupported_total_order_action",
            "plate_value_selected_priority_forbidden",
            "outcome_or_feedback_selected_priority_forbidden",
        },
        "priority_policy_schema fields drift",
    )
    require(value.get("policy_forms") == list(PRIORITY_POLICY_FORMS), "priority policy forms drift")
    require(value.get("ranked_subset_may_be_partial") is True, "partial ranked subsets must be allowed")
    require(
        value.get("visible_unranked_context_required_when_not_ranked") is True,
        "unranked context visibility must be explicit",
    )
    require(
        value.get("unsupported_total_order_action") == "ABSTAIN_FAIL_CLOSED",
        "unsupported total order must abstain fail-closed",
    )
    require(
        value.get("plate_value_selected_priority_forbidden") is True,
        "plate values cannot select priority policy",
    )
    require(
        value.get("outcome_or_feedback_selected_priority_forbidden") is True,
        "outcome/feedback cannot select priority policy",
    )


def validate_source(source):
    require(isinstance(source, dict), "V02 representation source must be object")
    require(set(source) == set(SOURCE_FIELDS), "V02 representation source fields drift")
    representation_id = source.get("representation_id")
    require(isinstance(representation_id, str) and representation_id.strip(), "representation_id missing")
    for field in COMPONENT_FIELDS:
        require(isinstance(source.get(field), dict) and source[field], f"{field} must be non-empty object")
    validate_symbol_vocabulary(source["symbol_vocabulary"])
    validate_priority_policy_schema(source["priority_policy_schema"])
    require(
        source["eligible_rule_pool"].get("lane_specific_additions") is False,
        "lane-specific eligible rule additions forbidden",
    )
    require(
        source["feature_extraction_manifest"].get("depth") == "SHARED",
        "feature extraction depth must remain shared",
    )
    require(
        source["feature_extraction_manifest"].get("derived_composite_source") == "SHARED_INPUTS_ONLY",
        "derived composites must use shared inputs only",
    )


def materialize_representation_v02(source):
    validate_source(source)
    shared_manifests = {field: copy.deepcopy(source[field]) for field in COMPONENT_FIELDS}
    shared_manifest_hashes = {
        field: canonical_sha256(shared_manifests[field]) for field in COMPONENT_FIELDS
    }
    shared_representation_sha256 = canonical_sha256(
        {
            "representation_id": source["representation_id"],
            "shared_manifest_hashes": shared_manifest_hashes,
            "shared_atomic_context_universe": list(ATOMIC_CONTEXT_LAYERS),
            "derived_composites": list(DERIVED_COMPOSITES),
        }
    )
    lane_bindings = [
        {
            "lane_id": lane_id,
            "shared_manifest_hashes": copy.deepcopy(shared_manifest_hashes),
            "shared_representation_sha256": shared_representation_sha256,
            "shared_atomic_context_universe": list(ATOMIC_CONTEXT_LAYERS),
            "derived_composites": list(DERIVED_COMPOSITES),
        }
        for lane_id in LANE_IDS
    ]
    result = {
        "artifact_kind": "P2_SHARED_SUPERSET_REPRESENTATION_MANIFEST_V02",
        "representation_id": source["representation_id"],
        "canonical_serialization": "UTF8_JSON_SORT_KEYS_COMPACT",
        "hash_algorithm": "SHA256",
        "shared_manifests": shared_manifests,
        "shared_manifest_hashes": shared_manifest_hashes,
        "shared_representation_sha256": shared_representation_sha256,
        "shared_atomic_context_universe": list(ATOMIC_CONTEXT_LAYERS),
        "derived_composites": list(DERIVED_COMPOSITES),
        "lane_bindings": lane_bindings,
        "representation_parity": copy.deepcopy(PARITY_CONTRACT),
    }
    validate_materialized_v02(result)
    return result


def validate_materialized_v02(value):
    require(isinstance(value, dict), "materialized V02 representation must be object")
    require(set(value) == MATERIALIZED_FIELDS, "materialized V02 fields drift")
    require(
        value.get("artifact_kind") == "P2_SHARED_SUPERSET_REPRESENTATION_MANIFEST_V02",
        "artifact_kind drift",
    )
    representation_id = value.get("representation_id")
    require(isinstance(representation_id, str) and representation_id.strip(), "representation_id missing")
    require(value.get("canonical_serialization") == "UTF8_JSON_SORT_KEYS_COMPACT", "canonical serialization drift")
    require(value.get("hash_algorithm") == "SHA256", "hash algorithm drift")
    require(value.get("shared_atomic_context_universe") == list(ATOMIC_CONTEXT_LAYERS), "materialized atomic universe drift")
    require(value.get("derived_composites") == list(DERIVED_COMPOSITES), "materialized composite set drift")

    shared_manifests = value.get("shared_manifests")
    require(isinstance(shared_manifests, dict) and set(shared_manifests) == set(COMPONENT_FIELDS), "shared manifest set drift")
    for field in COMPONENT_FIELDS:
        require(isinstance(shared_manifests[field], dict) and shared_manifests[field], f"materialized {field} invalid")
    validate_symbol_vocabulary(shared_manifests["symbol_vocabulary"])
    validate_priority_policy_schema(shared_manifests["priority_policy_schema"])
    require(shared_manifests["eligible_rule_pool"].get("lane_specific_additions") is False, "materialized lane rule additions forbidden")

    expected_hashes = {field: canonical_sha256(shared_manifests[field]) for field in COMPONENT_FIELDS}
    shared_manifest_hashes = value.get("shared_manifest_hashes")
    require(shared_manifest_hashes == expected_hashes, "shared manifest content/hash binding drift")
    require(all(isinstance(x, str) and SHA64_RE.match(x) for x in shared_manifest_hashes.values()), "shared manifest hash format invalid")

    expected_representation_hash = canonical_sha256(
        {
            "representation_id": representation_id,
            "shared_manifest_hashes": expected_hashes,
            "shared_atomic_context_universe": list(ATOMIC_CONTEXT_LAYERS),
            "derived_composites": list(DERIVED_COMPOSITES),
        }
    )
    require(value.get("shared_representation_sha256") == expected_representation_hash, "shared V02 representation hash drift")

    lane_bindings = value.get("lane_bindings")
    require(isinstance(lane_bindings, list) and len(lane_bindings) == len(LANE_IDS), "lane binding cardinality drift")
    require([row.get("lane_id") for row in lane_bindings] == list(LANE_IDS), "lane binding identity/order drift")
    expected_lane_fields = {
        "lane_id",
        "shared_manifest_hashes",
        "shared_representation_sha256",
        "shared_atomic_context_universe",
        "derived_composites",
    }
    for row in lane_bindings:
        require(isinstance(row, dict) and set(row) == expected_lane_fields, "lane binding fields drift")
        require(row.get("shared_manifest_hashes") == expected_hashes, f"lane manifest parity drift: {row.get('lane_id')}")
        require(row.get("shared_representation_sha256") == expected_representation_hash, f"lane representation digest drift: {row.get('lane_id')}")
        require(row.get("shared_atomic_context_universe") == list(ATOMIC_CONTEXT_LAYERS), f"lane atomic universe drift: {row.get('lane_id')}")
        require(row.get("derived_composites") == list(DERIVED_COMPOSITES), f"lane composite drift: {row.get('lane_id')}")

    require(value.get("representation_parity") == PARITY_CONTRACT, "representation parity contract drift")


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description="Materialize shared-superset P2 Representation V02 contract fixtures.")
    parser.add_argument("--input", required=True, help="Source JSON path")
    parser.add_argument("--output", help="Output JSON path; omit with --check-only")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only and not args.output:
        parser.error("--output is required unless --check-only is used")
    try:
        source = load_json(args.input)
        result = materialize_representation_v02(source)
        if args.output:
            Path(args.output).write_bytes(canonical_bytes(result) + b"\n")
    except ValidationError as exc:
        print(f"k2-qimen-p2-materialize-representation-v02: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "k2-qimen-p2-materialize-representation-v02: PASS "
        f"lanes={len(LANE_IDS)} shared_components={len(COMPONENT_FIELDS)} atomic_layers={len(ATOMIC_CONTEXT_LAYERS)} "
        f"derived_composites={len(DERIVED_COMPOSITES)} representation_sha256={result['shared_representation_sha256']}"
    )


if __name__ == "__main__":
    main()
