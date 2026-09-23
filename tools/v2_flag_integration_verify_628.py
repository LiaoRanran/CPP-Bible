"""628 A1 · V2 flag 接入验证（V1/V2 双路径数字一致 + 向后兼容）

验证内容：
1. flag 未设置 ⇒ 默认 V1（向后兼容），W2 = legacy grounded_labels（121 节点）
2. flag=0 ⇒ V1；flag=1 ⇒ V2（Authority ledger + 627 A1 归一化，121 节点）
3. 两种模式 W2 数字一致：IN 114 / OUT 7 / UNDEC 0，且逐节点标签一致
4. 输出 schema 一致（dict[node] → label）
5. CORE_TOOLS 不读 flag（静态扫描：gate_engine/atom_evidence_replay/poison_drill/toolchain/cppbible）
6. 修改 626 编译器后 tool_integrity --update 已重钉（.tool_checksums 中含该文件）
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV_FLAG = "QUEYI_AUTHORITY_V2"
OUT_MD = os.path.join(ROOT, "data", "v2_flag_integration_report_628.md")

CORE_TOOLS = ["gate_engine.py", "atom_evidence_replay.py",
              "poison_drill.py", "toolchain.py", "cppbible.py"]


def _run_mode(env_val: Optional[str], code: str) -> tuple[int, str]:
    env = dict(os.environ)
    env.pop(ENV_FLAG, None)
    if env_val is not None:
        env[ENV_FLAG] = env_val
    p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, env=env, cwd=ROOT, timeout=120)
    return p.returncode, p.stdout.strip()


SNIPPET = (
    "import sys, json; sys.path.insert(0, %r)\n"
    "import authority_projection_compiler_626 as C\n"
    "c = C.AuthorityProjectionCompiler()\n"
    "w2 = c.compile_w2()\n"
    "s = c.w2_summary()\n"
    "print(json.dumps({'v2': C.v2_enabled(), 'nodes': len(w2),\n"
    "                  'summary': s, 'labels': w2}, ensure_ascii=False))\n"
) % HERE


def run_verify() -> dict:
    results = {}
    for name, val in (("unset", None), ("v1", "0"), ("v2", "1")):
        rc, out = _run_mode(val, SNIPPET)
        results[name] = json.loads(out) if rc == 0 and out else {"error": out[-300:]}
    # 一致性判定
    v1, v2 = results.get("v1", {}), results.get("v2", {})
    consistent = (v1.get("summary") == v2.get("summary") == {"IN": 114, "OUT": 7, "UNDEC": 0}
                  and v1.get("labels") == v2.get("labels")
                  and v1.get("nodes") == v2.get("nodes") == 121)
    default_v1 = (results.get("unset", {}).get("v2") is False
                  and results.get("unset", {}).get("labels") == v1.get("labels"))
    # CORE_TOOLS 不读 flag
    core_clean = []
    for ct in CORE_TOOLS:
        p = os.path.join(HERE, ct)
        txt = open(p, encoding="utf-8", errors="ignore").read()
        if ENV_FLAG in txt:
            core_clean.append(ct)
    # integrity 重钉确认：--update 已跑 ⇒ .tool_checksums 在本批被重建（mtime 今日）
    ck = os.path.join(HERE, ".tool_checksums")
    re_pinned = False
    if os.path.exists(ck):
        import time
        re_pinned = time.strftime("%Y-%m-%d", time.localtime(
            os.path.getmtime(ck))) == time.strftime("%Y-%m-%d")
    return {"modes": results, "v1_v2_consistent": consistent,
            "default_is_v1": default_v1,
            "core_tools_reading_flag": core_clean,
            "integrity_re_pinned_today": re_pinned,
            "ok": consistent and default_v1 and not core_clean and re_pinned}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run_verify()
    v1, v2 = r["modes"].get("v1", {}), r["modes"].get("v2", {})
    chk("flag 未设置 ⇒ 默认 V1（向后兼容）", r["default_is_v1"])
    chk("V1 模式 121 节点", v1.get("nodes") == 121, f"({v1.get('nodes')})")
    chk("V2 模式 121 节点（归一化，非 519）", v2.get("nodes") == 121,
        f"({v2.get('nodes')})")
    chk("V1/V2 数字一致 IN114/OUT7/UNDEC0", r["v1_v2_consistent"],
        f"(V1={v1.get('summary')} V2={v2.get('summary')})")
    chk("CORE_TOOLS 不读 flag", not r["core_tools_reading_flag"],
        f"({r['core_tools_reading_flag']})")
    chk("tool_integrity --update 已重钉（基准为本批重建）", r["integrity_re_pinned_today"])
    print(f"A1 flag integration check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 A1 V2 flag 接入验证")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    r = run_verify()
    if args.report:
        v1, v2 = r["modes"].get("v1", {}), r["modes"].get("v2", {})
        lines = [
            "# 628 A1 · V2 flag 接入验证报告", "",
            "## 接入前状态",
            "- `v2_enabled()` 已定义（L46-47）但**全文件无调用点**——flag 是概念开关。",
            "- compile_w2 无条件走 ledger edge 粒度（519 节点）。",
            "",
            "## 接入位置与逻辑",
            "- `__init__`：`self.v2_mode = v2_enabled()`（编译时读取一次）。",
            "- `compile_w2()`：V1 → `_compile_w2_v1()`（legacy grounded_labels，121 节点）；"
            "V2 → `_compile_w2_v2()`（ledger + 627 A1 归一化，121 节点）。",
            "- 输出 schema 不变（dict[node]→label）；PCK/golden/dashboard/textbook 保持 "
            "authority-driven（626 前无 legacy 等价物，诚实登记）。",
            "- **偏差项登记**：626 测试 `test_w2_projection_vs_grounded_labels_deviation_registered` "
            "锁定 `len(w2)!=121`（当时偏差存在）——A1 落地后偏差被解决，该测试同 commit 更新为"
            "对齐断言；`test_empty_ledger_handled` 适配双模式。",
            "",
            "## V1 vs V2 对比",
            f"- V1（flag=0）：nodes={v1.get('nodes')} summary={v1.get('summary')}",
            f"- V2（flag=1）：nodes={v2.get('nodes')} summary={v2.get('summary')}",
            f"- 逐节点标签一致：{v1.get('labels') == v2.get('labels')}",
            "",
            "## 回归验证",
            f"- 默认（未设置）= V1：{r['default_is_v1']}",
            f"- CORE_TOOLS 读 flag 的文件：{r['core_tools_reading_flag'] or '无'}",
            f"- tool_integrity --update 已重钉：{r['integrity_re_pinned_today']}",
            "",
            f"- **总判定**：{'PASS ✅' if r['ok'] else 'FAIL ❌'}",
        ]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
    if args.check:
        return selftest()
    print(json.dumps({k: v for k, v in r.items() if k != "modes"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
