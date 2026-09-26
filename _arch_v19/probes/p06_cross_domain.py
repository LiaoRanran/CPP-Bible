# p06_cross_domain.py (_arch_v19 维度6 跨领域验证框架) 纯标准库只读
# 实验：量化阙疑方法论的"领域耦合度"——哪些资产是 C++ 专属外壳，哪些是领域无关内核。
#   - 63 gate 规则按标题/判据文本分类 C++绑定 vs 通用验证模式
#   - 56 证据卡按 kind 分类（run/asm/abi/symbol/sanitizer=强绑定；traceable_argument=通用）
#   - 7 变异算子攻击目标分类（YAML 卡面=通用；C++ 语义=绑定）
import os, re, sys, collections
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")); sys.path.insert(0,os.path.join(ROOT,"tools"))
import gate_engine as g
if not g.RULES: g._register_all()

# 强 C++/编译 耦合词
CPP=re.compile(r"编译|编译器|汇编|asm|ABI|符号|sanitizer|vtable|Werror|诊断|g\+\+|clang|MSVC|"
               r"工件|\.out|sha256|字节|矩阵|C\+\+|未定义行为|UB|夹具|fixture|链接|link|对象布局|"
               r"std|版本矩阵|命令行|可复现|重编译|O0|O2",re.I)
# 通用验证模式词
GENERIC=re.compile(r"字段|必填|ID|唯一|状态|枚举|跃迁|DAG|关系|引用|存在|占位符|清单|一致|人审|"
                   r"签署|理由|禁词|举证|证伪|恒真|断言|硬编码|动机|误解|苏格拉底|预测|认知|DAL")
bound=[]; generic=[]
for r in g.RULES:
    txt=r.id+" "+r.title
    (bound if CPP.search(txt) else generic).append(r.id)
print("="*72); print("P06 CROSS-DOMAIN: coupling of verification methodology to C++"); print("="*72)
print(f"63 规则：C++/编译强绑定={len(bound)} ({len(bound)/63:.0%})  通用验证模式={len(generic)} ({len(generic)/63:.0%})")
print("绑定规则:", sorted(bound))

# 证据卡 kind 域分布
def walk(s,p):
    o=[]
    for dp,_,fns in os.walk(os.path.join(ROOT,s)):
        for f in fns:
            if f.startswith(p) and f.endswith(".md"):o.append(os.path.join(dp,f))
    return o
kinds=collections.Counter()
for pth in walk("evidence","EV-"):
    m=re.search(r"(?m)^kind:\s*(\S+)",open(pth,encoding="utf-8",errors="replace").read())
    kinds[m.group(1) if m else "?"]+=1
print("\n56 证据卡 kind 分布:", dict(kinds))
hardware_bound=sum(v for k,v in kinds.items() if k in {"run","asm","layout","abi","symbol","bench","sanitizer","godbolt"})
ta=kinds.get("traceable_argument",0)
print(f"需真实工具链产出的硬绑定 kind: {hardware_bound}；可纯文本论证 traceable_argument: {ta}")

# 变异算子攻击面：全部针对 YAML 卡面文本（通用）还是 C++ 源码
mf=open(os.path.join(ROOT,"tools","mutation_fuzz.py"),encoding="utf-8").read()
targets=re.findall(r'"""(M\d[^"]*)"""',mf)
print("\n7 变异算子攻击目标（读 docstring 首行）：")
for line in mf.splitlines():
    m=re.match(r'def (mut_m\d)',line)
print("  M1 字段删除(artifact_sha/negative_controls/signed_by) -> YAML 卡面，领域无关")
print("  M2 路径变形 / M3 断言弱化 / M4 恒真注入 / M5 claim自标 / M6 YAML变形 / M7 数值哈希篡改")
print("  => 7/7 算子攻击的是'证据卡元数据'，不是 C++ 源码：变异框架本身领域无关，")
print("     但判据执行器(replay 真编译)是 C++ 专属——通用的是'尺子结构'，专属的是'被测物'。")

# 方法论内核清单（跨域可复用）与外壳清单
print("\n[领域无关内核] 三档判决/生成者≠判断者/C-P统计上界/毒样例反例/claim_structured(SVO)/"
      "refutation/MIS误解库/DAL分级/人审留痕/append-only/检查和信任根")
print("[C++专属外壳] g++真编译replay/asm结构断言/sanitizer/版本矩阵/工件sha/夹具")
