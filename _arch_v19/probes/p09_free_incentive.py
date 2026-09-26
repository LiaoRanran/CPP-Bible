# p09_free_incentive.py (_arch_v19 维度9 自由探索) 纯标准库只读
# 自由发现的新维度：验证的激励兼容性 (incentive-compatible verification)。
# 假说：单用户系统中验证者=被验证者=同一效用函数，所有压力都朝"宽松/降级/豁免"方向，
#       严格性没有外部受益人。本探针用仓内真实数据检验该压力的可见痕迹。
import os, re, sys, json, subprocess, collections
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))

def sh(*a):
    return subprocess.run(a,cwd=ROOT,capture_output=True,text=True,encoding="utf-8",errors="replace")

# 1) 活跑只读 gate --check，统计 warn 的规则分布（186 warn 是谁）
env=dict(os.environ); env["CPPBIBLE_OBS"]="0"
r=sh(sys.executable,"tools/gate_engine.py","--check")
out=r.stdout
sev_counter=collections.Counter(); warn_rules=collections.Counter()
for line in out.splitlines():
    m=re.search(r"\[(BLOCK|WARN|ADVICE)\s*\]\s+([A-Z0-9\-]+)",line)
    if m:
        sev_counter[m.group(1)]+=1; warn_rules[m.group(2)]+=1
print("="*72); print("P09 FREE DIMENSION: incentive-compatibility of verification"); print("="*72)
print("gate --check 实测:", dict(sev_counter), " (exit=%d, warn 非零退出但不阻断=设计)"%(r.returncode))
print("warn 规则分布 top10:")
for rid,c in warn_rules.most_common(10): print(f"   {rid:34s} {c}")

# 2) 规则注册表 severity 设计：block/warn/advice 与运行期 override
sys.path.insert(0,os.path.join(ROOT,"tools"))
import gate_engine as g
if not g.RULES: g._register_all()
des=collections.Counter(x.severity for x in g.RULES)
print("\n63 规则注册 severity 设计分布:", dict(des))

# 3) 豁免台账规模
def lines_skip_comments(p):
    return [l for l in open(os.path.join(ROOT,p),encoding="utf-8",errors="replace")
            if l.strip().startswith("-") or re.match(r"\s*\{\s*id",l)]
pe=os.path.join(ROOT,"tools","poison_exemptions.yaml")
ex_rows=[l for l in open(pe,encoding="utf-8") if re.match(r"\s*-\s*\{id:",l)]
legacy=sum(1 for l in ex_rows if "legacy" in l)
print(f"\npoison 毒样例豁免规则: {len(ex_rows)} 条 (redteam_seen=legacy 标记 {legacy} 条)")
for f in ("tools/compile_exempt.json","tools/artifact_producer_exempt.txt"):
    p=os.path.join(ROOT,f)
    if os.path.exists(p):
        n=len([l for l in open(p,encoding="utf-8",errors="replace") if l.strip() and not l.strip().startswith(("#","{","}"))])
        print(f"{f}: {n} 行有效条目")

# 4) git 历史中"宽松化动作"的提交比例（legacy/豁免/exempt/降级/warn/接受）
log=sh("git","log","--pretty=%s").stdout.splitlines()
kw=re.compile(r"legacy|豁免|exempt|降级|warn_only|接受|放行|宽免|adapt|适配",re.I)
loose=[l for l in log if kw.search(l)]
tight=re.compile(r"拦截|封堵|block|新增规则|收紧|防",re.I)
tight_n=sum(1 for l in log if tight.search(l))
print(f"\n提交总数={len(log)}  含宽松化语义提交≈{len(loose)} ({len(loose)/len(log):.1%})  含收紧语义≈{tight_n}")
print("宽松化提交样例:")
for l in loose[:8]: print("   ",l[:80])

# 5) 结论性度量：warn 积压是否被周期性'采纳为基线'（Goodhart: 度量变目标）
gold=sh("git","log","--pretty=%s","--grep","legacy").stdout.splitlines()
print(f"\ngit log 显式提及 legacy 的提交: {len(gold)}")
for l in gold[:6]: print("   ",l[:90])
print("\n判定材料：block=0 意味着当前没有任何规则真正拦住任何东西；")
print("186 warn 中 ATOM-CLAIM-CONCEPT-NORMALIZED 等长期挂账，近期被 golden 锁'采纳为 legacy 基线'。")
print("=> 当拦截有成本(返工)而宽松无成本(无外部用户受损)时，系统演化方向=持续宽松化。")
