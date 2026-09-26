# p02_vdd.py (_arch_v19 维度2 验证驱动生成 VDD) 纯标准库只读
# 实验：把 63 条 gate 规则按"生成时可否作为硬约束"分类：
#   A 类=纯文本/frontmatter 静态可判（生成器可在解码时强制，constrained decoding 可达）
#   B 类=必须真实编译/运行产物才能判（生成者同时是工件生产者 => 结构性可伪造面）
# 再测现有卡 frontmatter 作为"生成模板"的字段密度。
import os, re, sys, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

rules=[]
try:
    import gate_engine as g
    if not g.RULES: g._register_all()
    rules=[(r.id, r.kind, r.quadrant, r.severity, r.scope, r.title) for r in g.RULES]
except Exception as e:
    print("import fallback:", e)

# B 类触发词：裁判依赖真实编译/执行/工件字节/外部过程
EXEC_PAT = re.compile(r"编译|编译器|工件|asm|汇编|werror|诊断|diagnostic|sha|字节|out\b|run_match|"
                      r"sanitizer|symbol|符号|矩阵|matrix|actual|fixture|夹具|命令行|可复现|replay|"
                      r"零诊断|留痕|\.out|CI|版本绑定|诊断编译", re.I)
A_static=[]; B_exec=[]
for rid,kind,judge,sev,scope,title in rules:
    (B_exec if EXEC_PAT.search(rid+" "+title) else A_static).append((rid,judge,sev,scope))

print("="*72); print("P02 VERIFICATION-DRIVEN GENERATION: rules as generation constraints"); print("="*72)
print(f"总规则={len(rules)}  judge分布={collections.Counter(r[2] for r in rules)}")
print(f"kind分布={collections.Counter(r[1] for r in rules)}  scope={collections.Counter(r[4] for r in rules)}")
print(f"A 静态可前置约束(文本/frontmatter)={len(A_static)}")
print(f"B 必须真实执行/工件才能判        ={len(B_exec)}")
for r in B_exec: print("   B:", r[0], "|", r[3], "|", r[2])
print(f"\nVDD 生成时可强制覆盖率 = A/总 = {len(A_static)}/{len(rules)} = {len(A_static)/max(1,len(rules)):.1%}")
# 生成者即工件生产者的伪造面：B 类中 severity 分布（block 才有硬约束力）
print("B 类 severity:", collections.Counter(r[2] for r in B_exec))
print("B 类中非 block(warn/advice)=绕过成本为0的事后规则数:",
      sum(1 for r in B_exec if r[2]!="block"))
# human 裁判规则：生成器无法靠约束满足，必须等人
print("judge=human 的规则(约束再强也需人):", [r[0] for r in rules if r[2]=="human"])
# 现有卡作为生成模板：frontmatter 必填键的实际出现密度（27 卡）
def walk(sub,pre):
    o=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,sub)):
        for f in fns:
            if f.startswith(pre) and f.endswith(".md"): o.append(os.path.join(dp,f))
    return o
required=["id","title","status","verified_by","dal","claim","claim_structured","relations"]
fill=collections.Counter()
for p in walk("atoms","ATOM-"):
    t=open(p,encoding="utf-8",errors="replace").read()
    for k in required:
        if re.search(rf"(?m)^{k}:",t): fill[k]+=1
n=27
print("\n27 原子卡关键字段填充率(生成模板可得约束):")
for k in required: print(f"   {k:18s} {fill[k]}/{n}")
