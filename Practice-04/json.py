# IMPORTANT: this file is named json.py, the same as the standard module.
# Remove the script folder from sys.path so `import json` loads the standard module.
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if p not in ("", _here)]

import json

with open(os.path.join(_here, "sample-data.json")) as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20}  {'Speed':<6}  {'MTU':<6}")
print("-" * 50, "-" * 20, " ", "-" * 6, " ", "-" * 6)

for item in data["imdata"][:3]:
    attrs = item["l1PhysIf"]["attributes"]
    print(f"{attrs['dn']:<50} {attrs['descr']:<20}  {attrs['speed']:<6}  {attrs['mtu']:<6}")