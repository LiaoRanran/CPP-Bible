"""629 A3 · 自身免疫率仪表盘（纯标准库，自包含 HTML，无外部依赖）

左侧：逃逸率（漏报）· 中间：混淆矩阵 · 右侧：自身免疫率（误报）· 底部：v22 调研引述。

数据来源：A1 `autoimmune_rate_framework`（自身免疫率 + 分桶）、
A2 `autoimmune_probe_629`（格式过敏率 + 混淆矩阵）、§一 standing baseline（逃逸率/poison）。

`--check` **只读**：校验 HTML 已存在、非空、含 4 个模块与深色科技风标记，并核对
A1 实测自身免疫率与页面内嵌值一致（不重新生成，不写盘）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_HTML = os.path.join(ROOT, "data", "autoimmune_dashboard_629.html")

ESCAPE = {"hits": 1, "total": 1406, "cs_upper": 0.9062}
POISON = "124/124（诚实覆盖率 95.5%）"

CSS = """
:root{--bg:#0a0e1a;--panel:rgba(20,28,48,.62);--line:rgba(90,130,200,.22);
--txt:#c9d4ee;--dim:#7c89a8;--cyan:#3ad6c5;--violet:#8b6cff;--rose:#ff4d6d;--amber:#ffb020}
*{box-sizing:border-box}
body{margin:0;background:
 radial-gradient(1100px 620px at 12% -8%,rgba(58,214,197,.13),transparent 60%),
 radial-gradient(900px 560px at 92% 8%,rgba(139,108,255,.14),transparent 60%),var(--bg);
 color:var(--txt);font:15px/1.62 "Segoe UI","Microsoft YaHei",system-ui,sans-serif;min-height:100vh}
.wrap{max-width:1180px;margin:0 auto;padding:40px 22px 64px}
h1{margin:0 0 6px;font-size:30px;letter-spacing:.4px}
h1 span{color:var(--cyan)}
.sub{color:var(--dim);font-size:13px;margin-bottom:26px}
h2{margin:0 0 14px;font-size:15px;letter-spacing:.3px;color:#dfe8ff;font-weight:600}
h2 em{color:var(--dim);font-style:normal;font-size:12px;margin-left:8px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 22px;
 backdrop-filter:blur(10px);box-shadow:0 10px 30px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.04);
 margin-bottom:20px}
.cols{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:20px}
@media(max-width:980px){.cols{grid-template-columns:1fr}}
.big{font-size:44px;font-weight:700;line-height:1.05;letter-spacing:-.5px}
.big.c{color:var(--cyan)}.big.r{color:var(--rose)}.big.a{color:var(--amber)}
.unit{font-size:15px;color:var(--dim);font-weight:500;margin-left:4px}
.kv{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-bottom:1px dashed rgba(90,130,200,.16);font-size:13px}
.kv:last-child{border-bottom:0}
.kv b{color:#e6edff;font-weight:600}
.kv span{color:var(--dim)}
.bar{height:11px;border-radius:7px;background:rgba(90,130,200,.16);overflow:hidden;margin:9px 0 4px}
.bar i{display:block;height:100%;border-radius:7px}
.bar i.c{background:linear-gradient(90deg,#2fb9ab,#3ad6c5)}
.bar i.r{background:linear-gradient(90deg,#ff7b93,#ff4d6d)}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;color:var(--dim);margin-top:8px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:1px}
.mx{display:grid;grid-template-columns:88px 1fr 1fr;grid-gap:9px;align-items:stretch}
.mx .h{font-size:12px;color:var(--dim);display:flex;align-items:center;justify-content:center;text-align:center}
.mx .cell{border:1px solid var(--line);border-radius:12px;padding:13px 12px;text-align:center;background:rgba(12,18,34,.5)}
.mx .cell .n{font-size:26px;font-weight:700}
.mx .cell .t{font-size:11px;color:var(--dim);margin-top:3px}
.mx .tn .n{color:var(--cyan)}.mx .tp .n{color:var(--violet)}
.mx .fp .n{color:var(--rose)}.mx .fn .n{color:var(--amber)}
.note{font-size:12px;color:var(--dim);margin-top:10px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.chip{border:1px solid var(--line);border-radius:999px;padding:4px 11px;font-size:12px;color:#cfd9f2}
.chip.rose{border-color:rgba(255,77,109,.45);color:#ffb9c6}
.chip.cyan{border-color:rgba(58,214,197,.45);color:#a9f0e7}
blockquote{margin:0;padding:14px 18px;border-left:3px solid var(--violet);background:rgba(139,108,255,.07);
 border-radius:0 12px 12px 0;color:#cfd9f2;font-size:13.5px}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px}
th,td{padding:8px 10px;border-bottom:1px solid rgba(90,130,200,.16);text-align:left}
th{color:var(--dim);font-weight:600}
code{background:rgba(90,130,200,.14);padding:1px 6px;border-radius:6px;font-size:12.5px}
.foot{color:var(--dim);font-size:12px;text-align:center;margin-top:26px}
"""


def _pct(x: float, digits: int = 2) -> str:
    return f"{x * 100:.{digits}f}%"


def collect() -> dict[str, Any]:
    """只读采集 A1/A2 数字（供页面与 --check 共用）。"""
    import autoimmune_probe_629 as P
    import autoimmune_rate_framework as A

    m = A.measure()
    probe = P.measure()
    return {"a": {k: v for k, v in m.items() if k != "cards"},
            "probe": {k: v for k, v in probe.items() if k != "rows"},
            "cards": m["cards"], "rows": probe["rows"]}


def _card_escape() -> str:
    rate = ESCAPE["hits"] / ESCAPE["total"]
    return f"""<div class="card"><h2>① 逃逸率 <em>漏报 · 坏卡通过 gate</em></h2>
<div class="big c">{_pct(rate, 3)}<span class="unit">（{ESCAPE['hits']}/{ESCAPE['total']}）</span></div>
<div class="bar"><i class="c" style="width:{max(rate * 100, 0.4):.2f}%"></i></div>
<div class="kv"><span>采样规模</span><b>{ESCAPE['total']} 条 mutation</b></div>
<div class="kv"><span>CS anytime 上界</span><b>{ESCAPE['cs_upper']}%</b></div>
<div class="kv"><span>毒样例拦截（真阳性）</span><b>{POISON}</b></div>
<div class="note">逃逸率低说明 gate 在「拦坏卡」方向几乎无漏；但**低逃逸率不等于 gate 合格**——
还要看它误杀多不多（右侧）。</div></div>"""


def _card_auto(d: dict[str, Any]) -> str:
    a, probe = d["a"], d["probe"]
    return f"""<div class="card"><h2>③ 自身免疫率 <em>误报 · 好卡被 gate warn/block</em></h2>
<div class="big r">{_pct(a['rate'], 1)}<span class="unit">（{a['warned_count']}/{a['total']} 张已验证卡）</span></div>
<div class="bar"><i class="r" style="width:{max(a['rate'] * 100, 0.4):.2f}%"></i></div>
<div class="kv"><span>硬缺陷（真阳性嫌疑）</span><b>{len(a['hard_defect_cards'])} 张</b></div>
<div class="kv"><span>仅命题级口径（自身免疫嫌疑）</span><b>{len(a['caliber_only_cards'])} 张</b></div>
<div class="kv"><span>格式过敏率（A2 探针）</span><b>{_pct(probe['false_positive_rate'], 1)}（{len(probe['fp_events'])}/{probe['measured']}）</b></div>
<div class="chips"><span class="chip rose">口径错配 = 主因</span><span class="chip cyan">非格式问题</span>
<span class="chip">block = {a['block_count']}</span></div>
<div class="note">warn 语义是「记债」而非阻断；100% 说明该层目前**不能当质量评级**，
只能当 TODO 债清单。</div></div>"""


def _matrix(d: dict[str, Any]) -> str:
    probe = d["probe"]
    fp = len(probe["fp_events"])
    return f"""<div class="card"><h2>② 混淆矩阵 <em>两个错误方向同时看</em></h2>
<div class="mx">
 <div class="h"></div><div class="h">判定为「有问题」</div><div class="h">判定为「没问题」</div>
 <div class="h">实际有问题</div>
 <div class="cell tp"><div class="n">124</div><div class="t">真阳性 TP · 毒样例被 block</div></div>
 <div class="cell fn"><div class="n">1</div><div class="t">假阴性 FN · 逃逸（漏报）</div></div>
 <div class="h">实际没问题</div>
 <div class="cell fp"><div class="n">{fp}</div><div class="t">假阳性 FP · 格式微扰被 warn（自身免疫）</div></div>
 <div class="cell tn"><div class="n">✅</div><div class="t">真阴性 TN · 阴性对照成立（{probe['measured']} 次扰动）</div></div>
</div>
<div class="note">TP/FN 引用 §一 standing baseline（poison 与逃逸率）；FP/TN 为 A2 实测（镜像沙箱 + 语义等价格式微扰）。
两侧错误**极不对称**：漏报 0.07% vs 误报 100%（口径层）——gate 的设计取舍是「宁枉勿纵」，必须显式承认。</div>
<div class="legend"><span><span class="dot" style="background:var(--violet)"></span>TP</span>
<span><span class="dot" style="background:var(--amber)"></span>FN</span>
<span><span class="dot" style="background:var(--rose)"></span>FP</span>
<span><span class="dot" style="background:var(--cyan)"></span>TN</span></div></div>"""


def _rules_table(d: dict[str, Any]) -> str:
    rows = "".join(f"<tr><td><code>{r}</code></td><td>{n}</td></tr>"
                   for r, n in d["a"]["rules"])
    return f"""<div class="card"><h2>④ 自身免疫事件来自哪些规则 <em>A1 实测 warn 分布</em></h2>
<table><tr><th>规则 ID</th><th>warn 次数（23 张已验证卡）</th></tr>{rows}</table>
<div class="note">三条规则都是**命题级要求**（命题级 liveness / 规范概念短语 / 命题级机器验证），
而 27 张老卡只有**卡级**元数据 ⇒ 命中是口径错配的必然结果，不是内容错误。</div></div>"""


def _page(d: dict[str, Any]) -> str:
    a, probe = d["a"], d["probe"]
    return "\n".join([
        "<!doctype html>", '<html lang="zh-CN"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>自身免疫率 × 逃逸率 仪表盘 · 629 A3</title>",
        f"<style>{CSS}</style></head><body><div class=\"wrap\">",
        "<h1>自身免疫率 <span>×</span> 逃逸率</h1>",
        f'<div class="sub">629 A 线 · 深色科技风 · 纯内联 CSS 自包含（无 CDN/无外部依赖）· '
        f'数据：A1 自身免疫率框架（{a["total"]} 张已验证卡）+ A2 误报注入探针'
        f'（{probe["measured"]} 次有效扰动）</div>',
        '<div class="cols">', _card_escape(), _matrix(d), _card_auto(d), "</div>",
        _rules_table(d),
        '<div class="card"><h2>⑤ v22 调研引述：免疫系统的双层耐受 <em>为什么自身免疫率是范式输入</em></h2>',
        "<blockquote>免疫系统靠<b>中枢耐受</b>（胸腺里先删掉攻击自身的 T 细胞）与<b>外周耐受</b>"
        "（调节性 T 细胞 + 无共刺激信号不激活）双层机制，避免攻击自身组织；"
        "一旦失衡就是<b>自身免疫病</b>（误杀好细胞）。<br><br>"
        "阙疑对应物：中枢耐受 ≈ 写入侧 schema/gate 前置校验（不合格的卡进不来）；"
        "外周耐受 ≈ 运行侧 warn/advice 分级（先记债不动手）；"
        "<b>自身免疫率</b>就是这套双层机制的副作用指标——v18–v21 四轮调研只盯逃逸率（漏放坏卡），"
        "从未度量误杀好卡，本批首次补上。</blockquote>",
        f'<div class="kv"><span>本批实测（A1）</span><b>自身免疫率 {_pct(a["rate"], 1)}'
        f'（{a["warned_count"]}/{a["total"]}）· 分桶：硬缺陷 {len(a["hard_defect_cards"])} + '
        f'命题级口径 {len(a["caliber_only_cards"])}</b></div>',
        f'<div class="kv"><span>本批实测（A2）</span><b>格式过敏率 {_pct(probe["false_positive_rate"], 1)}'
        f'（{len(probe["fp_events"])}/{probe["measured"]}）</b></div>',
        '<div class="kv"><span>需人审裁决</span><b>命题级字段：新卡必需、老卡豁免？还是老卡补齐？</b></div>',
        '<div class="note">本页只展示度量结果，不代替任何人审裁决；warn 不阻断、block 才阻断。</div></div>',
        '<div class="foot">由 <code>tools/autoimmune_dashboard_629.py</code> 生成 · '
        '只读数据源：atoms/ + evidence/ + §一 standing baseline · 不含任何外部资源</div>',
        "</div></body></html>",
    ])


def generate() -> str:
    html = _page(collect())
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return html


MODULES = ("① 逃逸率", "② 混淆矩阵", "③ 自身免疫率", "④ 自身免疫事件来自哪些规则",
           "⑤ v22 调研引述")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("HTML 文件已存在（--check 不生成、只校验）", os.path.exists(OUT_HTML))
    if not os.path.exists(OUT_HTML):
        print("A3 autoimmune dashboard check: FAIL")
        return 1
    html = open(OUT_HTML, encoding="utf-8").read()
    chk("HTML 非空且体量合理", len(html) > 6000, f"({len(html)} bytes)")
    chk("含 5 个模块", all(k in html for k in MODULES),
        f"({[k for k in MODULES if k not in html]})")
    chk("深色科技风样式在位", all(k in html for k in
                             ("--bg:#0a0e1a", "backdrop-filter", "radial-gradient",
                              "--cyan", "--rose", "--amber")))
    chk("自包含：无外部资源引用", not re.search(r'(src|href)\s*=\s*["\']https?://', html))
    chk("左侧含逃逸率 1/1406 与 CS 上界", "1/1406" in html or "0.071%" in html)
    chk("中间含混淆矩阵四格", all(k in html for k in ("真阳性", "假阴性", "假阳性", "真阴性")))
    chk("右侧含 A2 格式过敏率", "格式过敏率" in html)
    chk("底部含 v22 引述", "中枢耐受" in html and "外周耐受" in html)
    import autoimmune_rate_framework as A

    live = A.measure()
    chk("页面内嵌自身免疫率与 A1 实测一致",
        f"{live['rate'] * 100:.1f}%" in html, f"({live['rate'] * 100:.1f}%)")
    chk("页面内嵌干净卡总数与实测一致",
        f"（{live['warned_count']}/{live['total']}）" in html)
    print(f"A3 autoimmune dashboard check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 A3 自身免疫率仪表盘")
    ap.add_argument("--check", action="store_true", help="只读自检（不生成）")
    ap.add_argument("--json", action="store_true", help="打印采集数字")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.json:
        d = collect()
        print(json.dumps({"a": {k: v for k, v in d["a"].items()},
                          "probe": d["probe"]}, ensure_ascii=False, indent=2,
                         default=str))
        return 0
    html = generate()
    print(f"written {OUT_HTML} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
