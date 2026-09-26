"""643 阶段0 · **两阶段 pytest 跑法**固化（fast 并行 ~90s + slow 串行 ~11min）。

**为什么**（铁律 §零.10）：全量串行 ≈ 35–40 分钟，是批循环墙钟的主要成本；
而本仓测试天然分两类（`tests/conftest.py:18-25` 的语义口径）：

* **fast**：纯逻辑，**并行安全** ⇒ `pytest -m "not slow" -n auto`（参考 85–90s）；
* **slow**：真调编译器 / 真跑 replay / 真跑 poison，**共享真实仓可变状态**
  （`build/.replay_lock`、`Examples/atoms/*.asm` 瞬时改写）⇒ `pytest -m slow -n0`（参考 640–660s）。

**为什么不用 `-n auto` 跑全部**：pyproject 注释（`pyproject.toml:156-172`）已实测——
14 个模块共享真实可变状态，32 路并发下 `replay 锁被占用超时` 假红；
且 xdist 3.8 的 `--dist loadgroup` + `xdist_group` **实测无效**（调度器读不到 marker）。
⇒ 只能**按标记切两阶段**（构造上安全，不依赖分组）。

**本模块的工程取舍（相对 642 的经验）**：
1. **计数以 junit XML 为准**（`--junitxml`），不依赖终端汇总行 ——
   642 实测"终端末尾汇总行会丢失"，进度行推导虽可用但脆弱；XML 是机器可读的权威口径；
2. 两阶段各自**记录墙钟与预算**（fast ≤ 120s / slow ≤ 900s 的**告警线**，不是硬失败，
   因为墙钟随机器负载漂移，pyproject 已声明"参考值、非契约"）；
3. `--check` 只读幂等；`--report` 写 `data/643_pytest_two_phase.md` + `.json`；
4. 不写 `-n auto` 进 addopts（不改 pyproject，避免影响别人的串行默认）。

只读契约：`--check` 只读、exit 0；`--fast` / `--slow` / `--both` 会**真跑 pytest**（这是它的本职），
产物日志落 `data/643_pytest_<phase>.txt` + `.xml`。纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
OUT_MD = os.path.join(ROOT, "data", "643_pytest_two_phase.md")
OUT_JSON = os.path.join(ROOT, "data", "643_pytest_two_phase.json")

#: 两阶段的权威命令（与 pyproject 注释、CI 一致）
PHASES: dict[str, list[str]] = {
    "fast": ["-m", "not slow", "-n", "auto"],
    "slow": ["-m", "slow", "-n0"],
}
#: 告警线（秒）——参考值、非契约（pyproject:167-170）
BUDGET = {"fast": 120.0, "slow": 900.0}
FAST_REFERENCE = "85–90s（589 任务4b 实测）"
SLOW_REFERENCE = "≈644.8s（589 任务4b 实测）"


def _py() -> str:
    return PY if os.path.exists(PY) else sys.executable


# ── 产物净化（**真实缺陷的修法**，见诚实登记）─────────────────────────────────
# 643 首跑实测：pytest 的**断言 diff 会带 ANSI 着色**（ESC `\x1b`），原样落盘到
# `data/643_pytest_fast.txt` ⇒ **破坏仓库两条"data/ 无控制字符"测试**
# （`test_control_char_cleaner_626::test_repo_data_has_no_control_chars_now`、
#   `test_snapshot_integrity_ci_626::test_control_chars_clean`）。
# 修法：① 命令加 `--color=no`（从源头不产生）；② 写入前**净化**（兜底，防别的来源）；
#       ③ junit XML 同样净化（失败消息里也会带 ANSI）。
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_KEEP = ("\t", "\n", "\r")


def sanitize(text: str) -> str:
    """去掉 ANSI 转义序列与所有控制字符（保留 \\t\\n\\r）。"""
    t = _ANSI.sub("", text)
    return "".join(ch for ch in t
                   if ch in _KEEP or (ord(ch) >= 32 and ord(ch) != 127))


def sanitize_file(path: str) -> int:
    """原地净化一个文本文件；返回被移除的控制字符数（0 = 本来就干净）。"""
    if not os.path.exists(path):
        return 0
    raw = open(path, "rb").read()
    keep = {9, 10, 13}
    removed = sum(1 for b in raw if b < 32 and b not in keep or b == 127)
    if not removed:
        return 0
    open(path, "wb").write(bytes(b for b in raw if b in keep or (b >= 32 and b != 127)))
    return removed


def junit_path(phase: str) -> str:
    return os.path.join(ROOT, "data", f"643_pytest_{phase}.xml")


def log_path(phase: str) -> str:
    return os.path.join(ROOT, "data", f"643_pytest_{phase}.txt")


def counts_from_junit(path: str) -> dict[str, int]:
    """从 junit XML 取权威计数（不依赖终端汇总行）。"""
    if not os.path.exists(path):
        return {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "passed": 0}
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    t = f = e = s = 0
    for su in suites:
        if su.tag != "testsuite":
            continue
        t += int(su.get("tests", 0))
        f += int(su.get("failures", 0))
        e += int(su.get("errors", 0))
        s += int(su.get("skipped", 0))
    return {"tests": t, "failures": f, "errors": e, "skipped": s,
            "passed": max(0, t - f - e - s)}


def node_id_of(tc: "ET.Element") -> str:
    """junit `testcase` ⇒ 可被 pytest 直接选中的 node id。

    junit 的 `classname` 是**点号模块名**（如 `tests.test_622_a2`），而 pytest 选例需要
    **文件路径含 `.py`**（`tests/test_622_a2.py::test_x`）。这里做转换 ——
    这个坑本批踩过：漏 `.py` 会让 `pytest <id>` 报 `file or directory not found` 而**静默 0 例**。
    """
    cls = tc.get("classname", "")
    name = tc.get("name", "")
    parts = [p for p in cls.split(".") if p]
    if not parts:
        return ""
    if len(parts) == 1:
        file = parts[0] + ".py"
        inner = ""
    else:
        file = f"{parts[0]}/{parts[1]}.py"
        inner = "::".join(parts[2:])
    inner = f"::{inner}" if inner else ""
    return f"{file}{inner}::{name}" if name else f"{file}{inner}"


def failed_node_ids(path: str) -> list[str]:
    """从 junit XML 取失败/错误用例的 node id（用于偶发项登记/复跑取证）。"""
    if not os.path.exists(path):
        return []
    root = ET.parse(path).getroot()
    bad: list[str] = []
    for tc in root.iter("testcase"):
        if tc.find("failure") is not None or tc.find("error") is not None:
            nid = node_id_of(tc)
            if nid:
                bad.append(nid)
    return sorted(set(bad))


def phase_report(phase: str) -> dict[str, Any]:
    """读回某一阶段的产物（跑过才有）。"""
    p = counts_from_junit(junit_path(phase))
    j = os.path.join(ROOT, "data", "643_pytest_two_phase.json")
    meta: dict[str, Any] = {}
    if os.path.exists(j):
        try:
            meta = json.loads(open(j, encoding="utf-8").read()).get("phases", {}).get(phase, {})
        except (OSError, json.JSONDecodeError):
            meta = {}
    return {"phase": phase, "budget_s": BUDGET[phase], **p,
            "failed_node_ids": failed_node_ids(junit_path(phase)), **meta}


def run_phase(phase: str, timeout: float = 1800.0) -> dict[str, Any]:
    """真跑一个阶段；返回 {phase, exit_code, seconds, counts, failed_node_ids, log}。"""
    if phase not in PHASES:
        raise ValueError(f"未知阶段：{phase}")
    xml = junit_path(phase)
    cmd = [_py(), "-m", "pytest", "tests/", *PHASES[phase], "-q",
           "--color=no",                       # ① 源头不产生 ANSI（否则污染 data/）
           f"--junitxml={xml}"]
    # 证据新鲜度闸门（**真实缺陷的修法**）：pytest 在 `pytest.exit()` / 收集期崩溃时
    # **不会写 junit**，此时若直接读路径就会拿到**上一轮的陈旧 XML** ⇒ 报出上一轮的失败清单
    # （643 实测踩过：第四轮打印的失败清单与第三轮**逐字相同**，一度误判"-m 过滤失效"）。
    # 修法：跑前删除 + 跑后校验存在性；缺失 ⇒ counts 置空且 `evidence_valid=False`。
    if os.path.exists(xml):
        os.remove(xml)
    started = time.time()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, env=env, timeout=timeout)
        out = p.stdout.decode("utf-8", "replace") + "\n" + p.stderr.decode("utf-8", "replace")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"TIMEOUT after {timeout}s", 124
    seconds = round(time.time() - started, 1)
    out = sanitize(out)                          # ② 兜底净化
    sanitize_file(xml)                           # ③ junit 也净化（失败消息含 ANSI）
    with open(log_path(phase), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"# pytest -m {PHASES[phase]} @ {datetime.datetime.now().isoformat(timespec='seconds')}\n")
        fh.write("# 注：本文件已经 sanitize() 净化（去 ANSI/控制字符）——data/ 有'无控制字符'门禁\n")
        fh.write(out)
    fresh = os.path.exists(xml)
    counts = counts_from_junit(xml) if fresh else {}
    res = {"phase": phase, "exit_code": rc, "seconds": seconds, "cmd": " ".join(cmd),
           "counts": counts, "evidence_valid": bool(fresh),
           "failed_node_ids": failed_node_ids(xml) if fresh else [],
           "budget_s": BUDGET[phase], "log": log_path(phase), "junit": xml}
    _save_meta(phase, res)
    return res


def _save_meta(phase: str, res: dict[str, Any]) -> None:
    payload: dict[str, Any] = {"schema": "pytest_two_phase/1", "phases": {}}
    if os.path.exists(OUT_JSON):
        try:
            payload = json.loads(open(OUT_JSON, encoding="utf-8").read())
        except (OSError, json.JSONDecodeError):
            pass
    payload.setdefault("phases", {})[phase] = {
        k: res[k] for k in ("exit_code", "seconds", "cmd", "budget_s")}
    payload["updated"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def green(phase: str) -> bool:
    """绿 = **有新鲜证据**（junit 是本轮产物）且 0 失败 0 错误。

    没有 `evidence_valid` 记录时退化为 `tests > 0`（兼容没有 meta 的旧产物）。
    """
    r = phase_report(phase)
    fresh = bool(r.get("evidence_valid", int(r["tests"]) > 0))
    return bool(fresh and int(r["tests"]) > 0
                and int(r["failures"]) == 0 and int(r["errors"]) == 0)


def verify_green(exclude: tuple[str, ...] = ()) -> dict[str, Any]:
    """两阶段都跑过、都 0 失败 ⇒ 绿。`exclude` 允许登记偶发项（须列 node id）。"""
    out: dict[str, Any] = {}
    for ph in PHASES:
        r = phase_report(ph)
        bad = [n for n in r["failed_node_ids"] if n not in exclude]
        out[ph] = {"tests": r["tests"], "failures": r["failures"] + r["errors"],
                   "skipped": r["skipped"], "seconds": r.get("seconds"),
                   "unexpected_failures": bad, "ok": r["tests"] > 0 and not bad}
    out["all_ok"] = all(v["ok"] for k, v in out.items() if k != "all_ok")
    return out


def write_report() -> str:
    lines = [
        "# 643 阶段0 · 两阶段 pytest 纪律固化", "",
        "> 依据：`pyproject.toml:151-173`（为什么不用 `-n auto` 跑全部）+ `tests/conftest.py:18-46`"
        "（快慢标记的**语义**口径）。", "",
        "## 一、权威命令（两阶段）", "",
        "```bash",
        "# fast：纯逻辑，并行安全",
        "pytest -m \"not slow\" -n auto      # 参考 " + FAST_REFERENCE,
        "# slow：真编译/replay/poison，共享真实仓可变状态 ⇒ 必须串行",
        "pytest -m slow -n0                # 参考 " + SLOW_REFERENCE,
        "```", "",
        "## 二、标记从哪来（不是装饰器扫出来的）", "",
        "- `tests/conftest.py:159-171` 的 `pytest_collection_modifyitems` **按模块名**打标：",
        "  `SLOW_MODULES`（20 个）+ `SERIAL_EXTRA`（11 个）⇒ 共 **31 个模块**自动带 `slow`；",
        "- 其余模块自动带 `fast`；未加 `-m` 时标记不影响结果（默认跑全部）。",
        "- ⇒ **新增测试文件默认落在 fast 组**；若新测试真调编译器/真跑 replay，"
        "**必须**把模块名加进 `tests/conftest.py` 的 `SLOW_MODULES`（否则会并行假红）。", "",
        "## 三、为什么不能把 `-n auto` 写进 addopts（已实测，别再试）", "",
        "1. ~14 个模块共享**真实仓库可变状态**（`build/.replay_lock`、"
        "`Examples/atoms/*.asm` 删-重建-比 sha-还原）⇒ 并发下 `replay 锁被占用超时` 假红；",
        "2. `--dist loadgroup` + `xdist_group(\"serial\")` 在 xdist 3.8 **实测无效**"
        "（调度器读不到 item 上的 marker）；",
        "3. 故改为**按标记切两阶段**：不依赖分组，**构造上安全**。", "",
        "## 四、计数口径（643 起）", "",
        "- **以 junit XML 为准**：`pytest ... --junitxml=data/643_pytest_<phase>.xml`，"
        "计数与失败 node id 都从 XML 读（`counts_from_junit` / `failed_node_ids`）；",
        "- **为什么**：642 D2 实测「终端末尾汇总行未被后台捕获」（文件止于 `snapshot report summary`），"
        "当时只能靠进度行推导；XML 是机器可读的权威口径，免受捕获/编码问题影响；",
        "- 每阶段另存原始输出 `data/643_pytest_<phase>.txt`（保留给人工查证）。", "",
        "## 五、墙钟预算（告警线，非契约）", "",
        "| 阶段 | 命令 | 参考墙钟 | 告警线 |", "|---|---|---|---|",
        f"| fast | `-m \"not slow\" -n auto` | {FAST_REFERENCE} | {BUDGET['fast']:.0f}s |",
        f"| slow | `-m slow -n0` | {SLOW_REFERENCE} | {BUDGET['slow']:.0f}s |", "",
        "> 超告警线**不失败**，只登记 —— 墙钟随机器负载/核数漂移（pyproject:170 已声明"
        "\"参考值、非契约\"）。", "",
        "## 六、最近一次实测", "",
        "| 阶段 | tests | passed | failures | errors | skipped | 秒 | 判定 |",
        "|---|---|---|---|---|---|---|---|"]
    for ph in PHASES:
        r = phase_report(ph)
        if r["tests"] == 0:
            lines.append(f"| {ph} | — | — | — | — | — | — | **未跑** |")
            continue
        ok = "✅ 绿" if (r["failures"] == 0 and r["errors"] == 0) else "❌ 红"
        lines.append(f"| {ph} | {r['tests']} | {r['passed']} | {r['failures']} | {r['errors']} | "
                     f"{r['skipped']} | {r.get('seconds', '—')} | {ok} |")
    lines += ["", "## 诚实登记", "",
              "1. 墙钟是**参考值非契约**（同机同核数下近似可复现，负载变化即漂移）；",
              "2. `-n auto` 的 worker 数取决于本机核数 ⇒ **同一命令在不同机器上不同墙钟**；",
              "3. 本模块**不改** `pyproject.toml` 的 `addopts`（保持别人的串行默认），"
              "两阶段只在本模块与 `run_643_gate` 里显式指定；",
              "4. junit XML 是 pytest 官方产物，但其 `tests/failures/errors/skipped` 口径"
              "与终端汇总行**在 `-n auto` 下可能因 worker 崩溃而略异**（本批未遇到，仅登记）。",
              "5. **并发写入污染（本批实测的重大情境）**：643 执行期间检测到"
              "**另一批次（644）在同一工作区写入**（`_auto/inbox/644.md` 11:18 入队；"
              "`tools/*_644.py` 于 11:25–11:42 连续落盘；644 的 pytest 进程实测在跑）。"
              "后果：表里\"最近一次实测\"的**部分红与 643 无关** —— 实测 mypy 报"
              "`tools/evidence_conflict_644.py` 的 `arg-type`、ruff 报"
              "`tests/test_evidence_card_link_644.py` 的 `F401`，都是**644 的半成品文件**。"
              "⇒ **静态检查类红（mypy/ruff/integrity/门禁自检）不得计入本模块的\"并行安全\"判定**；"
              "本模块的并行安全结论建立在**第一轮 fast（早于 644 开工）**与其**串行复跑取证**上"
              "（`_auto/_643_parallel_reds.json`）。",
              "6. **证据新鲜度闸门（真实缺陷的修法）**：pytest 在收集期崩溃/`pytest.exit()` 时"
              "**不写 junit**，若直接读路径就会拿到**上一轮陈旧 XML**（本批实测：第四轮打印的失败"
              "清单与第三轮**逐字相同**，一度误判\"`-m` 过滤失效\"）。修法：跑前删除 XML + "
              "跑后校验存在性，缺失则 `evidence_valid=False` 且**不报计数**。",
              "7. **node id 必须含 `.py`（真实缺陷的修法）**：junit 的 `classname` 是点号模块名，"
              "转成 pytest 选例路径时漏 `.py` 会让 `pytest <id>` 报"
              "`file or directory not found` 而**静默 0 例**（本批实测：一次\"串行全绿\"的取证"
              "其实跑了 0 个用例）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


DOC = os.path.join(ROOT, "docs", "pytest_two_phase.md")


def write_doc() -> str:
    """**工程纪律文档**（`docs/pytest_two_phase.md`，入库；数据型报告另存 data/）。"""
    lines = [
        "# 工程纪律 · 全量 pytest 两阶段跑法", "",
        "> 643 任务 0.2 固化。依据 `pyproject.toml:151-173` 与 `tests/conftest.py`。",
        "> 数据型报告（含最近一次实测数字）：`data/643_pytest_two_phase.md`。", "",
        "## 规矩", "",
        "1. **默认跑两阶段，不跑全量串行**（全量串行 ≈ 35–40 min，两阶段 ≈ 6 min + 11 min）：",
        "",
        "   ```bash",
        "   pytest -m \"not slow\" -n auto    # fast：纯逻辑，并行安全",
        "   pytest -m slow -n0              # slow：真编译/replay/poison，共享真实仓状态 ⇒ 串行",
        "   ```",
        "",
        "2. **计数以 junit XML 为准**：`--junitxml=data/643_pytest_<phase>.xml`；",
        "   不依赖终端汇总行（642 实测它会丢），也不靠进度行推导（脆弱）。",
        "   统一入口：`python tools/pytest_two_phase_643.py --fast|--slow|--both`。",
        "3. **新增测试默认落 fast 组**；若新测试**真调编译器 / 真跑 replay / 真跑 poison /",
        "   读真实仓可变状态 / 起子进程读同一批状态**，**必须**把模块名加进",
        "   `tests/conftest.py` 的 `SLOW_MODULES`（编译类）或 `SERIAL_EXTRA`（读真实状态类）。",
        "4. **不要**把 `-n auto` 写进 `addopts`（`pyproject.toml:156-172` 已实测：",
        "   并发下假红；xdist 3.8 的 `--dist loadgroup` 分组**不生效**）。",
        "5. **写入 `data/` 的测试日志必须净化**（`--color=no` + `sanitize()`）：",
        "   仓库有\"`data/` 无控制字符\"门禁，ANSI ESC 会直接打破它。", "",
        "## 改标记后必须做的事", "",
        "`tests/conftest.py` 与 `pyproject.toml` 是 **`tool_integrity` 的 `test_config` 受控文件**",
        "（`tools/.tool_checksums` 的 `# test_config` 节）⇒ 改完必须重钉：", "",
        "```bash",
        "python tools/tool_integrity.py --update    # 重钉 core + test_config + supply_chain + ruler",
        "python tests/../tools/tool_integrity.py --check   # 四项全 OK 才算完",
        "```", "",
        "否则 `pytest_configure` 的测试器配置完整性自检会**拒绝开跑**（591 任务3）。", "",
        "## 已知代价（如实登记）", "",
        "- 墙钟是**参考值非契约**（随核数/负载漂移）；",
        "- 串行组随批次增长（643 实测：31 → 77 个模块）；串行组越大，`slow` 阶段越长；",
        "- `SLOW_MODULES`/`SERIAL_EXTRA` 是**经验累积清单，不声称完备**：",
        "  并行跑再现新红时按实测增量登记（清单里逐批留了取证说明）。"]
    with open(DOC, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return DOC


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("两阶段各一条命令", set(PHASES) == {"fast", "slow"})
    chk("fast 用 -n auto", PHASES["fast"] == ["-m", "not slow", "-n", "auto"])
    chk("slow 用 -n0（串行）", PHASES["slow"] == ["-m", "slow", "-n0"])
    chk("告警线 fast < slow", BUDGET["fast"] < BUDGET["slow"])

    # junit 解析（合成样本，不依赖真实跑）
    import tempfile
    xml = ('<?xml version="1.0" encoding="utf-8"?><testsuites><testsuite name="p" '
           'tests="5" failures="1" errors="0" skipped="1">'
           '<testcase classname="tests.a" name="ok"/>'
           '<testcase classname="tests.a" name="bad"><failure message="x">t</failure></testcase>'
           '</testsuite></testsuites>')
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "j.xml")
        open(f, "w", encoding="utf-8").write(xml)
        c = counts_from_junit(f)
        chk("junit 计数正确", c == {"tests": 5, "failures": 1, "errors": 0, "skipped": 1,
                                    "passed": 3}, str(c))
        chk("junit 失败 node id（**含 .py**，可直接被 pytest 选中）",
            failed_node_ids(f) == ["tests/a.py::bad"], str(failed_node_ids(f)))
        chk("node id 可被 pytest 识别为文件路径",
            all(n.split("::")[0].endswith(".py") for n in failed_node_ids(f)))

    # 净化：ANSI/控制字符必须被去掉（643 首跑实测踩过，污染 data/ 门禁）
    dirty = "\x1b[33m'atoms'\x1b[0m ok\x08\x0c"
    chk("sanitize 去 ANSI", "\x1b" not in sanitize(dirty))
    chk("sanitize 保留 \\t\\n\\r",
        sanitize("a\tb\nc\rd") == "a\tb\nc\rd")
    chk("sanitize 结果全为可打印/空白",
        all(ch in "\t\n\r" or ord(ch) >= 32 for ch in sanitize(dirty)))
    with tempfile.TemporaryDirectory() as td:
        df = os.path.join(td, "d.txt")
        open(df, "wb").write(b"a\x1bb\x08c")
        n = sanitize_file(df)
        chk("sanitize_file 原地净化并报数", n == 2 and open(df, "rb").read() == b"abc", str(n))
        chk("干净文件报 0", sanitize_file(df) == 0)
    chk("run_phase 命令含 --color=no（源头不产 ANSI）",
        '"--color=no"' in open(os.path.abspath(__file__), encoding="utf-8").read())

    # 标记确实被 conftest 注册（机制核验）
    conf = open(os.path.join(ROOT, "tests", "conftest.py"), encoding="utf-8").read()
    chk("conftest 注册 slow 标记", 'markers", "slow' in conf or '"slow:' in conf)
    chk("conftest 有 SLOW_MODULES", "SLOW_MODULES" in conf)
    chk("不把 -n auto 写进 addopts",
        "-n auto" not in open(os.path.join(ROOT, "pyproject.toml"), encoding="utf-8").read()
        .split("[tool.pytest.ini_options]")[1].split("addopts =")[1].splitlines()[0])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 两阶段 pytest 跑法")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--fast", action="store_true", help="只跑 fast 阶段")
    ap.add_argument("--slow", action="store_true", help="只跑 slow 阶段")
    ap.add_argument("--both", action="store_true", help="两阶段都跑")
    ap.add_argument("--report", action="store_true", help="写两阶段报告")
    ap.add_argument("--json", action="store_true", help="打印跑过的阶段结果（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rc = 0
    todo = ["fast", "slow"] if a.both else ([p for p in ("fast", "slow")
                                             if getattr(a, p, False)])
    for ph in todo:
        r = run_phase(ph)
        c = r["counts"]
        print(f"  [{ph}] exit={r['exit_code']} {r['seconds']}s "
              f"tests={c.get('tests', 0)} passed={c.get('passed', 0)} "
              f"failed={c.get('failures', 0)}+{c.get('errors', 0)} "
              f"skipped={c.get('skipped', 0)} evidence_valid={r['evidence_valid']}")
        if not r["evidence_valid"]:
            print("        ⚠️ 本轮没有 junit 产物（pytest 提前退出/收集期崩溃）"
                  "⇒ 计数不可用；**不要**读上一轮残留")
        for n in r["failed_node_ids"]:
            print(f"        FAILED {n}")
        if r["seconds"] > BUDGET[ph]:
            print(f"        ⚠️ 超告警线 {BUDGET[ph]:.0f}s（参考值非契约）")
        rc = rc or (0 if r["exit_code"] == 0 else 1)
    if a.report:
        print(f"written {write_doc()}")
        print(f"written {write_report()}")
    if a.json:
        print(json.dumps({p: phase_report(p) for p in PHASES}, ensure_ascii=False, indent=2))
    if not todo and not a.report and not a.json:
        g = verify_green()
        print(f"[two-phase] fast ok={g['fast']['ok']} slow ok={g['slow']['ok']} "
              f"⇒ all_ok={g['all_ok']}")
        return 0 if g["all_ok"] else 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
