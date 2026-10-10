"""Front door: python main.py check"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check() -> int:
    results = {}
    for name, cmd in (("security", ["devtools", "scan"]), ("links", ["devtools", "links", "--offline"])):
        if not shutil.which(cmd[0]):
            print(f"== {name}: SKIPPED ({cmd[0]} not on PATH)")
            continue
        print(f"== {name}: {' '.join(cmd)}")
        results[name] = subprocess.run(cmd, cwd=ROOT, check=False).returncode == 0  # the exit code is the answer
    print("\n" + "  ".join(f"{n}:{'ok' if ok else 'FAIL'}" for n, ok in results.items()))
    return 0 if results and all(results.values()) else 1


if __name__ == "__main__":
    if sys.argv[1:] != ["check"]:
        sys.exit(__doc__)
    sys.exit(check())
