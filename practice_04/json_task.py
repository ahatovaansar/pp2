import json

with open("sample_data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<15} {'Speed':<10} {'MTU':<5}")
print("-" * 80)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]

    dn = attr["dn"]
    descr = attr.get("descr", "")
    speed = attr["speed"]
    mtu = attr["mtu"]

    print(f"{dn:<50} {descr:<15} {speed:<10} {mtu:<5}")