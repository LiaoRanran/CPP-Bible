# -*- coding: utf-8 -*-
"""676c-G Task A: 批量核实候选 CVE 的真实性与机制描述（来源: cveawg.mitre.org 官方 API）。
输出: cve_verify.txt  每行: CVE-ID | CWE | 描述前280字符 | 状态
"""
import json, time, urllib.request, ssl

CVES = [
    # openssl 经典
    "CVE-2014-0160", "CVE-2012-2110", "CVE-2014-3508", "CVE-2014-3571",
    "CVE-2015-0286", "CVE-2015-1789", "CVE-2015-1793", "CVE-2015-1791",
    "CVE-2016-2105", "CVE-2016-2106", "CVE-2016-2176", "CVE-2016-2177",
    "CVE-2016-2178", "CVE-2017-3731", "CVE-2018-0739", "CVE-2020-1971",
    "CVE-2022-0778", "CVE-2022-3602", "CVE-2014-0224", "CVE-2015-0204",
    # curl
    "CVE-2017-1000100", "CVE-2017-8816", "CVE-2019-3823", "CVE-2021-22945",
    "CVE-2023-38545", "CVE-2021-22876", "CVE-2021-22898", "CVE-2020-8284",
    "CVE-2020-8177", "CVE-2022-32221", "CVE-2015-3148", "CVE-2018-16839",
    "CVE-2017-1000257", "CVE-2019-5436",
    # sqlite / libpng / zlib / libwebp / libxml2 / nginx / php / 其他用户态
    "CVE-2015-3416", "CVE-2019-8457", "CVE-2020-11655", "CVE-2020-11656",
    "CVE-2022-35737", "CVE-2017-10989", "CVE-2015-8126", "CVE-2018-13785",
    "CVE-2016-9840", "CVE-2016-9841", "CVE-2023-4863", "CVE-2016-4658",
    "CVE-2017-9047", "CVE-2021-23017", "CVE-2013-2028", "CVE-2019-11034",
    "CVE-2019-11036", "CVE-2018-1124", "CVE-2016-0777", "CVE-2014-6271",
    "CVE-2018-10933", "CVE-2023-48795", "CVE-2016-5385", "CVE-2015-7547",
    "CVE-2018-1000001", "CVE-2021-4034", "CVE-2019-9514",
    # 内核 CVE（planted=true 用户态等价模拟用）
    "CVE-2016-0728", "CVE-2014-0196", "CVE-2017-2636", "CVE-2017-11176",
    "CVE-2016-5195", "CVE-2018-9568", "CVE-2016-2384", "CVE-2022-0847",
]

ctx = ssl.create_default_context()
out = open(__file__.rsplit("\\", 1)[0] + "\\cve_verify.txt", "w", encoding="utf-8")
ok = fail = 0
for cve in CVES:
    url = "https://cveawg.mitre.org/api/cve/" + cve
    try:
        with urllib.request.urlopen(url, timeout=25, context=ctx) as r:
            d = json.loads(r.read().decode("utf-8"))
        descs = d["containers"]["cna"]["descriptions"]
        desc = next((x["value"] for x in descs if x.get("lang") == "en"), "")[:280]
        cwes = []
        for cont in d["containers"].values():
            if not isinstance(cont, dict):
                continue
            for ad in cont.get("affected", []):
                for cd in ad.get("values", []):
                    for ce in cd.get("CWE", []):
                        cwes.append(ce.get("ID", "") + " " + ce.get("name", ""))
            cd = cont.get("problemTypes")
            if cd:
                for pt in cd:
                    for x in pt.get("descriptions", []):
                        if x.get("lang") == "en":
                            cwes.append(str(x.get("cweId", "")) + " " + str(x.get("description", "")))
        out.write(f"{cve} | {';'.join(sorted(set(cwes)))[:60]} | {desc} | OK\n")
        ok += 1
    except Exception as e:  # noqa: BLE001
        out.write(f"{cve} | | FETCH-FAIL {type(e).__name__}: {str(e)[:80]} | FAIL\n")
        fail += 1
    time.sleep(0.15)
out.close()
print(f"OK={ok} FAIL={fail} / {len(CVES)}")
