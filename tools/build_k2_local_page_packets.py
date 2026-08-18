#!/usr/bin/env python3
"""Build local-only page packets for K2B Wave1.

This tool never writes into the repository knowledge tree. It is intentionally
mechanical: it resolves each official Wave1 source to canonical local bytes,
verifies SHA256 identity, extracts existing text layers page-by-page for
TEXT_DIRECT sources, and records honest blockers for VISUAL_REQUIRED sources.

Resolution order:
1. optional private K1 intake registry (fast path);
2. canonical SHA256 discovery under explicit --search-root paths (portable
   fallback when the private intake registry is unavailable on this machine).

It does not create Evidence or Claims.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_PATH_RE = re.compile(r"^([A-Za-z]):[\\/](.*)$")
WSL_PATH_RE = re.compile(r"^/mnt/([A-Za-z])/(.*)$")
DISCOVERY_EXTENSIONS = {
    ".pdf", ".txt", ".md", ".text", ".rtf", ".html", ".htm",
    ".doc", ".docx", ".odt", ".epub",
}
SKIP_DIR_NAMES = {
    ".git", ".gradle", "build", "node_modules", "__pycache__",
    "K2_WAVE1_PAGE_PACKETS",
}


def fail(msg):
    print(f"k2-local-page-packets: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_jsonl(path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as e:
            fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row, dict):
            fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows


def ensure_local_only(path: Path):
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return resolved
    fail(f"output must stay outside repository: {resolved}")


def normalize_local_path(raw, host_os=None):
    """Translate Windows<->WSL drive paths without assuming the current host.

    The returned Path is suitable for the active host when host_os is omitted.
    Tests may pass host_os explicitly and compare Path.as_posix().
    """
    if not isinstance(raw, str) or not raw.strip():
        return None
    value = raw.strip()
    host = host_os or os.name

    match = WINDOWS_PATH_RE.match(value)
    if match:
        drive = match.group(1)
        rest = match.group(2).replace("\\", "/")
        if host == "nt":
            return Path(f"{drive.upper()}:/{rest}")
        return Path(f"/mnt/{drive.lower()}/{rest}")

    match = WSL_PATH_RE.match(value.replace("\\", "/"))
    if match and host == "nt":
        drive = match.group(1)
        rest = match.group(2)
        return Path(f"{drive.upper()}:/{rest}")

    return Path(value).expanduser()


def private_source_index(intake_root):
    if intake_root is None:
        return {}
    root = intake_root.expanduser().resolve()
    if not root.is_dir():
        return {}
    out = {}
    for path in sorted(root.glob("*/sources.jsonl")):
        for row in load_jsonl(path):
            sid = row.get("source_id")
            if isinstance(sid, str) and sid:
                if sid in out:
                    fail(f"duplicate private source_id: {sid}")
                out[sid] = row
    return out


def sha_text(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def iter_discovery_files(root: Path, output_dir: Path):
    root = root.expanduser()
    if not root.exists():
        return
    if root.is_file():
        if root.suffix.lower() in DISCOVERY_EXTENSIONS:
            yield root
        return

    output_resolved = output_dir.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        current = Path(dirpath)
        try:
            current.resolve().relative_to(output_resolved)
            dirnames[:] = []
            continue
        except ValueError:
            pass
        except OSError:
            pass
        for name in filenames:
            path = current / name
            if path.suffix.lower() not in DISCOVERY_EXTENSIONS:
                continue
            try:
                path.resolve().relative_to(output_resolved)
                continue
            except ValueError:
                pass
            except OSError:
                pass
            if path.is_file():
                yield path


def discover_hash_matches(search_roots, target_hashes, output_dir):
    """Find exact canonical bytes by SHA256 under user-supplied roots.

    Only research/document extensions are scanned; archives and build trees are
    intentionally skipped so a missing private registry does not force hashing
    unrelated multi-GB archives.
    """
    targets = set(target_hashes)
    matches = {h: [] for h in targets}
    seen_paths = set()
    remaining = set(targets)
    for root in search_roots:
        for path in iter_discovery_files(root, output_dir):
            try:
                resolved = path.resolve()
            except OSError:
                continue
            key = str(resolved).casefold() if os.name == "nt" else str(resolved)
            if key in seen_paths:
                continue
            seen_paths.add(key)
            try:
                digest = sha_file(path)
            except (OSError, PermissionError):
                continue
            if digest in targets:
                matches[digest].append(path)
                remaining.discard(digest)
        if not remaining:
            break
    return matches


def extract_pdf_text(path: Path):
    exe = shutil.which("pdftotext")
    if not exe:
        return None, "TEXT_EXTRACTION_FAILED", "pdftotext is not installed"
    proc = subprocess.run(
        [exe, "-layout", str(path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        return None, "TEXT_EXTRACTION_FAILED", err[:240] or f"pdftotext exit {proc.returncode}"
    text = proc.stdout.decode("utf-8", errors="replace")
    pages = text.split("\f")
    if pages and pages[-1] == "":
        pages.pop()
    return pages, None, None


def write_packet(path: Path, source_id: str, source_file_sha256: str, pages):
    with path.open("w", encoding="utf-8") as fh:
        for page_no, text in enumerate(pages, 1):
            row = {
                "source_id": source_id,
                "source_file_sha256": source_file_sha256,
                "page": page_no,
                "text": text,
                "text_sha256": sha_text(text),
                "char_count": len(text),
            }
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def validate_plan(plan):
    seen = set()
    for n, item in enumerate(plan, 1):
        sid = item.get("source_id")
        if not isinstance(sid, str) or not sid:
            fail(f"plan row {n}: missing source_id")
        if sid in seen:
            fail(f"plan contains duplicate source_id: {sid}")
        seen.add(sid)
        expected_hash = item.get("file_sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            fail(f"{sid}: plan missing canonical file_sha256")


def verify_private_registry_hash(sid, item, private_row):
    private_hash = private_row.get("file_sha256")
    if not isinstance(private_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", private_hash):
        fail(f"{sid}: private K1 registry missing valid file_sha256")
    if private_hash != item.get("file_sha256"):
        fail(f"{sid}: private K1 hash differs from official Wave1 plan")


def verify_local_file_hash(sid, expected_hash, local_path):
    actual_hash = sha_file(local_path)
    if actual_hash != expected_hash:
        fail(f"{sid}: local file SHA256 mismatch; expected {expected_hash}, got {actual_hash}")
    return actual_hash


def resolve_source(sid, item, private, hash_matches):
    expected_hash = item["file_sha256"]
    private_row = private.get(sid)
    if private_row is not None:
        verify_private_registry_hash(sid, item, private_row)
        local_path = normalize_local_path(private_row.get("local_path"))
        if local_path is not None and local_path.is_file():
            actual_hash = verify_local_file_hash(sid, expected_hash, local_path)
            return local_path, actual_hash, "PRIVATE_REGISTRY"

    candidates = hash_matches.get(expected_hash) or []
    if candidates:
        local_path = candidates[0]
        actual_hash = verify_local_file_hash(sid, expected_hash, local_path)
        return local_path, actual_hash, "CANONICAL_SHA256_SEARCH"

    return None, expected_hash, None


def blocked_row(sid, lane, source_file_sha256, code, reason, identity_mode=None):
    return {
        "source_id": sid,
        "source_file_sha256": source_file_sha256,
        "identity_mode": identity_mode,
        "execution_lane": lane,
        "packet_status": "BLOCKED",
        "blocker_code": code,
        "blocker_reason": reason,
        "packet_file": None,
        "packet_sha256": None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--intake-root", type=Path)
    ap.add_argument(
        "--search-root", type=Path, action="append", default=[],
        help="repeatable local corpus root used for canonical SHA256 discovery",
    )
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    output_dir = ensure_local_only(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = load_jsonl(args.plan)
    validate_plan(plan)
    private = private_source_index(args.intake_root)

    target_hashes = {item["file_sha256"] for item in plan}
    search_roots = [normalize_local_path(str(p)) for p in args.search_root]
    search_roots = [p for p in search_roots if p is not None]
    hash_matches = discover_hash_matches(search_roots, target_hashes, output_dir) if search_roots else {h: [] for h in target_hashes}

    manifest = []
    for item in plan:
        sid = item["source_id"]
        lane = item.get("execution_lane")
        local_path, actual_hash, identity_mode = resolve_source(sid, item, private, hash_matches)
        if local_path is None:
            manifest.append(blocked_row(
                sid, lane, item.get("file_sha256"), "FILE_MISSING",
                "canonical bytes not resolved from private K1 registry or explicit search roots",
            ))
            continue

        if lane == "VISUAL_REQUIRED":
            manifest.append(blocked_row(
                sid, lane, actual_hash, "VISION_UNAVAILABLE",
                "source requires original-page visual verification; text/OCR alone is insufficient",
                identity_mode=identity_mode,
            ))
            continue

        if lane != "TEXT_DIRECT":
            manifest.append(blocked_row(
                sid, lane, actual_hash, "ACCESS_UNAVAILABLE",
                "source is not classified for direct text-layer extraction",
                identity_mode=identity_mode,
            ))
            continue

        suffix = local_path.suffix.lower()
        expected_pages = item.get("pages")
        if suffix == ".pdf":
            pages, code, reason = extract_pdf_text(local_path)
            if pages is None:
                manifest.append(blocked_row(sid, lane, actual_hash, code, reason, identity_mode))
                continue
            if isinstance(expected_pages, int) and len(pages) != expected_pages:
                manifest.append(blocked_row(
                    sid, lane, actual_hash, "TEXT_EXTRACTION_FAILED",
                    f"text-layer page count {len(pages)} != registered PDF pages {expected_pages}",
                    identity_mode=identity_mode,
                ))
                continue
        else:
            try:
                pages = [local_path.read_text(encoding="utf-8")]
            except (UnicodeDecodeError, OSError):
                manifest.append(blocked_row(
                    sid, lane, actual_hash, "TEXT_EXTRACTION_FAILED",
                    "non-PDF TEXT_OK source is not UTF-8 readable",
                    identity_mode=identity_mode,
                ))
                continue

        packet_file = output_dir / f"{sid}.pages.jsonl"
        write_packet(packet_file, sid, actual_hash, pages)
        packet_hash = sha_file(packet_file)
        manifest.append({
            "source_id": sid,
            "source_file_sha256": actual_hash,
            "identity_mode": identity_mode,
            "execution_lane": lane,
            "packet_status": "READY",
            "blocker_code": None,
            "blocker_reason": None,
            "packet_file": packet_file.name,
            "packet_sha256": packet_hash,
            "page_count": len(pages),
            "total_chars": sum(len(text) for text in pages),
        })

    manifest_path = output_dir / "manifest.jsonl"
    manifest_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in manifest),
        encoding="utf-8",
    )
    ready = sum(1 for row in manifest if row["packet_status"] == "READY")
    blocked = len(manifest) - ready
    identity_counts = {}
    for row in manifest:
        mode = row.get("identity_mode") or "UNRESOLVED"
        identity_counts[mode] = identity_counts.get(mode, 0) + 1
    print("k2-local-page-packets: PASS")
    print(f"plan_units={len(plan)} ready={ready} blocked={blocked} output={output_dir}")
    print("identity_modes=" + json.dumps(identity_counts, ensure_ascii=False, sort_keys=True))
    print(f"manifest={manifest_path}")


if __name__ == "__main__":
    main()
