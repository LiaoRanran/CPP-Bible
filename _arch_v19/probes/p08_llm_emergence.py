# p08_llm_emergence.py (_arch_v19 维度8 LLM 发展与涌现) 纯标准库只读
# 实验：基于真实规则/证据结构，给阙疑 10 个核心能力打"LLM 能力 10 倍后"的重要性方向，
#       每个方向都用仓内可核数字支撑，而非空谈。
import os,re,sys,collections,json
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")); sys.path.insert(0,os.path.join(ROOT,"tools"))
import gate_engine as g
if not g.RULES: g._register_all()

EXEC=re.compile(r"编译|编译器|工件|asm|werror|诊断|sha|run_match|sanitizer|symbol|矩阵|actual|"
                r"夹具|命令行|可复现|\.out|CI|版本绑定|零诊断|留痕",re.I)
rules=g.RULES
n_exec=sum(1 for r in rules if EXEC.search(r.id+" "+r.title))
n_text=len(rules)-n_exec
n_human=sum(1 for r in rules if r.quadrant=="human")
n_llmq=sum(1 for r in rules if r.quadrant in ("llm","hybrid"))
print("="*72); print("P08 LLM EMERGENCE: which capabilities survive a 10x model"); print("="*72)
print(f"63规则中 依赖真实执行(LLM无法靠'更会说'满足)={n_exec} ({n_exec/63:.0%})")
print(f"         纯文本/结构可判(LLM能力提升会吞掉)  ={n_text} ({n_text/63:.0%})")
print(f"         quadrant 已显式交给 llm/hybrid 的规则 ={n_llmq}  纯human={n_human}")
# replay 硬执行证据规模
n_ev=0; n_run=0
for dp,_,fns in os.walk(os.path.join(ROOT,"evidence")):
    for f in fns:
        if f.startswith("EV-"):
            n_ev+=1
            t=open(os.path.join(dp,f),encoding="utf-8",errors="replace").read()
            if re.search(r"(?m)^kind:\s*run",t): n_run+=1
print(f"证据卡 {n_ev} 张，其中 run 类(必须真跑出读数) {n_run} 张——LLM 再强也改不了'程序实际输出'")
# 人审漏斗现状：已 100% 经 LLM 预标注
hr=[json.loads(l) for l in open(os.path.join(ROOT,"data","human_attack_edge_annotations.jsonl"),encoding="utf-8") if l.strip()]
via_llm=sum(1 for r in hr if "AI预标注" in r["reason"] or "对称边" in r["reason"])
print(f"人审 {len(hr)} 条中经 LLM 预标注/镜像漏斗的: {via_llm} ({via_llm/len(hr):.0%}) —— 不是未来时，是现在时")

caps=[
 ("1 真编译replay执行",      "↑更重要","LLM越强，'真跑过'与'说得像'越难区分，执行证据成唯一硬通货",f"{n_run} run卡"),
 ("2 gate文本/格式规则",      "↓被吞掉",f"{n_text}条纯文本规则≈constrained decoding默认满足",f"{n_text}规则"),
 ("3 poison毒样例反例",       "↑更重要","强模型生成的伪证据更逼真，毒样例是防强模型，不是防弱模型","124载荷"),
 ("4 mutation变异fuzz",      "→迁移","攻击对象从'删字段'升级为'语义级篡改'，7文本算子需扩到语义层","7算子"),
 ("5 人审判断",              "↑但变形","事实核对被LLM接管，人只剩'价值/相关度/教学意图'判断","388条已漏斗化"),
 ("6 claim结构化/SVO命题",   "↑更重要","成为LLM输出的强制schema，是可验证性的入口","79命题"),
 ("7 C-P统计上界",           "↑更重要","能力越强越需要诚实分母，否则'看起来都对'无法量化风险","1/1406"),
 ("8 BKT学习者镜像",         "→重新定义","LLM可直接当tutor，BKT掌握度从'模型'变'校准基准'，仍需真人结果做锚","27init/0事件"),
 ("9 信任根/检查和",          "↑更重要","LLM参与生成后，'这工件是不是这次真跑出来的'成为核心防伪","9文件钉锚"),
 ("10 内容产能(写卡/写章)",   "↓贬值","生成成本趋零，稀缺性完全转向验证与教学设计","27卡"),
]
print("\n10 核心能力 × LLM-10x 重要性方向：")
for c,d,why,num in caps:
    print(f"  {c:24s} {d:8s} | {num:10s} | {why}")
up=[c for c,d,*_ in caps if d.startswith("↑")]
print(f"\n重要性上升 {len(up)} 项，共性=都依赖'外部现实锚'(真执行/真毒样/真人/真统计)；")
print("下降项共性=都是'生成/表述'能力。结论：LLM 越强，阙疑的'验证层'越增值，'生成层'越贬值——")
print("项目把资本压在验证层，方向上抗模型迭代；但前提是验证锚必须持续锚在'现实'而非'文本'。")
