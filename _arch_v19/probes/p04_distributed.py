# p04_distributed.py (_arch_v19 维度4 分布式验证) 纯标准库只读
# 实验1：盘点仓内"验证者"真实多样性——verified_by/编译器/证据 kind/判决来源。
# 实验2：3 验证者 1 恶意的 BFT 多数表决，在"独立性=实测参数"下与理想独立情形对比。
import os, re, sys, json, collections, random
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def walk(sub,pre):
    o=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,sub)):
        for f in fns:
            if f.startswith(pre) and f.endswith(".md"): o.append(os.path.join(dp,f))
    return o

# --- 验证者身份：原子卡签署人 ---
signers=collections.Counter(); dvs=collections.Counter()
for p in walk("atoms","ATOM-"):
    t=open(p,encoding="utf-8",errors="replace").read()
    m=re.search(r"(?m)^verified_by:\s*(.+)$",t)
    signers[(m.group(1).strip() if m else "(none)")]+=1
    d=re.search(r"(?m)^dal:\s*(\S+)",t)
    dvs[d.group(1) if d else "?"]+=1
# --- 验证者身份：证据卡编译器矩阵 & kind ---
compilers=collections.Counter(); kinds=collections.Counter(); status=collections.Counter()
multi_comp=0; ev_total=0
for p in walk("evidence","EV-"):
    t=open(p,encoding="utf-8",errors="replace").read(); ev_total+=1
    k=re.search(r"(?m)^kind:\s*(\S+)",t);  kinds[k.group(1) if k else "?"]+=1
    s=re.search(r"(?m)^status:\s*(\S+)",t); status[s.group(1) if s else "?"]+=1
    m=re.search(r"compiler:\s*\[([^\]]*)\]",t)
    if m:
        cs=[c.strip() for c in m.group(1).split(",") if c.strip()]
        if len(cs)>1: multi_comp+=1
        for c in cs:
            compilers[re.sub(r"\d.*","",c).split()[0] if c.split() else c]+=1
# --- 人审验证者 ---
hr=[json.loads(l) for l in open(os.path.join(ROOT,"data","human_attack_edge_annotations.jsonl"),encoding="utf-8") if l.strip()]
reviewers=collections.Counter(r["reviewer"] for r in hr)

print("="*72); print("P04 DISTRIBUTED VERIFICATION: real verifier diversity"); print("="*72)
print("原子卡签署人:", dict(signers))
print("DAL 分布:", dict(dvs))
print("证据卡 kind:", dict(kinds))
print("证据卡 status:", dict(status))
print("多编译器矩阵证据卡:", multi_comp, "/", ev_total)
print("编译器家族原始计数(top12):", compilers.most_common(12))
print("人审验证者:", dict(reviewers))

# 独立实现语言/进程：grep verified_by_oracle / machine
oracle_fields=collections.Counter()
for p in walk("atoms","ATOM-"):
    t=open(p,encoding="utf-8",errors="replace").read()
    for k in ("verified_by_oracle","machine_verified","oracle"):
        if re.search(rf"(?m)^{k}:",t): oracle_fields[k]+=1
print("Oracle 字段出现:", dict(oracle_fields))

# --- BFT 模拟：坏命题被多数接受的概率 ---
# 理想独立：每验证者被骗概率 q，3 人中>=2 被骗 = 3q^2(1-q)+q^3
# 相关现实：引入共因 c（同一 python/同一作者语义/同一 LLM 预标注漏斗），
#   以潜变量方式：共因触发(概率c)则3人全错；否则各自独立错 q。
def accept_bad_independent(q): return 3*q*q*(1-q)+q**3
def accept_bad_correlated(q,c):
    return c*1.0 + (1-c)*accept_bad_independent(q)
print("\n3验证者多数表决 接受坏命题概率(单验证者被骗率 q):")
print(f"{'q':>7}{'独立':>10}{'c=0.3':>10}{'c=0.6':>10}{'c=1.0':>10}")
for q in (0.01,0.05,0.14,0.3):
    print(f"{q:>7.2f}{accept_bad_independent(q):>10.4f}"
          f"{accept_bad_correlated(q,.3):>10.4f}{accept_bad_correlated(q,.6):>10.4f}"
          f"{accept_bad_correlated(q,1):>10.4f}")
print("解读：c=共因失败概率。c=0.6 时，3 票多数相对单票几乎无增益；")
print("     仓内 60 programmatic 规则同进程/同语言/同作者 => 理论等效独立票数≈1（v11 实测 9 判官约2票）")
