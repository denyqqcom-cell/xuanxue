#!/usr/bin/env python3
import copy

from validate_k2_qimen_p2_execution_contract import (
    AUDIT_PATH,
    BATCHES_PATH,
    CONTRACT_PATH,
    FIXTURE_PATH,
    FREEZE_SCHEMA_PATH,
    FREEZES_PATH,
    GEN_SCHEMA_PATH,
    IMPL_PATH,
    PLANS_PATH,
    ROOT,
    V04_PATH,
    V05_PATH,
    ValidationError,
    load_json,
    load_jsonl,
    validate_core,
    validate_generator_descriptor,
    validate_repository,
)


def must_fail(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes):
    try:
        validate_core(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    except ValidationError:
        return
    raise AssertionError("negative mutation unexpectedly passed")


def descriptor_must_fail(descriptor):
    try:
        validate_generator_descriptor(descriptor)
    except ValidationError:
        return
    raise AssertionError("invalid generator descriptor unexpectedly passed")


def main():
    validate_repository(ROOT)

    v04 = load_json(V04_PATH)
    v05 = load_json(V05_PATH)
    audit = load_json(AUDIT_PATH)
    impl = load_json(IMPL_PATH)
    contract = load_json(CONTRACT_PATH)
    gen_schema = load_json(GEN_SCHEMA_PATH)
    freeze_schema = load_json(FREEZE_SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    plans = load_jsonl(PLANS_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    negative_cases = 0

    x = copy.deepcopy(v05)
    x["batch_ready"] = True
    must_fail(v04, x, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(v05)
    x["closed_execution_blockers"] = ["P2-EXEC-001"]
    must_fail(v04, x, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(impl)
    x["open_blockers"].remove("P2-EXEC-004")
    must_fail(v04, v05, audit, x, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["lanes"] = [lane for lane in x["lanes"] if lane["lane_id"] != "P2-A_PRIME"]
    must_fail(v04, v05, audit, impl, x, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["estimand_lock"]["P2-C1"]["only_allowed_difference"] = "ROLE_BINDING_PLUS_RULE_VISIBILITY"
    must_fail(v04, v05, audit, impl, x, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["estimand_lock"]["P2-C3"]["component_credit_forbidden"] = False
    must_fail(v04, v05, audit, impl, x, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["mapping_boundary"]["plate_value_access_before_mapping"] = True
    must_fail(v04, v05, audit, impl, x, gen_schema, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(gen_schema)
    x["properties"]["lane_id"]["enum"] = ["P2-A", "P2-B"]
    must_fail(v04, v05, audit, impl, contract, x, freeze_schema, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(freeze_schema)
    x["properties"]["estimand_lock"]["const"]["P2-C2"]["only_allowed_difference"] = "ANYTHING"
    must_fail(v04, v05, audit, impl, contract, gen_schema, x, fixture, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(fixture)
    x["descriptors"][0]["canonical_sha256"] = "0" * 64
    must_fail(v04, v05, audit, impl, contract, gen_schema, freeze_schema, x, plans, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(fixture["descriptors"][0]["descriptor"])
    x["seed"] = 42
    descriptor_must_fail(x)
    negative_cases += 1

    x = copy.deepcopy(plans)
    qrm = next(p for p in x if p.get("hypothesis_id") == "QRM-H1")
    qrm["estimand_lock"] = {}
    must_fail(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, x, batches, freezes)
    negative_cases += 1

    x = copy.deepcopy(batches)
    x.append({"batch_id": "ILLEGAL-P2", "plan_id": "K2PV-QRM-002", "hypothesis_id": "QRM-H1"})
    must_fail(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, x, freezes)
    negative_cases += 1

    x = copy.deepcopy(freezes)
    x.append({"freeze_id": "ILLEGAL-P2-FREEZE", "plan_id": "K2PV-QRM-002"})
    must_fail(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, x)
    negative_cases += 1

    print(f"k2-qimen-p2-execution-contract-tests: PASS negative_cases={negative_cases}")


if __name__ == "__main__":
    main()
