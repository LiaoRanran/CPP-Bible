# p03_meta_verification.py (_arch_v19 维度3 元验证) 纯标准库只读
# 实验1：静态正则枚举规则  vs  import 活注册表，量化"读代码能否完整枚举规则"。
# 实验2：用完全独立的第二实现重判 EV-MATRIX-UNBACKED，与 gate_engine 官方判定逐条比对
#        （diverse double implementation 思想；Wheeler DDC/Knight-Leveson 关切）。
# 实验3：tool_integrity 保护集覆盖率——63 条规则的"尺子文件"自身受保护吗。
import os, re, sys, hashlib, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

# ---- 实验1 ----
src=open(os.path.join(ROOT,"tools","gate_engine.py"),encoding="utf-8").read()
static = set(re.findall(r'register\(Rule\(\s*"([A-Z0-9\-]+)"', src))
blk = src[src.find("def _register_all"):]
static |= set(re.findall(r'\(\s*"([A-Z]{2,}-[A-Z0-9\-]+)"\s*,', blk))
import gate_engine as g
if not g.RULES: g._register_all()
live = {r.id for r in g.RULES}
print("="*72); print("P03 META-VERIFICATION"); print("="*72)
print(f"实验1 静态枚举止={len(static)}  活注册表={len(live)}  静态漏掉={sorted(live-static)}")

# ---- 实验2：独立第二实现（不调用任何 gate 函数，自己解析）----
def raw_without_actual(t, strip_sha=False):
    # 删除 actual: 段（到下一个顶层键或 frontmatter 结束）
    b = re.sub(r"(?ms)^actual:.*?(?=^\S|\Z)", "", t)
    if strip_sha:  # 官方经 P12 毒样例攻击后才补的第二剥（见 gate_engine.py:987-999）
        b = re.sub(r"(?m)^artifact_sha256:.*$", "", b)
    return b

def indie_judge(t, strip_sha=False):
    m = re.search(r"compiler:\s*\[([^\]]*)\]", t)
    if not m: return None  # 不适用
    comps=[c.strip().strip("'") for c in m.group(1).split(",") if c.strip()]
    if len(comps)<=1: return None
    body=raw_without_actual(t, strip_sha)
    outs=set(re.findall(r"(?:Examples|build)/[^\s\])]+\.out", body))
    runs=set(re.findall(r"run\s*#(\d+)", body)) | set(re.findall(r"\d{10,}", body))
    notice=bool(re.search(r"::notice::", body)); law=bool(re.search(r"标准条文|M2.*永久边界", body))
    backed=(len(outs)+len(runs)>=2) or (notice and (outs or runs)) or law
    return ("BACKED" if backed else "UNBACKED", len(outs)+len(runs))

off = {f.target.replace("\\","/"): f for f in g.check_evidence_matrix_backed()}
def run_diff(strip_sha):
    agree=disagree=0; rows=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,"evidence")):
        for fn in fns:
            if not fn.startswith("EV-"): continue
            p=os.path.join(dp,fn); t=open(p,encoding="utf-8",errors="replace").read()
            ij=indie_judge(t, strip_sha)
            if ij is None: continue
            rel=os.path.relpath(p,ROOT).replace("\\","/")
            official_hit = rel in off
            indie_hit = ij[0]=="UNBACKED"
            if official_hit==indie_hit: agree+=1
            else: disagree+=1; rows.append((rel,ij))
    return agree,disagree,rows
a1,d1,r1 = run_diff(False)
a2,d2,r2 = run_diff(True)
print(f"实验2a 自然第二实现(只剥actual)：适用卡={a1+d1} 一致={a1} 不一致={d1} 一致率={a1/(a1+d1):.1%}")
for r in r1[:8]: print("    分歧(被误放行):", r[0], r[1])
print(f"实验2b 对齐官方预处理(再剥sha256行)：一致={a2} 不一致={d2} 一致率={a2/max(1,a2+d2):.1%}")
print("   解读：2a 重现了官方 P12 毒样例(2026-09-12)暴露前的漏洞形态——")
print("   64位sha的纯数字片段被当成CI run号锚，多编译器毒卡被结构性放行。")

# ---- 实验3：保护集覆盖 ----
tc=os.path.join(ROOT,"tools",".tool_checksums")
protected=set()
for line in open(tc,encoding="utf-8"):
    line=line.strip()
    m=re.match(r"[0-9a-f]{64}\s+(.+)$",line)
    if m: protected.add(os.path.basename(m.group(1)))
allpy={f for f in os.listdir(os.path.join(ROOT,"tools")) if f.endswith(".py")}
critical={"gate_engine.py","poison_drill.py","mutation_fuzz.py","tool_integrity.py",
          "atom_evidence_replay.py","d5_compile_gate.py","d5_runtime_gate.py",
          "d5_source_integrity.py","attack_edge_generator.py","bkt_solver.py",
          "learner_mastery_update_613.py"}
print(f"实验3 .tool_checksums 保护 {len(protected)} 项；tools 下 {len(allpy)} 个 .py")
print("   关键尺子文件受保护状态:")
for f in sorted(critical):
    print(f"     {'[保护]' if f in protected else '[裸露]'} {f}")
print("   裸露尺子占比 =", f"{len(critical-protected)}/{len(critical)} = {len(critical-protected)/len(critical):.0%}")
# gate 规则全部定义在单文件 = 单点
print(f"   63 条规则 100% 定义于 gate_engine.py 单文件（单实现/单语言/单作者语义假设）")
