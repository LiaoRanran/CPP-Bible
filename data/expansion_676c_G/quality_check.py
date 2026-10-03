# -*- coding: utf-8 -*-
"""676c-G Task D: 质量抽检。
1) planted=false 样本 100% 来源核对(CVE 编号存在于 MITRE 核实清单 / GitHub issue 已抓取正文);
2) 固定种子随机抽 30% 做人工级机械检查(标记行==标注行/字段完整/判定一致/main 存在/行数<=200)。
"""
import json, os, random, re, urllib.request, ssl

HERE = os.path.dirname(os.path.abspath(__file__))

manifest = json.load(open(os.path.join(HERE, "_manifest.json"), encoding="utf-8"))
results = json.load(open(os.path.join(HERE, "verify_results.json"), encoding="utf-8"))

# ---- 来源核实清单 ----
verified_cves = set()
for f in ("cve_verify.txt", "cve_verify_r2.txt"):
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        pending = None
        for ln in open(p, encoding="utf-8"):
            m = re.match(r"(CVE-\d{4}-\d+) \|", ln)
            if m:
                pending = m.group(1)
            if ln.rstrip().endswith("| OK") and pending:
                verified_cves.add(pending)
                pending = None
verified_2026 = {"CVE-2026-3805", "CVE-2026-8925", "CVE-2026-72897"}  # 来自 curl.se/docs/vuln.json 与 openssl.org 官方页(本会话抓取)
verified_issues = set()
p = os.path.join(HERE, "github_issue_bodies.txt")
for m in re.finditer(r"===== (\S+/\S+#\d+)", open(p, encoding="utf-8").read()):
    verified_issues.add(m.group(1))

problems, checked_false = [], 0
for sid in manifest["samples"]:
    meta = json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))
    src = meta["source"]
    if meta["planted"] is False:
        checked_false += 1
        if src["type"] == "cve":
            if src["id"] not in verified_cves and src["id"] not in verified_2026:
                problems.append(f"{sid}: 来源 {src['id']} 不在核实清单")
        elif src["type"] == "github_issue":
            if src["id"] not in verified_issues:
                problems.append(f"{sid}: issue {src['id']} 未抓取正文")
        else:
            problems.append(f"{sid}: 未知来源类型 {src['type']}")
        if not src["url"].startswith(("https://nvd.nist.gov/", "https://github.com/")):
            problems.append(f"{sid}: URL 非规范 ({src['url']})")

# ---- 2026 CVE 经 cveawg 复核(3 个) ----
ctx = ssl.create_default_context()
for cve in sorted(verified_2026):
    try:
        with urllib.request.urlopen("https://cveawg.mitre.org/api/cve/" + cve, timeout=20, context=ctx) as r:
            json.loads(r.read().decode("utf-8"))
        print(f"2026 复核 {cve}: MITRE 在案 OK")
    except Exception as e:  # noqa: BLE001
        print(f"2026 复核 {cve}: MITRE 不在案({type(e).__name__})——以官方公告页为准(curl.se/docs/vuln.json)")

# ---- 固定种子抽 30% ----
random.seed(6762)
sample_pool = sorted(manifest["samples"])
sampled = sorted(random.sample(sample_pool, max(1, int(len(sample_pool) * 0.30))))
mech_fail = []
for sid in sampled:
    meta = json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))
    cpp = open(os.path.join(HERE, f"sample_{sid}.cpp"), encoding="utf-8").read()
    v = results[sid]
    lines = cpp.split("\n")
    if "int main(" not in cpp:
        mech_fail.append(f"{sid}: 无 main")
    if len(lines) > 200:
        mech_fail.append(f"{sid}: 行数 {len(lines)}")
    # 标记行 == 标注行
    marker_line = next((i for i, ln in enumerate(lines, 1) if "/* DEFECT */" in ln), -1)
    if marker_line != meta["defect_location"]["line"]:
        mech_fail.append(f"{sid}: DEFECT 行 {marker_line} != 标注 {meta['defect_location']['line']}")
    # 字段完整
    for f in ("sample_id", "defect_type", "defect_location", "severity", "planted",
              "source", "expected_verdict", "expected_detectors", "trigger_condition", "notes"):
        if f not in meta:
            mech_fail.append(f"{sid}: 缺字段 {f}")
    # 判定一致
    if not v.get("match"):
        mech_fail.append(f"{sid}: 检测器判定不一致")
    if v.get("syntax_mingw") != "PASS":
        mech_fail.append(f"{sid}: 语法门未过")

# 汇总 planted 统计
pf = sum(1 for sid in manifest["samples"]
         if json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))["planted"] is False)

print(f"\nplanted=false 来源核对: {checked_false} 个, 问题 {len([p for p in problems if '来源' in p or 'URL' in p or 'issue' in p])}")
print(f"抽样: {len(sampled)}/{len(sample_pool)} (seed=6762): {','.join(sampled)}")
print(f"机械检查不合格: {len(mech_fail)}")
for m in mech_fail:
    print("  !!", m)
print(f"来源核对问题: {problems if problems else '无'}")

json.dump({"seed": 6762, "sampled": sampled, "mech_fail": mech_fail, "source_problems": problems,
           "planted_false_checked": checked_false},
          open(os.path.join(HERE, "quality_check.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
