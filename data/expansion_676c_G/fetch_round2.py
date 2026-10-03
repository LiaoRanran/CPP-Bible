# -*- coding: utf-8 -*-
"""676c-G Task A 第二轮: (1) r2 CVE 核实 (2) GitHub Search API 找真实 issue"""
import json, time, urllib.request, ssl

ctx = ssl.create_default_context()
UA = {"User-Agent": "cpp-bible-676cG-batch/1.0"}

# ---------- (1) r2 CVE 核实 ----------
CVES = [
    "CVE-2017-7529", "CVE-2016-6153", "CVE-2016-6303", "CVE-2016-6306",
    "CVE-2014-3505", "CVE-2015-0206", "CVE-2015-0288", "CVE-2021-3449",
    "CVE-2021-3712", "CVE-2018-16890", "CVE-2019-15601", "CVE-2017-7407",
    "CVE-2018-1000120", "CVE-2018-1000122", "CVE-2020-8286", "CVE-2022-27780",
    "CVE-2023-27534", "CVE-2023-28322", "CVE-2016-7141", "CVE-2016-7167",
]
with open("cve_verify_r2.txt", "w", encoding="utf-8") as out:
    ok = fail = 0
    for cve in CVES:
        try:
            with urllib.request.urlopen("https://cveawg.mitre.org/api/cve/" + cve, timeout=25, context=ctx) as r:
                d = json.loads(r.read().decode("utf-8"))
            descs = d["containers"]["cna"]["descriptions"]
            desc = next((x["value"] for x in descs if x.get("lang") == "en"), "")[:260]
            cwes = []
            for pt in d["containers"]["cna"].get("problemTypes", []):
                for x in pt.get("descriptions", []):
                    if x.get("lang") == "en":
                        cwes.append(str(x.get("cweId", "")))
            out.write(f"{cve} | {';'.join(cwes)[:30]} | {desc} | OK\n")
            ok += 1
        except Exception as e:  # noqa: BLE001
            out.write(f"{cve} | | FETCH-FAIL {type(e).__name__} | FAIL\n")
            fail += 1
        time.sleep(0.12)
    print(f"cveawg r2: OK={ok} FAIL={fail}")

# ---------- (2) GitHub Search API 找 issue ----------
def gh_search(q):
    url = "https://api.github.com/search/issues?q=" + urllib.request.quote(q) + "&per_page=8"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

QUERIES = [
    "repo:nlohmann/json heap-buffer-overflow in:title,body type:issue",
    "repo:nlohmann/json use-after-free in:title type:issue",
    "repo:fmtlib/fmt use-after-free OR dangling in:title type:issue",
    "repo:gabime/spdlog crash OR overflow in:title type:issue",
    "repo:abseil/abseil-cpp out-of-bounds OR overflow in:title type:issue",
    "repo:catchorg/Catch2 crash OR overflow in:title type:issue",
    "repo:protocolbuffers/protobuf heap-buffer-overflow type:issue",
    "repo:leethomason/tinyxml2 out-of-bounds OR overflow type:issue",
    "repo:madler/zlib heap-buffer-overflow type:issue",
    "repo:open-source-parsers/jsoncpp out-of-bounds OR overflow type:issue",
]
lines = []
for q in QUERIES:
    try:
        d = gh_search(q)
        lines.append(f"### QUERY: {q}  (total={d.get('total_count')})")
        for it in d.get("items", []):
            lines.append(f"- [{it['number']}] {it['title']} | {it['html_url']} | state={it['state']}")
        time.sleep(2.5)  # GitHub search API 限速 10 req/min
    except Exception as e:  # noqa: BLE001
        lines.append(f"### QUERY: {q}  FAIL {type(e).__name__}: {str(e)[:120]}")
        time.sleep(2.5)
with open("github_issues_search.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("github search done:", len(lines), "lines")
