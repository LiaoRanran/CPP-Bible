# -*- coding: utf-8 -*-
"""676c-G Task A 第二轮: 扩池候选核实"""
import json, time, urllib.request, ssl

CVES = [
    "CVE-2017-7529", "CVE-2016-6153", "CVE-2016-6303", "CVE-2016-6306",
    "CVE-2014-3505", "CVE-2015-0206", "CVE-2015-0288", "CVE-2021-3449",
    "CVE-2021-3712", "CVE-2018-16890", "CVE-2019-15601", "CVE-2017-7407",
    "CVE-2018-1000120", "CVE-2018-1000122", "CVE-2020-8286", "CVE-2022-27780",
    "CVE-2023-27534", "CVE-2023-28322", "CVE-2016-7141", "CVE-2016-7167",
]
ctx = ssl.create_default_context()
out = open(__file__.rsplit("\\", 1)[0] + "\\cve_verify_r2.txt", "w", encoding="utf-8")
ok = fail = 0
for cve in CVES:
    try:
        with urllib.request.urlopen("https://cveawg.mitre.org/api/cve/" + cve, timeout=25, context=ctx) as r:
            d = json.loads(r.read().decode("utf-8"))
        descs = d["containers"]["cna"]["descriptions"]
        desc = next((x["value"] for x in descs if x.get("lang") == "en"), "")[:280]
        cwes = []
        cna = d["containers"]["cna"]
        for pt in cna.get("problemTypes", []):
            for x in pt.get("descriptions", []):
                if x.get("lang") == "en":
                    cwes.append(str(x.get("cweId", "")))
        out.write(f"{cve} | {';'.join(cwes)[:30]} | {desc} | OK\n")
        ok += 1
    except Exception as e:  # noqa: BLE001
        out.write(f"{cve} | | FETCH-FAIL {type(e).__name__} | FAIL\n")
        fail += 1
    time.sleep(0.15)
out.close()
print(f"OK={ok} FAIL={fail}")
