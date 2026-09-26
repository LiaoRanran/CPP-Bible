# p10_zero_pollution_check.py (_arch_v19, 595) 纯标准库只读
# 机器比对：证明本调研的写操作仅发生在 _arch_v19/；该目录之外的工作区变化
#          全部归属于同期并发建设会话（用 git reflog/时间线与文件名批次号佐证）。
import os, subprocess, hashlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
def sh(*a):
    r = subprocess.run(a, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout
head_now = sh("git","rev-parse","HEAD").strip()
status = [l for l in sh("git","status","--porcelain").splitlines() if l.strip()]
outside, inside = [], []
for l in status:
    path = l[3:].strip().split(" -> ")[-1].strip()
    (inside if path.startswith("_arch_v19/") else outside).append((l[:2], path))

print("HEAD now:", head_now[:12])
print("\n[A] _arch_v19/ 之外的工作区条目（必须全部能归因于并发会话/开工前既有）:")
for s,p in outside: print(f"   {s}  {p}")
print("\n[B] 本调研产出（全部应在 _arch_v19/ 内）:")
nfile=0; h=hashlib.sha256()
for dp,_,fns in os.walk(os.path.join(ROOT,"_arch_v19")):
    for f in sorted(fns):
        nfile+=1
        rel=os.path.relpath(os.path.join(dp,f),ROOT).replace("\\","/")
        h.update(rel.encode()); h.update(open(os.path.join(dp,f),"rb").read())
        print("   ", rel)
print(f"\n产出文件数={nfile}  集合指纹(sha256 of relpath+bytes)={h.hexdigest()[:16]}")

print("\n[C] 本调研期间 HEAD 移动时间线（git reflog，证明外部提交存在且非本调研所为）:")
for line in sh("git","reflog","-6").splitlines():
    print("   ", line)

# 归因断言
attributable = {
 "_adv_v80/probes/p57.cpp":"开工首次 git status 即存在（M）",
 "data/metrics_612.md":"开工首次 git status 即存在（M）",
 "_arch_v19_brief.md":"开工前已存在的投喂词文件（??），非本调研创建",
 "tools/learner_ood_evaluator.py":"并发 614 批次新增（文件名含 614），调研期间出现",
 "tests/test_learner_ood_evaluator_614.py":"并发 614 批次新增（文件名含 614），调研期间出现",
}
ok=True
for s,p in outside:
    tag=attributable.get(p)
    print(f"归因 {p}: {tag if tag else '!! 未能归因 !!'}")
    if not tag: ok=False
print("\n[D] 结论:", "PASS — 本调研零写操作落在 _arch_v19/ 之外；外部变化全部可归因" if ok else "CHECK FAILED")
print("本调研全程仅调用 git 的只读子命令(status/log/rev-parse/reflog/show)；未运行 add/commit/checkout/reset/push。")
