"""628 B4 · 他验端到端演示（独立验证 → VSA 凭证 → 透明日志）

把 B1/B2/B3 串成一条可复核的链路（他验三件套的端到端闭环）：

1. 子进程运行 **B1 独立验证者**（零 import、纯标准库、朴素算法）→ 关键数字
2. 与**系统 V2 投影**对比：子进程设 `QUEYI_AUTHORITY_V2=1` 调 626 编译器 `w2_summary()`
3. 子进程运行 **B2** 生成 VSA 凭证（HMAC-SHA256，锚定 ledger/grounded/PCK 三重输入哈希）
4. 子进程运行 **B3** 把凭证追加进 append-only 透明日志
5. 子进程运行 **B3** 验证日志完整性（线性哈希链逐条重算）
6. 输出端到端审计报告 + 一行审计声明

**设计**：本工具是**编排器**，不重算任何数字——所有计算都发生在子进程里，
避免"编排器顺手算一遍"造成同源耦合。

`--check`：验证端到端链路全绿，**幂等**（不新增凭证、不新增日志条目）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from typing import Any, Optional, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VERIFIER = os.path.join(HERE, "independent_verifier_628.py")
VSA_TOOL = os.path.join(HERE, "vsa_attestation_628.py")
LOG_TOOL = os.path.join(HERE, "transparency_log_628.py")

LOG = os.path.join(ROOT, "data", "transparency_log.jsonl")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
OUT_JSON = os.path.join(ROOT, "data", "third_party_audit_demo_628.json")
OUT_MD = os.path.join(ROOT, "data", "third_party_audit_demo_report_628.md")

ENV_FLAG = "QUEYI_AUTHORITY_V2"
EXPECT_W2 = {"IN": 114, "OUT": 7, "UNDEC": 0}
EXPECT_PCK_AUTHORIZED = 27
EXPECT_UNIQUE = 93

_SYS_SNIPPET = (
    "import sys, json\n"
    "sys.path.insert(0, {here!r})\n"
    "import authority_projection_compiler_626 as C\n"
    "print(json.dumps(C.AuthorityProjectionCompiler().w2_summary()))\n"
)


def _run(script: str, *args: str, env: Optional[dict] = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, script, *args], capture_output=True,
                          text=True, cwd=ROOT, env=env, timeout=300, check=False)


def _load_json(text: str) -> Any:
    """取子进程 stdout 里的 JSON（单行或多行缩进均可）。"""
    body = text.strip()
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        pass
    for line in reversed(body.splitlines()):
        s = line.strip()
        if s.startswith("{") and s.endswith("}"):
            return json.loads(s)
    raise ValueError(f"no JSON in output: {body[:120]!r}")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


# ── 步骤 1-2：独立重算 vs 系统 V2 投影 ──────────────────────────────

def step1_independent_verify() -> dict:
    p = _run(VERIFIER)
    if p.returncode != 0:
        raise RuntimeError(f"B1 独立验证者失败 rc={p.returncode}: {p.stderr[-300:]}")
    return cast(dict, _load_json(p.stdout))


def system_v2_w2() -> dict:
    """子进程设 flag=1 调 626 编译器，取 V2 模式 W2 分布。"""
    env = dict(os.environ)
    env[ENV_FLAG] = "1"
    p = subprocess.run([sys.executable, "-c", _SYS_SNIPPET.format(here=HERE)],
                       capture_output=True, text=True, cwd=ROOT, env=env,
                       timeout=300, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"系统 V2 投影失败: {p.stderr[-300:]}")
    return cast(dict, _load_json(p.stdout))


def compare(iv: dict, sys_w2: dict) -> dict:
    return {
        "w2_match": sys_w2 == iv["w2"]["summary"] == EXPECT_W2,
        "verifier_vs_system": sys_w2 == iv["w2"]["summary"],
        "frozen_labels_match": bool(iv["w2"]["frozen_labels_match"]),
        "pck_authorized_match": iv["pck"]["authorized"] == EXPECT_PCK_AUTHORIZED,
        "ledger_chain_valid": bool(iv["ledger_chain"]["chain_valid"]),
        "unique_match": iv["unique"]["unique"] == EXPECT_UNIQUE,
    }


# ── 步骤 3-5：凭证 → 日志 → 完整性 ────────────────────────────────

def step3_generate_vsa() -> str:
    p = _run(VSA_TOOL, "--generate")
    if p.returncode != 0:
        raise RuntimeError(f"B2 生成凭证失败: {p.stderr[-300:]}")
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("written ")]
    if not lines:
        raise RuntimeError(f"B2 未返回凭证路径: {p.stdout[-200:]}")
    return cast(str, lines[-1].split(" ", 1)[1].strip())


def step4_append_log(vsa_path: str) -> dict:
    p = _run(LOG_TOOL, "--append", vsa_path)
    if p.returncode != 0:
        raise RuntimeError(f"B3 追加日志失败: {p.stderr[-300:]}")
    return cast(dict, _load_json(p.stdout))


def step5_verify_log() -> dict:
    p = _run(LOG_TOOL, "--status")
    if p.returncode != 0:
        raise RuntimeError(f"B3 验证日志失败: {p.stderr[-300:]}")
    return cast(dict, _load_json(p.stdout))


def tail_logged_credential() -> Optional[str]:
    """**日志在册的最后一个凭证**。

    比"文件名最新的凭证"可靠：不受同秒生成、未入册凭证、测试尘埃影响
    （旧实现用文件名排序，`--check` 一旦产生未入册凭证就会误判）。
    """
    if not os.path.exists(LOG):
        return None
    entries = [json.loads(line) for line in open(LOG, encoding="utf-8") if line.strip()]
    if not entries:
        return None
    p = os.path.join(ROOT, str(entries[-1].get("vsa_file", "")))
    return p if os.path.exists(p) else None


def step_inclusion(vsa_path: str) -> dict:
    p = _run(LOG_TOOL, "--inclusion", vsa_path)
    if p.returncode != 0:
        raise RuntimeError(f"B3 存在性验证失败: {p.stderr[-300:]}")
    return cast(dict, _load_json(p.stdout))


# ── 端到端实跑 / 幂等自检 ─────────────────────────────────────────

def run_e2e(write_report: bool = False) -> dict:
    """完整跑一次：独立验证 → 对比 → 生成凭证 → 追加日志 → 验链 → 审计声明。"""
    iv = step1_independent_verify()
    sys_w2 = system_v2_w2()
    cmp_ = compare(iv, sys_w2)

    vsa_path = step3_generate_vsa()
    append = step4_append_log(vsa_path)
    log = step5_verify_log()
    inc = step_inclusion(vsa_path)

    cred = json.load(open(vsa_path, encoding="utf-8"))
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    statement = (
        f"在 {stamp}，独立验证者 {cred['verifier_id']}"
        f"（脚本 sha256 {cred['verifier_sha256'][:16]}…）对输入 "
        f"ledger={iv['ledger_chain']['events']} 条 / PCK={iv['pck']['total']} 张 / "
        f"节点 grounded_labels 独立重算得 W2 IN/OUT/UNDEC="
        f"{iv['w2']['summary']['IN']}/{iv['w2']['summary']['OUT']}/"
        f"{iv['w2']['summary']['UNDEC']}，与系统 V2 投影 "
        f"IN/OUT/UNDEC={sys_w2['IN']}/{sys_w2['OUT']}/{sys_w2['UNDEC']} "
        f"{'一致' if cmp_['verifier_vs_system'] else '不一致'}；凭证 "
        f"{os.path.relpath(vsa_path, ROOT)} 已存入透明日志 "
        f"index={append['log_index']}（entry_hash={append['entry_hash'][:16]}…），"
        f"日志链{'完整' if log['chain_valid'] else '断裂'}（{log['entries']} 条）。"
    )
    result = {
        "stamp": stamp,
        "verifier_id": cred["verifier_id"],
        "verifier_sha256": cred["verifier_sha256"],
        "independent": iv,
        "system_v2_w2": sys_w2,
        "compare": cmp_,
        "vsa_path": os.path.relpath(vsa_path, ROOT),
        "vsa_attestation": cred["attestation"],
        "log_append": append,
        "log_state": log,
        "inclusion": inc,
        "audit_statement": statement,
        "all_green": all(cmp_.values()) and log["chain_valid"] and bool(inc["included"]),
    }
    if write_report:
        _write_report(result)
    return result


def run_check() -> dict:
    """幂等自检：不生成新凭证、不追加日志、不改任何文件。"""
    iv = step1_independent_verify()
    sys_w2 = system_v2_w2()
    cmp_ = compare(iv, sys_w2)
    log = step5_verify_log()
    cred_path = tail_logged_credential()
    vsa_ok = False
    inc_ok = False
    if cred_path:
        p = _run(VSA_TOOL, "--verify-path", cred_path)
        vsa_ok = bool(_load_json(p.stdout)["valid"])
        inc_ok = bool(step_inclusion(cred_path)["included"])
    checks = dict(cmp_)
    checks.update({
        "log_chain_valid": bool(log["chain_valid"]),
        "log_entries_ge_1": log["entries"] >= 1,
        "log_files_ok": bool(log["files"]["ok"]),
        "all_credentials_logged": not log["unlogged"],
        "logged_vsa_valid": vsa_ok,
        "logged_vsa_in_log": inc_ok,
    })
    return {"checks": checks, "all_ok": all(checks.values()), "log_state": log,
            "system_v2_w2": sys_w2, "independent_w2": iv["w2"]["summary"],
            "logged_credential": (os.path.relpath(cred_path, ROOT) if cred_path else None)}


def _write_report(r: dict) -> None:
    iv = r["independent"]
    cmp_ = r["compare"]
    lines = [
        "# 628 B4 · 他验端到端演示报告（独立验证 → VSA 凭证 → 透明日志）", "",
        f"- 运行时刻：{r['stamp']}",
        f"- 独立验证者：`{r['verifier_id']}`（脚本 sha256 `{r['verifier_sha256'][:16]}…`）",
        "",
        "## 一、链路步骤与结果", "",
        "| 步骤 | 组件 | 结果 |",
        "|---|---|---|",
        f"| 1 独立重算关键数字 | B1 独立验证者（零 import） | W2 {iv['w2']['summary']}"
        f"／PCK authorized {iv['pck']['authorized']}／ledger 链 "
        f"{'valid' if iv['ledger_chain']['chain_valid'] else 'BROKEN'}"
        f"（{iv['ledger_chain']['events']} 条）／unique {iv['unique']['unique']} |",
        f"| 2 与系统 V2 投影对比 | 626 编译器（flag=1） | 系统 "
        f"{r['system_v2_w2']} ↔ 独立 {iv['w2']['summary']} ⇒ "
        f"{'一致' if cmp_['verifier_vs_system'] else '不一致'} |",
        f"| 3 生成 VSA 凭证 | B2（HMAC-SHA256） | `{r['vsa_path']}` |",
        f"| 4 追加透明日志 | B3（append-only） | index={r['log_append']['log_index']}"
        f"（entry_hash {r['log_append']['entry_hash'][:16]}…） |",
        f"| 5 日志完整性 | B3（线性哈希链） | "
        f"{'完整' if r['log_state']['chain_valid'] else '断裂'}"
        f"（{r['log_state']['entries']} 条） |",
        f"| 6 凭证存在性 | B3（inclusion） | "
        f"{'在册 index=' + str(r['inclusion']['log_index']) if r['inclusion']['included'] else '不在册'} |",
        f"| 7 日志/凭证一致性 | B3（漂移检测） | 引用文件完整 "
        f"{r['log_state']['files']['ok']}（{r['log_state']['entries']} 条）· "
        f"未入册凭证 {len(r['log_state']['unlogged'])} 张 |",
        "",
        "## 二、独立验证 vs 系统输出", "",
        "| 项目 | 独立重算 | 系统口径 | 一致 |",
        "|---|---|---|---|",
        f"| W2 IN/OUT/UNDEC | {iv['w2']['summary']} | {r['system_v2_w2']} | "
        f"{cmp_['verifier_vs_system']} |",
        f"| W2 逐节点 vs 冻结 label | {iv['w2']['nodes']} 节点 | 121 节点 | "
        f"{cmp_['frozen_labels_match']} |",
        f"| PCK authorized | {iv['pck']['authorized']} | 27 | "
        f"{cmp_['pck_authorized_match']} |",
        f"| ledger 哈希链 | {'valid' if iv['ledger_chain']['chain_valid'] else 'BROKEN'} | "
        f"452 条 valid | {cmp_['ledger_chain_valid']} |",
        f"| unique 审查项 | {iv['unique']['unique']} | 93 | {cmp_['unique_match']} |",
        "",
        "## 三、审计声明", "",
        f"> {r['audit_statement']}",
        "",
        "## 四、他验意义", "",
        "- 这是系统第一次有「**不依赖本项目代码**、可验证、可追溯的第三方复核闭环」：",
        "  独立验证者零 import 本项目工具、纯标准库、朴素算法；凭证锚定输入哈希；",
        "  日志 append-only 且任何历史改动都会断链。",
        "- 与 v20 调研结论对应：独立复核 ✅ / VSA 验证凭证 ✅ / 透明日志 ✅"
        "（三件套全部落地**原型**）。",
        "- **诚实局限**：① 验证者仍由本项目作者编写（缺真正的外部验证者）；",
        "  ② VSA 用 HMAC 而非非对称签名（无独立密钥托管）；",
        "  ③ 日志存本地、无外部见证者。三条都需后续批次（外部主体 / 密钥托管 / 公开 Rekor）。",
        "",
        f"- **总判定**：{'端到端全绿 ✅' if r['all_green'] else '存在不一致 ❌'}",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run_check()
    c = r["checks"]
    chk("独立重算 = 系统 V2 投影（W2）", c["verifier_vs_system"],
        f"({r['independent_w2']} ↔ {r['system_v2_w2']})")
    chk("W2 数字 = IN114/OUT7/UNDEC0", c["w2_match"])
    chk("与冻结 label 逐节点一致", c["frozen_labels_match"])
    chk("PCK authorized = 27", c["pck_authorized_match"])
    chk("ledger 哈希链 valid", c["ledger_chain_valid"])
    chk("unique = 93", c["unique_match"])
    chk("日志在册凭证签名/输入/结果有效", c["logged_vsa_valid"],
        f'({r["logged_credential"]})')
    chk("日志在册凭证可验证存在于日志（inclusion）", c["logged_vsa_in_log"])
    chk("透明日志链完整且 ≥1 条", c["log_chain_valid"] and c["log_entries_ge_1"],
        f"({r['log_state']['entries']} 条)")
    chk("日志引用的凭证文件都在且哈希一致", c["log_files_ok"])
    chk("凭证全部入册（无未登记凭证）", c["all_credentials_logged"],
        f'({r["log_state"]["unlogged"]})')
    chk("端到端全绿", r["all_ok"])
    print(f"B4 third-party audit demo check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B4 他验端到端演示")
    ap.add_argument("--check", action="store_true", help="幂等自检（不写产物）")
    ap.add_argument("--report", action="store_true", help="端到端实跑并写报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = run_e2e(write_report=args.report)
    if args.report:
        print(f"written {OUT_MD}")
        print(f"written {OUT_JSON}")
    print(r["audit_statement"])
    return 0 if r["all_green"] else 1


if __name__ == "__main__":
    sys.exit(main())
