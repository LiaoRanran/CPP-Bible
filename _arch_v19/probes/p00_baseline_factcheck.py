# p00_baseline_factcheck.py  (_arch_v19, 595)
# 纯标准库只读探针：独立核实 brief 的全部权威数字，不照抄任何前序报告。
# 用法: .venv/Scripts/python.exe _arch_v19/probes/p00_baseline_factcheck.py
import os, re, json, math, subprocess, collections, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()

def count_files(sub, pat):
    n = 0
    for dp, _, fns in os.walk(os.path.join(ROOT, sub)):
        for fn in fns:
            if fn.startswith(pat.split("*")[0]) and fn.endswith(pat.split("*")[1]):
                n += 1
    return n

# ---- Clopper-Pearson: regularized incomplete beta via Lentz continued fraction ----
def _betacf(a, b, x, itmax=300, eps=3e-14):
    qab, qap, qam = a+b, a+1.0, a-1.0
    c = 1.0
    d = 1.0 - qab*x/qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0/d
    h = d
    for m in range(1, itmax+1):
        m2 = 2*m
        aa = m*(b-m)*x/((qam+m2)*(a+m2))
        d = 1.0+aa*d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0+aa/c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0/d; h *= d*c
        aa = -(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d = 1.0+aa*d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0+aa/c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0/d
        de = d*c; h *= de
        if abs(de-1.0) < eps: break
    return h

def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)
    bt = math.exp(lbeta + a*math.log(x) + b*math.log(1.0-x))
    if x < (a+1.0)/(a+b+2.0):
        return bt*_betacf(a,b,x)/a
    return 1.0 - bt*_betacf(b,a,1.0-x)/b

def cp_upper(k, n, conf=0.95):
    lo, hi = 0.0, 1.0
    target = conf  # upper: I_p(k+1,n-k)=conf
    for _ in range(200):
        mid = (lo+hi)/2
        if betai(k+1, n-k, mid) < target: lo = mid
        else: hi = mid
    return (lo+hi)/2

print("="*70); print("P00 BRIEF BASELINE FACT-CHECK  (_arch_v19, read-only)"); print("="*70)
head = sh("git","rev-parse","--short","HEAD"); ncommits = sh("git","rev-list","--count","HEAD")
print(f"HEAD={head}  commits={ncommits}")

atoms = count_files("atoms","ATOM-*.md")
ev    = count_files("evidence","EV-*.md")
mis   = len([f for f in os.listdir(os.path.join(ROOT,"misconceptions")) if re.match(r"MIS-.*\.md$",f)])
tools = len([f for f in os.listdir(os.path.join(ROOT,"tools")) if f.endswith(".py")])
ntests= 0
for dp,_,fns in os.walk(os.path.join(ROOT,"tests")):
    ntests += sum(1 for f in fns if f.startswith("test_") and f.endswith(".py"))
print(f"atoms={atoms} (brief 28) | evidence={ev} (brief 57) | MIS={mis} (brief 80)")
print(f"tools_py={tools} (brief 196) | test_files={ntests} (brief 175)")

# ---- gate rules: static parse of register(Rule(...)) calls + severity tables ----
ge = open(os.path.join(ROOT,"tools","gate_engine.py"),encoding="utf-8").read()
rids = re.findall(r'register\(Rule\(\s*"([A-Z0-9\-]+)"', ge)
# fact rules loaded via tuple table around line 3466-3558: collect quoted ids in that block
blk = ge[ge.find("def _register_all"):]
tup_ids = set(re.findall(r'\(\s*"([A-Z]{2,}-[A-Z0-9\-]+)"\s*,', blk))
all_rule_ids = sorted(set(rids) | tup_ids)
sev_override = dict(re.findall(r'"([A-Z]{2,}-[A-Z0-9\-]+)"\s*:\s*"(block|warn|advice)"', ge))
print(f"gate rule ids parsed={len(all_rule_ids)} (brief 63)")
print("severity override table entries:", len(sev_override),
      collections.Counter(sev_override.values()))

# ---- propositions: claim_structured prop ids in atoms ----
nprop = nobs = ninf = 0; prop_no_ev = 0
for dp,_,fns in os.walk(os.path.join(ROOT,"atoms")):
    for fn in fns:
        if not fn.startswith("ATOM-"): continue
        t = open(os.path.join(dp,fn),encoding="utf-8",errors="replace").read()
        for m in re.finditer(r'claim_type:\s*(observation|inference)', t):
            nprop += 1
            if m.group(1)=="observation": nobs += 1
            else: ninf += 1
print(f"propositions claim_type parsed={nprop} (obs={nobs}/inf={ninf})  (brief 79: 50/29)")

# ---- human review ----
hr = [json.loads(l) for l in open(os.path.join(ROOT,"data","human_attack_edge_annotations.jsonl"),encoding="utf-8") if l.strip()]
acts = collections.Counter(r.get("action") for r in hr)
reasons = collections.Counter(r.get("reason","") for r in hr)
batch = sum(1 for r in hr if ("批量" in r.get("reason","") or "授权" in r.get("reason","")))
print(f"human_review rows={len(hr)} actions={dict(acts)} distinct_reasons={len(reasons)} batch_worded={batch}")

# ---- learner twin: zero real-event check ----
ls = [json.loads(l) for l in open(os.path.join(ROOT,"data","learner_state_612.jsonl"),encoding="utf-8") if l.strip()]
kinds = collections.Counter(r.get("kind") for r in ls)
beh_path = os.path.join(ROOT,"data","learner_behavior.jsonl")
beh = [l for l in open(beh_path,encoding="utf-8") if l.strip()]
print(f"learner_state rows={len(ls)} kinds={dict(kinds)} | behavior_events={len(beh)}")

# ---- C-P for the headline escape contract ----
for k,n in [(1,1406),(0,20)]:
    print(f"C-P95 upper(k={k},n={n}) = {cp_upper(k,n)*100:.4f}%")

# ---- severity architecture: warn legacy surface (Goodhart probe pre-signal) ----
print("distinct rule-id prefixes:",
      collections.Counter(i.split("-")[0] for i in all_rule_ids).most_common(12))
print("DONE")
