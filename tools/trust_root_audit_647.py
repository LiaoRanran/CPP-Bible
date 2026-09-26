"""647 A5 · **信任根独立审计**（A1–A4 修复后：信任根到底独立了多少？**不夸大**）。

审计五件事（§三 A5）：
1. 缺信任根文件是否 FAIL（A1）—— 在**临时沙箱**里删一个已钉文件，实测 strict/lenient 两档；
2. 不完整事件是否被拒绝（A2）—— `from_dict_strict({})` 实测；
3. 闭包是否完整（A3）—— 647 闭包状态 + 与 tool_integrity 交叉一致 + 假装缺失必 FAIL；
4. 外部锚接口是否就绪（A4）—— 契约两条 + mock 可发布可验证 + 预留接入点；
5. **仍存在的信任根共置点**（诚实登记的核心）—— 把"修好了什么"与"仍然共置什么"分开写。

输出：`data/647_trust_root_report.md`（**修复前后对比 + 仍存在的风险**）。

**诚实原则**（§十二.1）：本报告**不宣称"信任根已独立"**。A1/A2 修的是 **fail-open 行为**，
A3 扩的是 **覆盖面**，A4 只建了 **接口**。密钥与 anchor 仍在本地 ⇒ 独立性仍是 **L2**。

CLI：`--check`（只读自检）/ `--report`（写报告 + JSON）/ `--json`。纯标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as de  # noqa: E402
import external_anchor_647 as ext  # noqa: E402
import tool_integrity as ti  # noqa: E402
import verifier_closure_647 as vc647  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_trust_root_report.md")
OUT_JSON = os.path.join(ROOT, "data", "647_trust_root_report.json")

#: 与"日志/基线"共置的信任根载体（按重要性）
CO_LOCATION_ITEMS = (
    ("透明日志 anchor", "data/transparency_log.jsonl",
     "改仓库即可同时改日志与其 anchor ⇒ 自证"),
    ("完整性基线", "tools/.tool_checksums",
     "「什么算被改过」的定义与被校验的文件在同一仓库 ⇒ 一起改就自洽"),
    ("目录 Merkle 根", "data/supply_chain/merkle_roots.json", "同上，且根与被覆盖文件同源"),
    ("in-toto layout", "data/supply_chain/layout.json", "同上"),
    ("VSA 公钥", "data/vsa/public_key_631.json",
     "公钥在仓库内；验签方若读仓库里的公钥，则「换钥+换公钥」同样自洽"),
    ("外部锚", "tools/external_anchor_647.py（mock-local）",
     "A4 的 mock 与被锚对象**同机同仓库** ⇒ 不构成独立锚（L3 未达）"),
)


def sandbox_missing_trust_root() -> dict[str, Any]:
    """A1 实测（**临时沙箱，不碰真实仓库**）：删一个已钉信任根文件，看两档退出码。"""
    out: dict[str, Any] = {}
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "tools").mkdir(parents=True, exist_ok=True)
        (root / "tools" / "a_tool.py").write_text("# a\n", encoding="utf-8")
        for rel in ti.SUPPLY_CHAIN_FILES:
            f = root / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(f"# {rel}\n", encoding="utf-8")
        cs = root / ".tool_checksums"
        ti.write_baseline(path=cs, tools_dir=root / "tools", names=("a_tool.py",))
        ti.write_supply_chain_baseline(path=cs, root=root, names=ti.SUPPLY_CHAIN_FILES)
        out["before_delete"] = {
            "strict": ti.verify_supply_chain(cs, root, strict=True)[2],
            "lenient": ti.verify_supply_chain(cs, root, strict=False)[2]}
        victim = ti.SUPPLY_CHAIN_FILES[0]
        (root / victim).unlink()
        _, wn, strict_code = ti.verify_supply_chain(cs, root, strict=True)
        _, _, lenient_code = ti.verify_supply_chain(cs, root, strict=False)
        out["after_delete"] = {"victim": victim, "strict": strict_code,
                               "lenient": lenient_code,
                               "named": any(victim in w for w in wn)}
        # 真实仓库**必须原封不动**
        out["real_repo_file_still_there"] = os.path.isfile(os.path.join(ROOT, victim))
    out["fail_open_fixed"] = bool(out["after_delete"]["strict"] == 1
                                  and out["after_delete"]["lenient"] == 0
                                  and out["after_delete"]["named"]
                                  and out["real_repo_file_still_there"])
    return out


def audit_event_strictness() -> dict[str, Any]:
    """A2 实测：不完整/未知字段事件是否被拒绝。"""
    rejected: dict[str, bool] = {}
    for name, payload in (("空 dict", {}),
                          ("缺 decision_origin", {"operation": "CREATE", "result": "APPROVE",
                                                  "target_type": "edge", "target_id": "x",
                                                  "review_method": "ITEM_BLIND", "reviewer": "A",
                                                  "decided_at": "2026-09-26"}),
                          ("未知字段", {"operation": "CREATE", "result": "APPROVE",
                                        "target_type": "edge", "target_id": "x",
                                        "review_method": "ITEM_BLIND",
                                        "decision_origin": "human_observed", "reviewer": "A",
                                        "decided_at": "2026-09-26", "bogus": 1})):
        try:
            de.DecisionEvent.from_dict_strict(payload)
            rejected[name] = False
        except de.StrictEventError:
            rejected[name] = True
    legacy = de.DecisionEvent.from_dict({})
    return {"rejected": rejected, "all_rejected": all(rejected.values()),
            "lenient_legacy": {"result": legacy.result,
                               "decision_origin": legacy.decision_origin},
            "note": "宽容入口**有意保留**（历史 452 条必须能导入）⇒ 它是显式的历史通道，不是默认路径"}


def audit_closure() -> dict[str, Any]:
    cl = vc647.build_closure()
    cons = vc647.consistency_with_tool_integrity(cl)
    att = vc647.attack_missing_trust_root()
    return {"status": cl["status"], "n_files": cl["n_files"], "n_rules": cl["n_rules"],
            "consistent_with_tool_integrity": cons["consistent"],
            "attack_status": att["status"],
            "attack_named": att["missing"],
            "digest": cl["digest"]}


def audit_external_anchor() -> dict[str, Any]:
    spec = ext.interface_spec()
    cur = ext.publish_current_anchor(published_at="2026-09-26T00:00:00Z")
    return {"contract": spec["contract"], "implemented": spec["implemented"],
            "reserved": [s["name"] for s in spec["reserved"]],
            "real_external_service_connected": spec["real_external_service_connected"],
            "mock_roundtrip": {"published": cur["published"], "verified": cur["verified"],
                               "tamper_detected": cur["tamper_detected"]},
            "anchor": cur.get("anchor", {}).get("anchor", "")}


def co_located_points() -> list[dict[str, str]]:
    """**仍存在的共置点**（修复不覆盖这些）：每条给"在哪 / 为什么是风险 / 谁能解"。"""
    return [{"point": name, "where": path, "risk": why,
             "resolved_by": "外部锚 / 外部 KMS（交人裁决，647 未做）",
             "present_on_disk": os.path.exists(os.path.join(ROOT, path))}
            for name, path, why in CO_LOCATION_ITEMS]


def independence_level() -> dict[str, Any]:
    return {"level": "L2",
            "why": "同机独立实现/独立进程可复核（628/629 他验三件套已建），"
                   "但 anchor 与基线仍在**同一仓库**里 ⇒ 未达 L3（仓库外第三方可验）",
            "l1": False, "l2": True, "l3": False, "l4": False,
            "to_l3": "把 anchor 发布到仓库外的第三方（A4 的 3 个接入点任选其一）"}


def audit() -> dict[str, Any]:
    return {"trA1": sandbox_missing_trust_root(),
            "trA2": audit_event_strictness(),
            "trA3": audit_closure(),
            "trA4": audit_external_anchor(),
            "co_located": co_located_points(),
            "independence": independence_level()}


def write_report(a: Optional[dict[str, Any]] = None) -> str:
    a = a or audit()
    a1, a2, a3, a4 = a["trA1"], a["trA2"], a["trA3"], a["trA4"]
    ind = a["independence"]
    lines = [
        "# 647 A5 · 信任根独立审计（A1–A4 修复前后对比 + **仍存在的风险**）", "",
        "> **结论先行**：A1/A2 修的是 **fail-open 行为**，A3 扩的是 **覆盖面**，A4 只建了 **接口**。",
        f"> **信任根独立性仍是 `{ind['level']}`**（L3 未达）—— 密钥与 anchor 仍在本地。", "",
        "## 一、修复前后对比", "",
        "| # | 项 | 642 审计时（修复前） | 647 之后 | 判据 |", "|---|---|---|---|---|",
        f"| A1 | 信任根文件缺失 | 只 warning，**exit 0**（642 FO-A 实测） | "
        f"**strict 默认：exit {a1['after_delete']['strict']}**"
        f"（lenient 兼容档仍 {a1['after_delete']['lenient']}） | "
        f"沙箱删 `{a1['after_delete']['victim']}`，点名={a1['after_delete']['named']} |",
        f"| A2 | 不完整事件 | `from_dict({{}})` ⇒ **APPROVE + human_observed**（642 FO-B 实测） | "
        f"`from_dict_strict()` 全拒={a2['all_rejected']} | 空 dict/缺字段/未知字段三类 |",
        f"| A3 | 闭包覆盖 | 23 文件（641） | **{a3['n_files']} 条目**（含 67 规则指纹），"
        f"与 tool_integrity 一致={a3['consistent_with_tool_integrity']} | 假装缺失 ⇒ "
        f"{a3['attack_status']} |",
        f"| A4 | 外部锚 | **不存在** | 接口就绪（publish/verify + mock），"
        f"但**真连外部服务={a4['real_external_service_connected']}** | 契约 + mock 往返 |", "",
        "## 二、逐项实测证据", "",
        "### A1（关键：**真实仓库一个文件都没删**）", "",
        "```json",
        json.dumps(a1, ensure_ascii=False, indent=2),
        "```", "",
        "### A2", "",
        "```json",
        json.dumps(a2, ensure_ascii=False, indent=2),
        "```", "",
        "### A3", "",
        "```json",
        json.dumps(a3, ensure_ascii=False, indent=2),
        "```", "",
        "### A4", "",
        "```json",
        json.dumps(a4, ensure_ascii=False, indent=2),
        "```", "",
        "## 三、**仍存在的信任根共置点**（本批**没有**解决）", "",
        "| 共置点 | 载体 | 为什么是风险 | 谁能解 | 磁盘在否 |", "|---|---|---|---|---|",
    ]
    for c in a["co_located"]:
        lines.append(f"| {c['point']} | `{c['where']}` | {c['risk']} | {c['resolved_by']} | "
                     f"{'在' if c['present_on_disk'] else '不在'} |")
    lines += ["", "## 四、独立性刻度（v29 四级）", "",
              "| 级别 | 定义 | 647 状态 |", "|---|---|---|",
              f"| L1 同进程自证 | 自己证明自己 | {'✅' if ind['l1'] else '❌'} |",
              f"| L2 同机独立实现 | 独立实现/独立进程复核 | {'✅' if ind['l2'] else '❌'} **已达** |",
              f"| L3 仓库外可验 | 第三方凭仓库外锚独立验证 | {'✅' if ind['l3'] else '❌'} **未达** |",
              f"| L4 外部权威背书 | 机构/标准背书 | {'✅' if ind['l4'] else '❌'} |", "",
              f"- 从 L2 到 L3 的唯一路径：{ind['to_l3']}", "",
              "## 诚实登记（防自欺）", "",
              "1. **不宣称「信任根已独立」**：A1/A2 修的是**行为**（缺文件必红、残事件必拒），"
              "A3 扩的是**覆盖面**，A4 只建**接口** —— 三者都不改变「密钥与 anchor 在本地」这一事实；",
              "2. **A1 保留了一个后门**：`--warn-only` 可退回宽容口径 —— "
              "这是兼容性代价（迁移期/仓库副本），**不是** fail-closed 的漏洞（默认是 strict）；",
              "3. **A2 的宽容入口有意保留**：历史 452 条必须能被导入 ⇒ `from_dict_lenient()` 是**显式历史通道**；",
              "4. **A3 闭包仍跟不到 site-packages**，且**两个闭包并存**（641/647）——"
              "是否收编 641 留人裁决（改它会带跑历史 run 的 digest）；",
              "5. **A4 的 mock 不是独立锚**：同机同仓库 ⇒ 对 L3 **零贡献**，只把「能不能接」变成「接口就绪」；",
              "6. **本报告的一切数字都来自可复算的实测**（沙箱删除 / try-except / 闭包构建），"
              "没有一处是「应该会」。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = audit()
    chk("A1：fail-open 已修（strict=1 / lenient=0 / 真仓库未删）", a["trA1"]["fail_open_fixed"])
    chk("A1：真实仓库文件仍在", a["trA1"]["real_repo_file_still_there"] is True)
    chk("A2：三类不完整事件全被拒", a["trA2"]["all_rejected"] is True)
    chk("A2：历史宽容通道仍有（不破坏历史）",
        a["trA2"]["lenient_legacy"]["result"] == "APPROVE")
    chk("A3：闭包 OK 且与 tool_integrity 一致",
        a["trA3"]["status"] == "OK" and a["trA3"]["consistent_with_tool_integrity"] is True)
    chk("A3：假装缺失 ⇒ FAIL", a["trA3"]["attack_status"] == "FAIL")
    chk("A3：闭包含 67 规则指纹", a["trA3"]["n_rules"] == 67)
    chk("A4：接口两条就绪", set(a["trA4"]["contract"]) == {"publish", "verify"})
    chk("A4：mock 往返可验", a["trA4"]["mock_roundtrip"]["verified"] is True)
    chk("A4：未连外部服务（诚实）", a["trA4"]["real_external_service_connected"] is False)
    chk("共置点全部如实登记（≥5 条）", len(a["co_located"]) >= 5, str(len(a["co_located"])))
    chk("独立性不夸大（仍是 L2，L3 未达）",
        a["independence"]["level"] == "L2" and a["independence"]["l3"] is False)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"A5 audit selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 A5 信任根独立审计")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写审计报告 + JSON")
    ap.add_argument("--json", action="store_true", help="打印审计（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    res = audit()
    if a.report:
        print(f"written {write_report(res)}")
        return 0
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(f"[trust-root-audit] A1 修复={res['trA1']['fail_open_fixed']}；"
          f"A2 全拒={res['trA2']['all_rejected']}；闭包={res['trA3']['n_files']} 条目/"
          f"{res['trA3']['status']}；外部锚真连={res['trA4']['real_external_service_connected']}；"
          f"独立性={res['independence']['level']}（L3 未达）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
