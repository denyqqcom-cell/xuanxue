#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_mixed_voice_holds as v


def hold():
    return {"source_id":"QM-SRC-9000","status":"PARTIAL_READING_CONFIRMED","reviewed_page_start":1,"reviewed_page_end":50,"verification_mode":"VISUAL_PAGE","hold_policy":"BLOCK_FORMAL_EVIDENCE_UNTIL_VOICE_SCHEMA","reason":"mixed voice observed","allowed_voice_layers":sorted(v.LAYERS),"review_status":"REVIEWED"}


def must_pass(holds,evidence):
    issues=v.validate_rows({"QM-SRC-9000"},holds,evidence)
    assert not issues,issues


def must_fail(holds,evidence,needle):
    issues=v.validate_rows({"QM-SRC-9000"},holds,evidence)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=hold();must_pass([base],[])

    bad=copy.deepcopy(base);bad["reviewed_page_end"]=0
    must_fail([bad],[],"invalid reviewed page range")

    bad=copy.deepcopy(base);bad["hold_policy"]="ALLOW"
    must_fail([bad],[],"invalid hold_policy")

    bad=copy.deepcopy(base);bad["allowed_voice_layers"]=["BASE_TEXT"]
    must_fail([bad],[],"allowed_voice_layers")

    must_fail([base,copy.deepcopy(base)],[],"duplicate hold row")

    must_fail([base],[{"source_id":"QM-SRC-9000","evidence_id":"E-1"}],"formal evidence E-1 is forbidden")

    unknown=copy.deepcopy(base);unknown["source_id"]="QM-SRC-9999"
    must_fail([unknown],[],"unknown source_id")

    print("k2-mixed-voice-hold-tests: PASS")
    print("cases=7")

if __name__=="__main__":main()
