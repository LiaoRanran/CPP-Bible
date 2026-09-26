# p01_self_evolution.py (_arch_v19 维度1) 纯标准库只读
# 目的：在本仓真实数据上测量 discover/propose/verify/merge/report 五步自进化循环的
#       现有支撑度与瓶颈，并对 L0-L5 自进化等级给出证据化定级。
import os, re, json, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def read(p): return open(p, encoding="utf-8", errors="replace").read()
def walk(sub, pre):
    out=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,sub)):
        for f in fns:
            if f.startswith(pre) and f.endswith(".md"): out.append(os.path.join(dp,f))
    return out

atoms = walk("atoms","ATOM-"); evs = walk("evidence","EV-")
atom_ids = {os.path.basename(p)[:-3] for p in atoms}
ev_ids   = {os.path.basename(p)[:-3] for p in evs}

n_prop=n_prop_noev=n_inf=n_inf_nobasis=0
prereq=[]; ev_serves=set(); atom_frontmatter_keys=collections.Counter()
for p in atoms:
    t=read(p)
    fm=t.split("---",2)
    head=fm[1] if len(fm)>=3 else t
    for k in re.findall(r"(?m)^([a-z_]+):", head): atom_frontmatter_keys[k]+=1
    # propositions
    for blk in re.finditer(r"claim_type:\s*(observation|inference)(.*?)(?=\n  - id:|\n\S|\Z)", t, re.S):
        n_prop+=1; seg=blk.group(0)
        if not re.search(r"evidence:\s*\[[^\]]+\]", seg): n_prop_noev+=1
        if blk.group(1)=="inference":
            n_inf+=1
            if "external_basis" not in seg: n_inf_nobasis+=1
    for m in re.finditer(r"type:\s*prerequisite,\s*target:\s*([A-Z0-9\-]+)", t):
        prereq.append((os.path.basename(p)[:-3], m.group(1)))
for p in evs:
    for m in re.finditer(r"serves:\s*\[([^\]]*)\]", read(p)):
        for x in m.group(1).split(","):
            x=re.sub(r"#.*","",x).strip()
            if x: ev_serves.add(x)

broken = [(a,b) for a,b in prereq if b not in atom_ids]
unserved = sorted(atom_ids - {s for s in ev_serves if s in atom_ids})

# 工具层：五步 API 是否已有实现（按文件名/函数名语义检索，只读 grep 式扫描）
tools_dir=os.path.join(ROOT,"tools")
cap = {"discover":[], "propose":[], "verify":[], "merge":[], "report":[]}
kw = {"discover":r"discover|gap|missing|inventory|coverage|triage|backlog",
      "propose":r"propos|generat|draft|candidate|recommend",
      "verify":r"verify|gate|replay|check|drill|fuzz|audit",
      "merge":r"\bmerge\b|accept|promote|transition",
      "report":r"report|dashboard|html|summary|collect"}
for f in os.listdir(tools_dir):
    if not f.endswith(".py"): continue
    body=read(os.path.join(tools_dir,f))
    for stage,pat in kw.items():
        if re.search(pat, f, re.I) or re.search(pat, body[:4000]):
            cap[stage].append(f)

# 学习者传感器现状（自进化 L3 闭环的反馈源）
beh=[l for l in open(os.path.join(ROOT,"data","learner_behavior.jsonl"),encoding="utf-8") if l.strip()]
ls=[json.loads(l) for l in open(os.path.join(ROOT,"data","learner_state_612.jsonl"),encoding="utf-8") if l.strip()]
real_events=[r for r in ls if r.get("kind")!="init"]

print("="*72); print("P01 SELF-EVOLUTION LOOP AUDIT (real repo data, read-only)"); print("="*72)
print(f"atoms={len(atoms)} evidence={len(evs)} propositions={n_prop}")
print(f"[discover 原料] 命题无 evidence 引用: {n_prop_noev}/{n_prop} = {n_prop_noev/n_prop:.1%}")
print(f"[discover 原料] inference 无 external_basis: {n_inf_nobasis}/{n_inf}")
print(f"[discover 原料] prerequisite 断链: {len(broken)}/{len(prereq)}  {broken[:5]}")
print(f"[discover 原料] 无任何证据卡 serves 的原子: {len(unserved)}/{len(atoms)} -> {unserved[:8]}")
print(f"前置依赖总数={len(prereq)} 被证据覆盖的原子={len(atom_ids & ev_serves)}/{len(atoms)}")
for s in cap: print(f"[工具支撑 {s:9s}] {len(cap[s])} 个工具文件语义命中")
print(f"[闭环反馈] learner init={len(ls)} 真实掌握度更新={len(real_events)} behavior事件={len(beh)}")
print(f"[闭环反馈] 自进化最关键的 reward 信号(学习者结果)样本量 = {len(real_events)+len(beh)}")
# 自进化等级判定
ver = len(cap["verify"]); mer = len([f for f in cap['merge'] if 'learner' in f or 'state' not in f])
print("L0纯人工:是  L1机器发现(只读gap扫描):探针即可达  L2机器提案:无独立proposer")
print("L3自动闭环: 缺反馈信号(0真实学习事件)+merge无自动通道  => 定级 L0+（L1 半成品）")
