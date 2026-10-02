# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_672a_design_system.py — 672a「设计系统 P0 补漏」的验收测试（25 条断言）。

三组，全部**无 jsdom 依赖**（任务书 F1 的"纯 Node"即：不碰浏览器、不渲染 DOM）：

  ① CSS 文本断言：焦点环令牌化 / 僵尸变量清零 / 圆角收敛 / z-index 令牌化。
     用 Python 读文本（等价于 grep，零依赖、秒级）；
  ② 对比度审计：subprocess 调 `node web/js/contrast_check.js --json`，
     断言配对数 ≥50、焦点环配对在列、基础 27 对保留、ratio 是真算的；
  ③ a11y 审计口径：`tools/a11y_audit_670c4.py` 的 stdout 与 JSON 都带覆盖率声明，
     且审计逻辑没被改坏（critical_total 仍为 0）。

为何 CSS 部分不也走 node：这三类断言的对象是**文本模式**（有没有某个字符串），
用 Node 再跑一遍只是多一层进程开销；真正需要 Node 的是 ②③（要真跑审计逻辑）。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")

# Node：优先环境变量，其次 PATH。仓库 CI 跑 web/tests/*.test.mjs 用的就是 PATH 上的 node。
NODE = os.environ.get("NODE_BIN") or "node"

A11Y_CSS = os.path.join(WEB, "css", "a11y.css")
ROBUST_CSS = os.path.join(WEB, "css", "robustness.css")
TOKENS_CSS = os.path.join(WEB, "css", "design-tokens.css")
STYLE_CSS = os.path.join(WEB, "style.css")
C669C_CSS = os.path.join(WEB, "css", "669c.css")
RESP_CSS = os.path.join(WEB, "css", "responsive.css")
AUDIT_JSON = os.path.join(ROOT, "data", "a11y_audit_670c4.json")

# 僵尸变量名（666 时代的旧别名，design-tokens.css 里**不存在**）
ZOMBIE_VARS = ("--bg-1", "--bg-2", "--border", "--fg-muted")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def hits(text: str, pattern: str) -> list:
    return re.findall(pattern, text)


# ─────────────────────────────────────────────────────────────────────────────
# ① 焦点环（任务 A）
# ─────────────────────────────────────────────────────────────────────────────
def test_a_focus_ring_tokenized():
    css = read(A11Y_CSS)
    # 旧暖橙 #d97757 必须彻底消失（它曾整体覆盖 design-tokens 的 --focus-ring）
    assert not hits(css, r"#d97757"), "a11y.css 仍有硬编码的旧焦点色 #d97757"
    assert "outline: var(--focus-ring)" in css, "焦点环未改用 var(--focus-ring)"
    assert "outline-offset: var(--focus-ring-offset)" in css, "焦点环 offset 未令牌化"
    # 消费的令牌必须在令牌源里真实存在（防"凭空造变量名"）
    tokens = read(TOKENS_CSS)
    assert "--focus-ring:" in tokens and "--focus-ring-offset:" in tokens, \
        "design-tokens.css 未定义 --focus-ring / --focus-ring-offset"


def test_a_old_orange_absent_project_wide():
    """旧橙只允许留在 design-tokens.css 的**历史变更说明注释**里（令牌源本批不动）。

    若哪天它在 a11y/robustness/style/669c/responsive 任一处复活，就是设计系统又被击穿。
    """
    for path in (A11Y_CSS, ROBUST_CSS, STYLE_CSS, C669C_CSS, RESP_CSS):
        assert not hits(read(path), r"d977"), \
            f"{os.path.basename(path)} 出现旧橙 d977（设计系统被击穿）"


# ─────────────────────────────────────────────────────────────────────────────
# ② 僵尸变量 / 圆角 / z-index（任务 B、C）
# ─────────────────────────────────────────────────────────────────────────────
def test_b_no_zombie_vars():
    for path in (A11Y_CSS, ROBUST_CSS):
        css = read(path)
        for var in ZOMBIE_VARS:
            assert var not in css, f"{os.path.basename(path)} 仍用僵尸变量 {var}"
    # 修复后的正确变量名必须真的出现（防"只删不改"）
    rob = read(ROBUST_CSS)
    for var in ("--panel-2", "--line", "--fg-mute"):
        assert var in rob, f"robustness.css 缺少修复后的变量 {var}"
    assert "--panel," in read(A11Y_CSS), "a11y.css 对话框底色未改用 --panel"


def test_b_radius_converged():
    """圆角只允许 4/6/8 三档 —— 12px 是 666 时代的旧值。"""
    for path in (A11Y_CSS, ROBUST_CSS):
        css = read(path)
        assert not hits(css, r"border-radius:\s*12px"), \
            f"{os.path.basename(path)} 仍有 border-radius: 12px"


def test_c_zindex_tokenized():
    css = read(A11Y_CSS)
    assert not hits(css, r"z-index:\s*10000"), "a11y.css 仍有绕过令牌层的 z-index: 10000"
    assert "z-index: var(--z-modal)" in css, "帮助弹窗 z-index 未改用 var(--z-modal)"
    assert "--z-modal:" in read(TOKENS_CSS), "design-tokens.css 未定义 --z-modal"


def test_b_tokens_consumed_exist():
    """本批消费的每个变量名都必须在令牌源里存在（--bg-1 这类僵尸变量的回归锁）。"""
    tokens = read(TOKENS_CSS)
    for var in ("--panel", "--panel-2", "--line", "--fg", "--fg-mute"):
        assert re.search(re.escape(var) + r"\s*:", tokens), \
            f"design-tokens.css 未定义 {var}（本批却消费了它）"


# ─────────────────────────────────────────────────────────────────────────────
# ③ 对比度审计口径（任务 D）
# ─────────────────────────────────────────────────────────────────────────────
def _contrast_report():
    r = subprocess.run([NODE, os.path.join("web", "js", "contrast_check.js"), "--json"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, "contrast_check 退出码非 0：\n" + r.stdout + r.stderr
    return json.loads(r.stdout)


def test_d_pair_count_and_composition():
    rep = _contrast_report()
    assert rep["pairs"] >= 50, f"配对数 {rep['pairs']} < 50（自动抽取没生效）"
    dark = rep["themes"]["dark"]
    base = [r for r in dark if r["source"] == "base"]
    focus = [r for r in dark if r["source"] == "focus-ring"]
    auto = [r for r in dark if r["source"] == "auto"]
    assert len(base) == 27, f"基础清单被破坏：{len(base)} 对（应为 27）"
    assert len(focus) == 3, f"焦点环配对应 3 对，实际 {len(focus)}"
    assert len(auto) >= 23, f"自动抽取 {len(auto)} 对 < 23"


def test_d_focus_ring_pairs_present_and_pass():
    rep = _contrast_report()
    for theme in ("dark", "light"):
        rows = [r for r in rep["themes"][theme] if r["source"] == "focus-ring"]
        assert len(rows) == 3, f"{theme}: 焦点环配对缺失"
        for r in rows:
            # 焦点环色 = --color-accent，底 = bg / surface / surface-2
            assert r["fg"] == "--color-accent", f"{theme}: 焦点环前景不是 accent"
            assert r["pass"], f"{theme}: 焦点环 vs {r['bg']} 未过 AA（{r['ratio']}:1）"


def test_d_ratios_are_computed_not_hardcoded():
    rep = _contrast_report()
    for theme in ("dark", "light"):
        for r in rep["themes"][theme]:
            assert isinstance(r["ratio"], (int, float)) and r["ratio"] > 0, \
                f"{theme}: {r['name']} 的 ratio 不是真算出来的数：{r['ratio']}"
    assert rep["failures"] == [], f"存在未过 AA 的配对：{rep['failures']}"


def test_d_error_token_gap_is_warned():
    """design-tokens.css 没有 --color-error ⇒ 必须**记 warn 而不是静默跳过**。"""
    rep = _contrast_report()
    assert any("--color-error" in str(w.get("token", "")) for w in rep["warns"]), \
        "缺少 --color-error 的 warn（错误色令牌缺口被静默吞掉了）"


# ─────────────────────────────────────────────────────────────────────────────
# ④ a11y 审计口径诚实化（任务 E）
# ─────────────────────────────────────────────────────────────────────────────
def test_e_coverage_declared_in_json():
    with open(AUDIT_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    assert data["coverage"] == "static_html_only", "JSON 缺 coverage 声明"
    assert data["js_rendered_dom_audited"] is False, "js_rendered_dom_audited 应为 False"
    assert len(data["limitations"]) >= 3, "limitations 未登记全部盲区"
    # 加元数据**不能**改审计逻辑：critical 数必须与 670c4 一致
    assert data["critical_total"] == 0, "审计逻辑被改坏了：critical_total 变了"
    assert len(data["pages"]) == 8, "审计页数变了"


def test_e_coverage_declared_in_stdout():
    r = subprocess.run([sys.executable, os.path.join("tools", "a11y_audit_670c4.py")],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "coverage: static HTML only (JS-rendered DOM not audited)" in r.stdout, \
        "stdout 未打印覆盖率声明 —— '0 问题'仍可能被读成'全站无问题'"


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 回归锁：新口径不能把旧结论改掉
# ─────────────────────────────────────────────────────────────────────────────
def test_d_base_pairs_unchanged():
    """670c 锁定的数值必须还在（自动抽取是**加项**，不是替换）。"""
    rep = _contrast_report()
    dark = {r["name"]: r["ratio"] for r in rep["themes"]["dark"] if r["source"] == "base"}
    assert abs(dark["正文 / 底"] - 16.91) < 0.05, \
        f"正文/底 暗色 {dark.get('正文 / 底')} 与 670c 锁定的 16.91 不符"
    assert abs(dark["正文 / 卡片"] - 16.13) < 0.05, "正文/卡片 暗色值被改坏"
    assert abs(dark["次级文字 / 卡片"] - 7.31) < 0.05, "次级文字/卡片 暗色值被改坏"


def test_d_auto_pairs_cover_the_two_fixed_files():
    """本批修的 a11y.css / robustness.css 必须真的进了抽取结果（不再靠人肉清单）。"""
    rep = _contrast_report()
    files = {r.get("file") for r in rep["themes"]["dark"] if r["source"] == "auto"}
    assert any(f and f.endswith("a11y.css") for f in files), "a11y.css 未进入自动抽取"
    assert any(f and f.endswith("robustness.css") for f in files), \
        "robustness.css 未进入自动抽取"


def test_a_both_focus_ring_sites_tokenized():
    """:focus-visible 与 .skip-link:focus 两处都要令牌化（只改一处等于没改）。"""
    css = read(A11Y_CSS)
    assert re.search(r":where\([^)]*\):focus-visible\s*\{[^}]*outline:\s*var\(--focus-ring\)",
                     css, re.DOTALL), "统一焦点样式未令牌化"
    assert re.search(r"\.skip-link:focus\s*\{[^}]*var\(--focus-ring\)", css, re.DOTALL), \
        ".skip-link 焦点未令牌化"


def test_b_positive_radius_values():
    """正向锁：改后的圆角必须是 8px（新档位），不是随手填的数。"""
    assert re.search(r"\.qy-dialog-box\s*\{[^}]*border-radius:\s*8px", read(A11Y_CSS), re.DOTALL), \
        "帮助弹窗圆角不是 8px"
    rob = read(ROBUST_CSS)
    assert re.search(r"\.qy-error-card\s*\{[^}]*border-radius:\s*8px", rob, re.DOTALL), \
        "错误卡圆角不是 8px"
    assert re.search(r"\.ns-fallback\s*\{[^}]*border-radius:\s*8px", rob, re.DOTALL), \
        "noscript 降级块圆角不是 8px"
