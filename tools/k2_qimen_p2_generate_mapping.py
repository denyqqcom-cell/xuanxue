#!/usr/bin/env python3
import copy
import hashlib
import json

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
FIXED_GLOBAL_PRIORITY = ("奇仪", "八门", "八神", "九星")
MODEL_BY_LANE = {
    "P2-A": "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01",
    "P2-A_PRIME": "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01",
    "P2-B": "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01",
}
ROLE_POLICY_BY_LANE = {
    "P2-A": "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY",
    "P2-A_PRIME": "QUESTION_TOPOLOGY_CONDITIONED",
    "P2-B": "QUESTION_TOPOLOGY_CONDITIONED",
}
LAYER_POLICY_BY_LANE = {
    "P2-A": "FIXED_GLOBAL",
    "P2-A_PRIME": "FIXED_GLOBAL",
    "P2-B": "QUESTION_TOPOLOGY_CONDITIONED",
}

PRE_PLATE_FIELDS = {
    "question_definition",
    "question_domain",
    "asked_object",
    "scenario_graph",
    "object_graph",
    "method_layer",
    "source_role_catalog",
    "topology_role_candidates",
    "topology_layer_priority",
    "correction_registry",
    "competing_mappings",
}
FORBIDDEN_PRE_PLATE_FIELDS = {
    "current_plate_symbol_values",
    "current_plate_strength_or_auspiciousness",
    "prediction",
    "outcome",
    "feedback",
    "lane_peer_intermediate_output",
    "unregistered_external_omen",
}
ROLE_FIELDS = {
    "role_id",
    "question_domain",
    "asked_object",
    "method_layer",
    "symbol_instance_selector",
    "source_refs",
    "source_scope",
}
SYMBOL_INSTANCE_FIELDS = {
    "symbol_type",
    "plate_layer",
    "instance_role",
    "relation_direction",
}
CORRECTION_FIELDS = {
    "correction_id",
    "trigger",
    "action",
    "source_refs",
    "source_scope",
}
COMPETING_MAPPING_FIELDS = {"mapping_id", "source_refs"}
TOPOLOGY_PRIORITY_FIELDS = {
    "priority",
    "source_refs",
    "source_scope",
    "fixture_synthetic_order",
}
GLOBAL_SCOPE_TOKENS = {"GLOBAL", "UNIVERSAL", "ALL_DOMAINS", "*"}


class GeneratorError(RuntimeError):
    pass


class MappingBoundaryError(GeneratorError):
    pass


class SourceLocalityError(GeneratorError):
    pass


class ContaminationError(GeneratorError):
    pass


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require(condition, message, exc_type=MappingBoundaryError):
    if not condition:
        raise exc_type(message)


def _require_nonempty_string(value, label):
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be non-empty string")


def _validate_source_refs(value, label):
    _require(isinstance(value, list) and value, f"{label} must be non-empty list")
    for idx, ref in enumerate(value):
        _require_nonempty_string(ref, f"{label}[{idx}]")


def _validate_source_scope(scope, expected_domain, label):
    _require_nonempty_string(scope, label)
    if scope.upper() in GLOBAL_SCOPE_TOKENS:
        raise SourceLocalityError(f"{label} may not globalize source-local material")
    _require(
        scope == expected_domain,
        f"{label} must stay within frozen question_domain {expected_domain!r}",
        SourceLocalityError,
    )


def _validate_symbol_instance(value, label):
    _require(isinstance(value, dict), f"{label} must be object")
    _require(set(value) == SYMBOL_INSTANCE_FIELDS, f"{label} fields drift")
    for key in sorted(SYMBOL_INSTANCE_FIELDS):
        _require_nonempty_string(value.get(key), f"{label}.{key}")


def _validate_role(role, question_domain, asked_object, method_layer, label):
    _require(isinstance(role, dict), f"{label} must be object")
    _require(set(role) == ROLE_FIELDS, f"{label} fields drift")
    _require_nonempty_string(role.get("role_id"), f"{label}.role_id")
    _require(
        role.get("question_domain") == question_domain,
        f"{label}.question_domain must match frozen input",
        SourceLocalityError,
    )
    _require(
        role.get("asked_object") == asked_object,
        f"{label}.asked_object must match frozen input",
        SourceLocalityError,
    )
    _require(
        role.get("method_layer") == method_layer,
        f"{label}.method_layer must match frozen input",
        SourceLocalityError,
    )
    _validate_symbol_instance(role.get("symbol_instance_selector"), f"{label}.symbol_instance_selector")
    _validate_source_refs(role.get("source_refs"), f"{label}.source_refs")
    _validate_source_scope(role.get("source_scope"), question_domain, f"{label}.source_scope")


def _validate_role_list(rows, question_domain, asked_object, method_layer, label):
    _require(isinstance(rows, list) and rows, f"{label} must be non-empty list")
    ids = []
    for idx, row in enumerate(rows):
        _validate_role(row, question_domain, asked_object, method_layer, f"{label}[{idx}]")
        ids.append(row["role_id"])
    _require(len(ids) == len(set(ids)), f"{label} contains duplicate role_id")


def _validate_corrections(rows, question_domain):
    _require(isinstance(rows, list), "correction_registry must be list")
    ids = []
    for idx, row in enumerate(rows):
        label = f"correction_registry[{idx}]"
        _require(isinstance(row, dict), f"{label} must be object")
        _require(set(row) == CORRECTION_FIELDS, f"{label} fields drift")
        for key in ("correction_id", "trigger", "action"):
            _require_nonempty_string(row.get(key), f"{label}.{key}")
        _validate_source_refs(row.get("source_refs"), f"{label}.source_refs")
        _validate_source_scope(row.get("source_scope"), question_domain, f"{label}.source_scope")
        ids.append(row["correction_id"])
    _require(len(ids) == len(set(ids)), "correction_registry contains duplicate correction_id")


def _validate_competing_mappings(rows):
    _require(isinstance(rows, list), "competing_mappings must be list")
    ids = []
    for idx, row in enumerate(rows):
        label = f"competing_mappings[{idx}]"
        _require(isinstance(row, dict), f"{label} must be object")
        _require(set(row) == COMPETING_MAPPING_FIELDS, f"{label} fields drift")
        _require_nonempty_string(row.get("mapping_id"), f"{label}.mapping_id")
        _validate_source_refs(row.get("source_refs"), f"{label}.source_refs")
        ids.append(row["mapping_id"])
    _require(len(ids) == len(set(ids)), "competing_mappings contains duplicate mapping_id")


def _validate_topology_priority(value, question_domain):
    _require(isinstance(value, dict), "topology_layer_priority must be object")
    _require(set(value) == TOPOLOGY_PRIORITY_FIELDS, "topology_layer_priority fields drift")
    priority = value.get("priority")
    _require(
        isinstance(priority, list)
        and len(priority) == len(FIXED_GLOBAL_PRIORITY)
        and set(priority) == set(FIXED_GLOBAL_PRIORITY),
        "topology layer priority must rank all and only the shared four layers",
    )
    _validate_source_refs(value.get("source_refs"), "topology_layer_priority.source_refs")
    _validate_source_scope(
        value.get("source_scope"), question_domain, "topology_layer_priority.source_scope"
    )
    _require(
        isinstance(value.get("fixture_synthetic_order"), bool),
        "topology_layer_priority.fixture_synthetic_order must be boolean",
    )


def validate_pre_plate_input(value):
    _require(isinstance(value, dict), "pre-plate input must be object")
    forbidden = set(value) & FORBIDDEN_PRE_PLATE_FIELDS
    _require(not forbidden, f"forbidden pre-plate fields present: {sorted(forbidden)}")
    _require(set(value) == PRE_PLATE_FIELDS, "pre-plate input fields drift")

    _require_nonempty_string(value.get("question_definition"), "question_definition")
    _require_nonempty_string(value.get("question_domain"), "question_domain")
    _require_nonempty_string(value.get("asked_object"), "asked_object")
    _require_nonempty_string(value.get("method_layer"), "method_layer")
    _require(isinstance(value.get("scenario_graph"), dict), "scenario_graph must be object")
    _require(isinstance(value.get("object_graph"), dict), "object_graph must be object")

    question_domain = value["question_domain"]
    asked_object = value["asked_object"]
    method_layer = value["method_layer"]
    _validate_role_list(
        value["source_role_catalog"],
        question_domain,
        asked_object,
        method_layer,
        "source_role_catalog",
    )
    _validate_role_list(
        value["topology_role_candidates"],
        question_domain,
        asked_object,
        method_layer,
        "topology_role_candidates",
    )
    catalog_role_ids = {row["role_id"] for row in value["source_role_catalog"]}
    topology_role_ids = {row["role_id"] for row in value["topology_role_candidates"]}
    _require(
        topology_role_ids == catalog_role_ids,
        "topology-conditioned mapping may rebind but may not add/drop roles outside the shared source catalog",
        SourceLocalityError,
    )
    _validate_topology_priority(value["topology_layer_priority"], question_domain)
    _validate_corrections(value["correction_registry"], question_domain)
    _validate_competing_mappings(value["competing_mappings"])
    return True


def _sorted_copy(rows, key):
    return sorted(copy.deepcopy(rows), key=lambda row: row[key])


def _materialize_lane(pre_plate_input, lane_id, input_hash):
    if lane_id == "P2-A":
        roles = _sorted_copy(pre_plate_input["source_role_catalog"], "role_id")
        priority = list(FIXED_GLOBAL_PRIORITY)
    elif lane_id == "P2-A_PRIME":
        roles = _sorted_copy(pre_plate_input["topology_role_candidates"], "role_id")
        priority = list(FIXED_GLOBAL_PRIORITY)
    elif lane_id == "P2-B":
        roles = _sorted_copy(pre_plate_input["topology_role_candidates"], "role_id")
        priority = list(pre_plate_input["topology_layer_priority"]["priority"])
    else:
        raise MappingBoundaryError(f"unknown lane {lane_id}")

    row = {
        "artifact_kind": "P2_ROLE_LAYER_MAPPING",
        "lane_id": lane_id,
        "model_name": MODEL_BY_LANE[lane_id],
        "role_binding_policy": ROLE_POLICY_BY_LANE[lane_id],
        "layer_priority_policy": LAYER_POLICY_BY_LANE[lane_id],
        "layer_priority": priority,
        "mapping_input_sha256": input_hash,
        "roles": roles,
        "correction_registry": _sorted_copy(pre_plate_input["correction_registry"], "correction_id"),
        "competing_mappings": _sorted_copy(pre_plate_input["competing_mappings"], "mapping_id"),
        "outcome_data_used": False,
    }
    row["mapping_sha256"] = canonical_sha256(row)
    return row


def generate_all_lane_mappings(pre_plate_input):
    validate_pre_plate_input(pre_plate_input)
    frozen_input = copy.deepcopy(pre_plate_input)
    input_hash = canonical_sha256(frozen_input)
    generated = {
        lane_id: _materialize_lane(frozen_input, lane_id, input_hash)
        for lane_id in LANE_IDS
    }

    _require(
        generated["P2-A"]["layer_priority"] == list(FIXED_GLOBAL_PRIORITY),
        "P2-A fixed global priority drift",
    )
    _require(
        generated["P2-A_PRIME"]["layer_priority"] == list(FIXED_GLOBAL_PRIORITY),
        "P2-A_PRIME fixed global priority drift",
    )
    _require(
        generated["P2-A_PRIME"]["roles"] == generated["P2-B"]["roles"],
        "P2-C2 role binding must remain identical",
    )
    for key in (
        "mapping_input_sha256",
        "roles",
        "correction_registry",
        "competing_mappings",
        "role_binding_policy",
    ):
        _require(
            generated["P2-A_PRIME"][key] == generated["P2-B"][key],
            f"P2-C2 drift outside layer priority: {key}",
        )
    return generated


class RoleLayerSession:
    def __init__(self, pre_plate_input):
        self._pre_plate_input = copy.deepcopy(pre_plate_input)
        validate_pre_plate_input(self._pre_plate_input)
        self._mappings = None
        self._mapping_frozen = False
        self._plate_values_read = False
        self._feedback_read = False
        self.contamination_ledger = []

    @property
    def mappings(self):
        return copy.deepcopy(self._mappings)

    def _record_contamination(self, kind, detail):
        row = {"kind": kind, "detail": detail}
        self.contamination_ledger.append(row)
        raise ContaminationError(f"{kind}: {detail}")

    def freeze_mappings(self):
        _require(not self._plate_values_read, "cannot freeze mappings after plate values")
        _require(not self._feedback_read, "cannot freeze mappings after feedback")
        self._mappings = generate_all_lane_mappings(self._pre_plate_input)
        self._mapping_frozen = True
        return self.mappings

    def read_plate_values(self, current_plate_symbol_values):
        _require(self._mapping_frozen, "Role/Layer mapping must freeze before plate-value access")
        _require(isinstance(current_plate_symbol_values, dict), "current_plate_symbol_values must be object")
        self._plate_values_read = True
        return copy.deepcopy(current_plate_symbol_values)

    def read_feedback(self, feedback):
        _require(self._mapping_frozen, "feedback cannot be read before mapping freeze")
        _require(self._plate_values_read, "feedback cannot be read before plate-value phase")
        self._feedback_read = True
        return copy.deepcopy(feedback)

    def attempt_role_map_edit(self, detail):
        if self._mapping_frozen or self._plate_values_read or self._feedback_read:
            self._record_contamination("LATE_ROLE_MAP_EDIT", str(detail))
        raise MappingBoundaryError("role-map edits belong to pre-freeze input construction only")

    def attempt_role_switch(self, role_id):
        if self._feedback_read:
            self._record_contamination("POST_FEEDBACK_ROLE_SWITCH", str(role_id))
        raise MappingBoundaryError("role switch is not allowed outside frozen mapping")

    def attempt_correction_registry_edit(self, change):
        if self._feedback_read:
            self._record_contamination("POST_FEEDBACK_CORRECTION_EDIT", canonical_json(change))
        raise MappingBoundaryError("correction registry edits are not allowed after freeze")

    def select_unfrozen_competing_mapping(self, mapping_id, selection_basis):
        basis = str(selection_basis).upper()
        if (not self._mapping_frozen) and any(
            token in basis for token in ("OUTCOME", "HIT", "FEEDBACK", "RESULT")
        ):
            self._record_contamination(
                "UNFROZEN_COMPETING_MAPPING_OUTCOME_SELECTION",
                f"{mapping_id}:{selection_basis}",
            )
        raise MappingBoundaryError(
            "competing mappings must be preserved/frozen or abstained before outcome access"
        )
