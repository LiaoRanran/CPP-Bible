# -*- coding: utf-8 -*-
"""676c-G: 抓取候选 GitHub issue 正文，确认缺陷机制与最小复现代码。"""
import json, time, urllib.request, ssl

ctx = ssl.create_default_context()
UA = {"User-Agent": "cpp-bible-676cG-batch/1.0"}
ISSUES = [
    ("nlohmann/json", 5647), ("nlohmann/json", 3492), ("nlohmann/json", 575),
    ("leethomason/tinyxml2", 1065), ("leethomason/tinyxml2", 923), ("leethomason/tinyxml2", 728),
    ("open-source-parsers/jsoncpp", 1682), ("open-source-parsers/jsoncpp", 1623),
    ("open-source-parsers/jsoncpp", 1471), ("open-source-parsers/jsoncpp", 1545),
    ("madler/zlib", 1276), ("fmtlib/fmt", 3415),
]
out = []
for repo, num in ISSUES:
    url = f"https://api.github.com/repos/{repo}/issues/{num}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            d = json.loads(r.read().decode("utf-8"))
        body = (d.get("body") or "")[:1800]
        out.append(f"===== {repo}#{num} [{d.get('state')}] {d.get('title')}\n{body}\n")
        time.sleep(1.2)
    except Exception as e:  # noqa: BLE001
        out.append(f"===== {repo}#{num} FETCH-FAIL {type(e).__name__}: {str(e)[:100]}\n")
        time.sleep(1.2)
with open("github_issue_bodies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done", len(out))
