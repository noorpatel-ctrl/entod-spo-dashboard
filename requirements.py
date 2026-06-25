"""
requirements.py
===============
Helper that installs the Python packages required by `dashboard.py`.

Usage:
    python requirements.py            # install (or upgrade) all deps
    python requirements.py --check    # verify deps, exit 0/1
    python requirements.py --print    # just print the pinned versions

Why this exists:
    Streamlit apps break silently if pandas / openpyxl / plotly drift.
    Pinning exact (or minimum) versions keeps the dashboard reproducible.
"""

import importlib
import subprocess
import sys

# ── Pinned versions (lower-bound friendly) ──────────────────────────────────
# Tested on Python 3.10 / 3.11 / 3.12.
REQUIRED = {
    "streamlit":  ">=1.32.0",
    "pandas":     ">=2.0.0",
    "openpyxl":   ">=3.1.0",
    "plotly":     ">=5.18.0",
    "pyxlsb":     ">=1.0.9",   # only needed for .xlsb files
}


def _pip_install(pkg_spec: str) -> None:
    """Run `pip install <pkg_spec>` and stream output.

    Retries with ``--break-system-packages`` if the first attempt is blocked
    by PEP 668 (e.g. Debian/Ubuntu system Python with no venv). venv users
    get the normal clean install.
    """
    print(f"  → pip install {pkg_spec}")
    base = [sys.executable, "-m", "pip", "install", "--upgrade", pkg_spec]
    try:
        subprocess.check_call(base)
        return
    except subprocess.CalledProcessError:
        # PEP 668 — retry with --break-system-packages (only if NOT in a venv)
        in_venv = (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        )
        if in_venv:
            raise
        print("    (externally-managed environment detected, "
              "retrying with --break-system-packages)")
        subprocess.check_call(base + ["--break-system-packages"])


def install_all() -> None:
    """Install every dependency listed in REQUIRED."""
    print("📦 Installing ENTOD Dashboard requirements…\n")
    for pkg, ver in REQUIRED.items():
        _pip_install(f"{pkg}{ver}")
    print("\n✅ All requirements installed.")
    print("👉 Launch the dashboard with:    streamlit run dashboard.py")


def check_all() -> int:
    """Return 0 if every required package is importable, else 1."""
    print("🔍 Checking installed packages…\n")
    ok = True
    width = max(len(p) for p in REQUIRED) + 2
    for pkg, ver in REQUIRED.items():
        try:
            m = importlib.import_module(pkg)
            version = getattr(m, "__version__", "unknown")
            print(f"  ✔ {pkg:<{width}} {version}")
        except Exception as e:  # pragma: no cover
            print(f"  ✘ {pkg:<{width}} MISSING ({e})")
            ok = False
    print()
    print("All good ✅" if ok else "Some packages missing ❌ — run without --check")
    return 0 if ok else 1


def print_list() -> None:
    """Print a `pip install`-style one-liner of every requirement."""
    line = " ".join(f"{p}{v}" for p, v in REQUIRED.items())
    print(line)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--check" in argv:
        return check_all()
    if "--print" in argv:
        print_list()
        return 0
    install_all()
    return 0


if __name__ == "__main__":
    sys.exit(main())
