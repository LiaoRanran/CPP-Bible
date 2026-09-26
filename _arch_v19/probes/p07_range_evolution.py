# p07_range_evolution.py (_arch_v19 维度7 超大规模靶场自进化) 纯标准库只读
# 实验1：静态估算 56 证据卡 × M1-M7 的可变异点总量（不产变体文件，只数模式触发点）。
# 实验2：检索"修复器"是否存在——自进化闭环 discover->verify->? 的最后一环。
# 实验3：10 轮自进化靶场的纯统计模拟（用实测逃逸率与变异点结构），展示质量曲线形态。
import os, re, math, collections
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
def walk(s,p):
    o=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,s)):
        for f in fns:
            if f.startswith(p) and f.endswith(".md"):o.append(os.path.join(dp,f))
    return o
ev=[open(p,encoding="utf-8",errors="replace").read() for p in walk("evidence","EV-")]

# --- 各算子在真实卡上的可触发点数（静态模式计数，上界估计）---
PAT={
 "M1_field_drop": r"(?m)^(artifact_sha256|run_match_file|negative_controls|signed_by):",
 "M3_assert_weaken": r"contains_in|assert_between|-Werror|assert_count",
 "M4_tautology_inject": r"(?m)^artifact_assert:",
 "M5_inference_relabel": r"claim_type:\s*inference",
 "M6_yaml_shape": r"(?m)^id:\s*\S+",
 "M7_sha_or_number": r"(?m)^artifact_sha256:\s*[0-9a-fA-F]{8,}",
}
counts={k:0 for k in PAT}; cards_hit={k:0 for k in PAT}
for t in ev:
    for k,pat in PAT.items():
        n=len(re.findall(pat,t))
        counts[k]+=n
        if n: cards_hit[k]+=1
print("="*72); print("P07 OVERSIZED RANGE: real mutation-surface static estimate"); print("="*72)
print(f"证据卡={len(ev)}（注：M5 作用于原子卡 claim_type，29 inference 已由 p00 核得）")
for k in PAT:
    print(f"  {k:22s} 触发点合计={counts[k]:4d}  命中卡={cards_hit[k]:3d}/{len(ev)}")
total_sites=sum(counts[k] for k in PAT if k!="M5_inference_relabel")+29
print(f"静态可变异点总量(含原子卡29 inference) ≈ {total_sites}")
print(f"对照历史实测：1593 变体/1406 可判/1 逃逸（静态点远少于实跑，因每点多个变形）")

# --- 修复器检索 ---
td=os.path.join(ROOT,"tools")
repair=[]
for f in os.listdir(td):
    if f.endswith(".py"):
        b=open(os.path.join(td,f),encoding="utf-8",errors="replace").read()[:6000]
        if re.search(r"def .*(repair|autofix|auto_fix|heal|synthesize|self_fix)",b,re.I):
            repair.append(f)
regen=[f for f in os.listdir(td) if re.search(r"regen|fix|repair",f,re.I)]
print(f"\n含自动修复/合成语义函数的工具: {repair or '无'}")
print(f"文件名含 regen/fix/repair 的工具: {sorted(regen)[:12]}")

# --- 10 轮自进化模拟 ---
# 假设：每轮系统自己产 S 个变异(取自自己7算子的已知族)，自己验证，自己"修复"。
# 已知族内检测能力 p_det=1-1/1406≈0.99929；但族外新缺陷检测率 q 未知(无独立发现源=>置0假设)。
# 自进化若只在自己算子族内打转，"表观通过率"恒为 p_det；真正缺陷率分母不增加。
import random; random.seed(20260921)
pdet=1-1/1406
print("\n10 轮自进化靶场模拟（每轮500自产变异，族内检测 p=%.5f，族外缺陷不被自产变异触及）"%pdet)
undet=0; tested=0
for rnd in range(1,11):
    for _ in range(500):
        tested+=1
        if random.random()>pdet: undet+=1
    print(f"  round {rnd:2d}: 累计测试={tested:5d} 族内逃逸={undet:3d}  "
          f"表观通过率={1-undet/tested:.5f}  对'真实缺陷率分母'增益=0(自产样本非独立发现源)")
print("结论：曲线平坦且自我强化——靶场越大，对'自己已知攻击族'的信心越高，")
print("      但对未知族零信息；无外部 oracle/真实学习者反馈时，自进化=在自己影子里赛跑。")
