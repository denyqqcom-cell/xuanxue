#!/usr/bin/env python3
"""Validate the external Python dependency directory used by K2 local helpers.

The K2 page-packet builder intentionally supports dependencies installed with
``pip --target`` outside the repository. A partially interrupted target install
can leave importable pure-Python package shells while omitting native modules
needed by cffi/cryptography. This validator fails closed before corpus work
starts and also rejects accidental fallback to globally installed packages.
"""

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg):
    print(f"k2-python-deps: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def normalize_path(path):
    return Path(path).expanduser().resolve()


def is_within(path: Path, root: Path):
    try:
        normalize_path(path).relative_to(normalize_path(root))
        return True
    except ValueError:
        return False


def ensure_external_dir(path: Path):
    resolved = normalize_path(path)
    if is_within(resolved, ROOT):
        fail(f"dependency directory must stay outside repository: {resolved}")
    if not resolved.is_dir():
        fail(f"dependency directory does not exist: {resolved}")
    return resolved


def module_origin(module):
    raw = getattr(module, "__file__", None)
    if not isinstance(raw, str) or not raw:
        fail(f"module has no concrete file origin: {module.__name__}")
    return normalize_path(raw)


def import_from_target(name: str, target: Path):
    try:
        module = importlib.import_module(name)
    except Exception as exc:
        fail(f"cannot import {name}: {type(exc).__name__}: {exc}")
    origin = module_origin(module)
    if not is_within(origin, target):
        fail(f"{name} resolved outside isolated directory: {origin}")
    return module, origin


def version_of(module):
    value = getattr(module, "__version__", None)
    return str(value) if value is not None else "UNKNOWN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python-deps-dir", type=Path, required=True)
    args = ap.parse_args()

    target = ensure_external_dir(args.python_deps_dir)
    value = str(target)
    if value in sys.path:
        sys.path.remove(value)
    sys.path.insert(0, value)

    # Package roots must come from the target directory, not global site-packages.
    pypdf, pypdf_origin = import_from_target("pypdf", target)
    pdfminer, pdfminer_origin = import_from_target("pdfminer", target)
    cryptography, crypto_origin = import_from_target("cryptography", target)
    cffi, cffi_origin = import_from_target("cffi", target)

    # Exercise the exact native/runtime pieces that were missing in the observed
    # interrupted Windows target install.
    _, cffi_backend_origin = import_from_target("_cffi_backend", target)
    _, rust_origin = import_from_target("cryptography.hazmat.bindings._rust", target)
    import_from_target("pdfminer.high_level", target)
    import_from_target("pypdf._crypt_providers._cryptography", target)

    print("k2-python-deps: PASS")
    print(f"python_deps_dir={target}")
    print(f"pypdf={version_of(pypdf)} origin={pypdf_origin}")
    print(f"pdfminer={version_of(pdfminer)} origin={pdfminer_origin}")
    print(f"cryptography={version_of(cryptography)} origin={crypto_origin}")
    print(f"cffi={version_of(cffi)} origin={cffi_origin}")
    print(f"_cffi_backend_origin={cffi_backend_origin}")
    print(f"cryptography_rust_origin={rust_origin}")


if __name__ == "__main__":
    main()
