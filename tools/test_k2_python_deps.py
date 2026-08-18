#!/usr/bin/env python3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_k2_python_deps as deps


def expect_system_exit(fn):
    try:
        fn()
    except SystemExit:
        return
    raise AssertionError("expected SystemExit")


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td).resolve()
        child = root / "child"
        child.mkdir()
        outside = root.parent

        assert deps.is_within(child, root)
        assert deps.is_within(root, root)
        assert not deps.is_within(outside, child)
        assert deps.ensure_external_dir(child) == child

        # A dependency target inside the repository must fail closed even if it
        # does not exist yet.
        expect_system_exit(
            lambda: deps.ensure_external_dir(deps.ROOT / "should-not-exist-k2-deps")
        )

        # Verify concrete target-origin enforcement with a synthetic module.
        (child / "k2_fake_dep.py").write_text("__version__='1.2.3'\n", encoding="utf-8")
        sys.path.insert(0, str(child))
        try:
            sys.modules.pop("k2_fake_dep", None)
            module, origin = deps.import_from_target("k2_fake_dep", child)
            assert deps.version_of(module) == "1.2.3"
            assert deps.is_within(origin, child)
        finally:
            sys.modules.pop("k2_fake_dep", None)
            if str(child) in sys.path:
                sys.path.remove(str(child))

        # Importable modules from stdlib/global locations must not satisfy an
        # isolated target dependency requirement.
        expect_system_exit(lambda: deps.import_from_target("json", child))

    print("k2-python-deps-tests: PASS")


if __name__ == "__main__":
    main()
