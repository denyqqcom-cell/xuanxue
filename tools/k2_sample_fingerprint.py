#!/usr/bin/env python3
import argparse,hashlib,hmac,json,os,re,sys,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IDENTITY_SCHEMA_PATH=ROOT/"knowledge"/"K2_PROSPECTIVE_SAMPLE_IDENTITY_SCHEMAS.jsonl"
DEFAULT_IDENTITY_SCHEMA_VERSION="SAMPLE_IDENTITY_V1"
FINGERPRINT_METHOD="HMAC_SHA256_V1"
FINGERPRINT_SCOPE="PROJECT_WIDE"
SECRET_ENV="K2_SAMPLE_FINGERPRINT_SECRET"
SCHEMA_FIELDS={
    "schema_version","required_fields","allow_extra_fields","unicode_normalization",
    "strip_outer_whitespace","empty_values_forbidden","identity_namespace_pattern",
    "source_system_pattern","raw_identity_repository_storage_forbidden","research_only",
}


def canonical_json(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_identity_schemas(root=ROOT):
    path=root/"knowledge"/"K2_PROSPECTIVE_SAMPLE_IDENTITY_SCHEMAS.jsonl"
    if not path.exists():return []
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        row=json.loads(raw)
        if not isinstance(row,dict):raise ValueError(f"identity schema row must be object: {path}:{n}")
        rows.append(row)
    return rows


def identity_schema_index(rows):
    issues=[];out={}
    if not rows:
        return out,[("<sample-identity-schema>","sample identity schema registry must contain at least one version")]
    for row in rows:
        version=row.get("schema_version") or "<missing>"
        if set(row)!=SCHEMA_FIELDS:
            issues.append((version,f"sample identity schema fields mismatch missing={sorted(SCHEMA_FIELDS-set(row))} extra={sorted(set(row)-SCHEMA_FIELDS)}"))
        if not isinstance(version,str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{2,63}",version):issues.append((version,"invalid sample identity schema_version"))
        if version in out:issues.append((version,"duplicate sample identity schema_version"))
        out[version]=row
        required=row.get("required_fields")
        if not isinstance(required,list) or not required or not all(isinstance(x,str) and x for x in required):issues.append((version,"required_fields must be non-empty string array"))
        elif len(required)!=len(set(required)):issues.append((version,"required_fields must not contain duplicates"))
        if row.get("allow_extra_fields") is not False:issues.append((version,"allow_extra_fields must be false in current governed identity schema"))
        if row.get("unicode_normalization")!="NFC":issues.append((version,"unicode_normalization must be NFC"))
        for field in ["strip_outer_whitespace","empty_values_forbidden","raw_identity_repository_storage_forbidden","research_only"]:
            if row.get(field) is not True:issues.append((version,f"{field} must be true"))
        for field in ["identity_namespace_pattern","source_system_pattern"]:
            pattern=row.get(field)
            if not isinstance(pattern,str) or not pattern:
                issues.append((version,f"{field} must be non-empty regex text"))
            else:
                try:re.compile(pattern)
                except re.error:issues.append((version,f"{field} must compile as regex"))
    return out,issues


def get_identity_schema(version=DEFAULT_IDENTITY_SCHEMA_VERSION,root=ROOT):
    rows=load_identity_schemas(root)
    index,issues=identity_schema_index(rows)
    if issues:raise ValueError(f"invalid sample identity schema registry: {issues[0][0]}: {issues[0][1]}")
    schema=index.get(version)
    if not schema:raise ValueError(f"unknown sample identity schema_version: {version}")
    return schema


def normalize_identity_material(identity_material,schema):
    if not isinstance(identity_material,dict):raise ValueError("identity_material must be a JSON object")
    required=list(schema.get("required_fields") or [])
    missing=[field for field in required if field not in identity_material]
    extra=[field for field in identity_material if field not in required]
    if missing:raise ValueError(f"identity_material missing required fields: {sorted(missing)}")
    if extra and schema.get("allow_extra_fields") is False:raise ValueError(f"identity_material contains ungoverned extra fields: {sorted(extra)}")
    normalized={}
    for field in required:
        value=identity_material.get(field)
        if not isinstance(value,str):raise ValueError(f"identity_material field must be text: {field}")
        if schema.get("strip_outer_whitespace"):value=value.strip()
        form=schema.get("unicode_normalization")
        if form:value=unicodedata.normalize(form,value)
        if schema.get("empty_values_forbidden") and not value:raise ValueError(f"identity_material field must be non-empty: {field}")
        normalized[field]=value
    namespace_pattern=schema.get("identity_namespace_pattern")
    source_pattern=schema.get("source_system_pattern")
    if namespace_pattern and not re.fullmatch(namespace_pattern,normalized.get("identity_namespace","")):
        raise ValueError("identity_namespace does not match governed pattern")
    if source_pattern and not re.fullmatch(source_pattern,normalized.get("source_system","")):
        raise ValueError("source_system does not match governed pattern")
    return normalized


def compute_fingerprint(secret,key_id,identity_material,identity_schema=None):
    if isinstance(secret,str):secret=secret.encode("utf-8")
    if not isinstance(secret,(bytes,bytearray)) or len(secret)<32:
        raise ValueError("sample fingerprint secret must contain at least 32 bytes")
    if not isinstance(key_id,str) or not key_id.strip():
        raise ValueError("key_id must be non-empty text")
    schema=identity_schema or get_identity_schema()
    normalized=normalize_identity_material(identity_material,schema)
    envelope={
        "fingerprint_method":FINGERPRINT_METHOD,
        "fingerprint_scope":FINGERPRINT_SCOPE,
        "fingerprint_key_id":key_id,
        "identity_schema_version":schema["schema_version"],
        "identity_schema_sha256":canonical_sha256(schema),
        "identity_material":normalized,
    }
    return hmac.new(bytes(secret),canonical_json(envelope).encode("utf-8"),hashlib.sha256).hexdigest()


def main():
    parser=argparse.ArgumentParser(description="Generate a project-stable sample fingerprint without storing raw identity material.")
    parser.add_argument("--key-id",required=True)
    parser.add_argument("--identity-schema-version",default=DEFAULT_IDENTITY_SCHEMA_VERSION)
    args=parser.parse_args()
    secret=os.environ.get(SECRET_ENV)
    if secret is None:raise SystemExit(f"missing environment variable: {SECRET_ENV}")
    try:
        identity=json.load(sys.stdin)
        schema=get_identity_schema(args.identity_schema_version)
        fingerprint=compute_fingerprint(secret,args.key_id,identity,schema)
    except Exception as exc:
        raise SystemExit(f"sample fingerprint generation failed: {exc}")
    print(fingerprint)


if __name__=="__main__":main()
