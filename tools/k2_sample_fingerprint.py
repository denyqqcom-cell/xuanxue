#!/usr/bin/env python3
import argparse,hashlib,hmac,json,os,sys

FINGERPRINT_METHOD="HMAC_SHA256_V1"
FINGERPRINT_SCOPE="PROJECT_WIDE"
SECRET_ENV="K2_SAMPLE_FINGERPRINT_SECRET"


def canonical_json(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def compute_fingerprint(secret,key_id,identity_material):
    if isinstance(secret,str):secret=secret.encode("utf-8")
    if not isinstance(secret,(bytes,bytearray)) or len(secret)<32:
        raise ValueError("sample fingerprint secret must contain at least 32 bytes")
    if not isinstance(key_id,str) or not key_id.strip():
        raise ValueError("key_id must be non-empty text")
    if not isinstance(identity_material,dict) or not identity_material:
        raise ValueError("identity_material must be a non-empty JSON object")
    envelope={
        "fingerprint_method":FINGERPRINT_METHOD,
        "fingerprint_scope":FINGERPRINT_SCOPE,
        "fingerprint_key_id":key_id,
        "identity_material":identity_material,
    }
    return hmac.new(bytes(secret),canonical_json(envelope).encode("utf-8"),hashlib.sha256).hexdigest()


def main():
    parser=argparse.ArgumentParser(description="Generate a project-stable sample fingerprint without storing raw identity material.")
    parser.add_argument("--key-id",required=True)
    args=parser.parse_args()
    secret=os.environ.get(SECRET_ENV)
    if secret is None:
        raise SystemExit(f"missing environment variable: {SECRET_ENV}")
    try:
        identity=json.load(sys.stdin)
        fingerprint=compute_fingerprint(secret,args.key_id,identity)
    except Exception as exc:
        raise SystemExit(f"sample fingerprint generation failed: {exc}")
    print(fingerprint)


if __name__=="__main__":main()
