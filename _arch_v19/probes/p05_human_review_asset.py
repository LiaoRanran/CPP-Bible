# p05_human_review_asset.py (_arch_v19 维度5 人审即内容) 纯标准库只读
# 实验：把 388 条"人审"当作可复用的判断资产做质量审计：
#   模板化率 / 独立逐条判断数 / 镜像边(错误相关=1) / 抽样外推的统计上界 /
#   理由的证据引用密度 / 时间窗(橡皮图章速度)。
import os, re, json, collections, datetime, math
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 复用 p00 的 C-P
def _betacf(a,b,x,itmax=300,eps=3e-14):
    qab,qap,qam=a+b,a+1.,a-1.; c=1.; d=1.-qab*x/qap
    if abs(d)<1e-30:d=1e-30
    d=1./d; h=d
    for m in range(1,itmax+1):
        m2=2*m
        aa=m*(b-m)*x/((qam+m2)*(a+m2)); d=1.+aa*d
        if abs(d)<1e-30:d=1e-30
        c=1.+aa/c
        if abs(c)<1e-30:c=1e-30
        d=1./d;h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2)); d=1.+aa*d
        if abs(d)<1e-30:d=1e-30
        c=1.+aa/c
        if abs(c)<1e-30:c=1e-30
        d=1./d;de=d*c;h*=de
        if abs(de-1.)<eps:break
    return h
def betai(a,b,x):
    if x<=0:return 0.
    if x>=1:return 1.
    lb=math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)
    bt=math.exp(lb+a*math.log(x)+b*math.log(1.-x))
    if x<(a+1.)/(a+b+2.):return bt*_betacf(a,b,x)/a
    return 1.-bt*_betacf(b,a,1.-x)/b
def cp_upper(k,n,conf=.95):
    lo,hi=0.,1.
    for _ in range(200):
        mid=(lo+hi)/2
        if betai(k+1,n-k,mid)<conf:lo=mid
        else:hi=mid
    return (lo+hi)/2

rows=[json.loads(l) for l in open(os.path.join(ROOT,"data","human_attack_edge_annotations.jsonl"),encoding="utf-8") if l.strip()]
N=len(rows)
tpl=collections.Counter(r["reason"] for r in rows)
mirror=sum(1 for r in rows if "对称边" in r["reason"] or "对称关系" in r["reason"])
sample_extrapolate=sum(1 for r in rows if "抽样" in r["reason"] and "授权" in r["reason"])
# 逐条独立判断：reason 不含"批量/授权/对称对应" 且针对该 edge 具体内容
independent=[r for r in rows if not re.search(r"批量|授权|对称",r["reason"])]
# 理由是否引用具体证据锚（EV-/ATOM-/行号/数据）
with_anchor=sum(1 for r in rows if re.search(r"EV-[A-Z]+-\d+|ATOM-[A-Z]+-[A-Z0-9-]+|prop-\d|实测|标准引用",r["reason"]))
# 时间窗
ts=sorted(datetime.datetime.fromisoformat(r["timestamp"]) for r in rows)
span=(ts[-1]-ts[0]).total_seconds()/60 if len(ts)>1 else 0
# 行动分布
act=collections.Counter(r["action"] for r in rows)
# 抽样 20/20 的统计上界
cp20=cp_upper(0,20)
# 354 approve 的"镜像外推"构成
print("="*72); print("P05 HUMAN REVIEW AS CONTENT: asset-quality audit (n=%d)"%N); print("="*72)
print(f"行动分布={dict(act)}  唯一 reason 模板数={len(tpl)}")
for reason,c in tpl.most_common():
    print(f"  [{c:3d}] {reason[:60]}")
print(f"\n镜像边(对称推断,与种子边错误相关=1): {mirror} ({mirror/N:.1%})")
print(f"抽样外推边(20样本->全批授权):       {sample_extrapolate} ({sample_extrapolate/N:.1%})")
print(f"逐条独立判断(无批量/授权/对称字样): {len(independent)}")
print(f"理由含具体证据/命题锚的记录:        {with_anchor} ({with_anchor/N:.1%})")
print(f"388 条时间跨度: {span:.1f} 分钟  => 若全程手判 {N/max(span,1):.1f} 条/分钟")
print(f"\n抽样宣称准确率 20/20=100% 的 Clopper-Pearson 单侧95%上界 = {cp20:.2%}")
print("=> 20/20 在95%%置信下只能支持错误率上界 %.2f；据此授权 %d 条，期望误标上界≈%.1f 条(独立假设)"
      %(cp20, sample_extrapolate, cp20*sample_extrapolate))
print(f"\n作为训练/学习资产的有效标签估计：")
print(f"  信息论：{N} 标签 / {len(tpl)} 模板 = 平均每模板 {N/len(tpl):.0f} 条；去重后唯一判断信息={len(tpl)} 条")
print(f"  真正承载'人为什么认为这条边成立'的文本: 0 条（模板只记录授权动作，不记录边特定证据）")
print(f"  唯一人工判断者: {set(r['reviewer'] for r in rows)}  (双盲/多主体=0)")
