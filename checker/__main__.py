import sys
import yaml
from .checks import check

issues = check(yaml.safe_load(open(sys.argv[1])))
for path, msg in issues:
    print(f"{path}: {msg}")
sys.exit(1 if issues else 0)
