import sys, json
d = json.load(sys.stdin)
items = d["items"]
multi = [i for i in items if len(i["atoms"]) > 1]
print(f"概念 {len(items)} 个，连接≥2原子的 {len(multi)} 个")
for i in multi[:10]:
    print("  ", i["name"][:40], "->", i["atoms"])
