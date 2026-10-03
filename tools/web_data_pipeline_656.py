#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_data_pipeline_656.py — 656 C3/C4：前端数据管线 + 构建（一条命令，可接 CI）。

为什么需要它
============
656 之前，`web/data/` 下的三份 JSON 由**三个不同的工具**各自产出（`web_data_653 --build`、
`web_status_655`），谁先谁后、改了卡要不要重跑，全靠人记得。655 D 就在这里踩过一次：
重钉 `.tool_checksums` 之后忘了重生成 `manifest.json` ⇒ 台账哈希当场失配（被前端真求值抓出）。

本工具把这件事固化成**一条命令 + 一份索引 + 一次校验**：
  `--build`  依次跑齐所有生成器 ⇒ 校验 schema ⇒ 写 `web/data/index.json`（含每个文件的 sha256/字节）
             ⇒ 产出 `web/dist/`（保守压缩 + 版本号 + manifest）
  `--check`  只读校验：schema、index 是否与实际文件一致（漂移可见）、设计令牌对比度（WCAG 2.2 AA）、
             组件与页面接线（三个页面必须引用 tokens 与组件出口）

诚实边界
========
- **压缩是保守子集**（只删整行注释 / 空行 / 行尾空白），且产出后用 `node --check` 复检；
  检不过就**退回原样复制**并在 manifest 里标 `minified=false`——不为"看起来更小"牺牲正确性。
- 不引入任何 npm 依赖与打包框架（保持原生）。
- `--check` **不改任何文件**；漂移只报告，不自动修（要修请显式 `--build`）。

用法
====
    python tools/web_data_pipeline_656.py --build
    python tools/web_data_pipeline_656.py --check        # CI 用这个
    python tools/web_data_pipeline_656.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEB = ROOT / "web"
DATA = WEB / "data"
DIST = WEB / "dist"
TOKENS = WEB / "css" / "design-tokens.css"
COMPONENTS = WEB / "components"
INDEX = DATA / "index.json"
DIST_MANIFEST = DIST / "manifest.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

#: 数据文件 → 最小 schema（缺任一 ⇒ --check 红）
SCHEMAS: dict[str, list[str]] = {
    "graph.json": ["nodes", "links", "meta"],
    "manifest.json": ["count", "items"],
    "status.json": ["cards", "rules", "protectors", "escape", "w2",
                    "generated_from", "unavailable"],
    "cards_index.json": ["count", "cards"],
    "card.json": ["id", "meta", "claim", "verdict", "props", "evidence", "selfcheck"],
    # 667 新增：判决页数据（缺任一 ⇒ 页面会渲染成 undefined）
    "verdicts_667.json": ["dashboard", "verdicts", "verdicts_total", "compare",
                          "drift", "excluded", "unavailable"],
}

#: 生成器（顺序有意义：先图/台账，后现状，最后学习卡数据）
GENERATORS: list[list[str]] = [
    [sys.executable, str(HERE / "web_data_653.py"), "--build"],
    [sys.executable, str(HERE / "web_status_655.py")],
    [sys.executable, str(HERE / "teach_card_656.py"), "--list"],
    [sys.executable, str(HERE / "teach_card_656.py"), "--card", "ATOM-CONC-RACE-001"],
    # 670c A2/A4：把仓库根的真实数据同步进 web/data/（页面以 web/ 为文档根）
    [sys.executable, str(HERE / "web_experiments_sync_670c.py")],
]

#: 需要进 dist 的静态资源（相对 web/）
ASSETS: list[str] = [
    "index.html", "starmap.html", "verify.html", "card.html",
    "verdicts.html", "cards.html",
    # 670c A1/A2：学习页与实验页（669c 建页，670c 深化）
    "learn.html", "experiments.html",
    "app.js", "starmap.js", "verify.js", "verify_core.js", "graph_core.js",
    "card.js", "cards.js", "verdicts.js", "verdicts_core.js",
    # 674a 修复：`web/*.html` 静态引用但 ASSETS 漏列的 3 个 js（干净检出实测 dist 缺失：
    # index.html→home.js、learn.html→js/learn.js、experiments.html→js/experiments.js）。
    "home.js", "js/learn.js", "js/experiments.js",
    # 670c：页面用的纯逻辑模块（少了这些 dist 里的页面会 404 加载不到核心）
    "js/learn_engine.js", "js/charts.js", "js/cards_core.js", "js/contrast_check.js",
    "js/verdicts_core.js",
    "style.css", "css/design-tokens.css",
    # 670c A6：新页面的共享组件层（此前 dist 里没有它，新页面会掉样式）
    "css/669c.css",
    # 674a 修复：`web/*.html` 实际 `<link href="css/…">` 引用 5 个 css，而 ASSETS 只列了
    # `design-tokens.css` / `669c.css` ⇒ 干净检出上 `dist/` 缺 3 个 css（实测 27 处引用缺失、
    # `test_dist_no_missing_refs` / `test_dist_overall_passes` 红）。主仓之所以看着正常，
    # 是因为 `web/dist/`（gitignore）里**残留着更早一次构建**留下的文件 —— 属"本地绿、CI 红"的典型。
    # 这里按"页面实际引用"补齐（纯构建资源清单，不动任何前端源码）。
    "css/a11y.css", "css/responsive.css", "css/robustness.css",
    "components/index.js", "components/qy-nav.js", "components/qy-card.js",
    "components/qy-panel.js", "components/qy-button.js", "components/qy-tag.js",
    "components/qy-status.js",
]
PAGES = ["index.html", "starmap.html", "verify.html", "card.html",
         "verdicts.html", "cards.html",
         # 670c A1/A2：接线门禁要覆盖到这两个页面
         "learn.html", "experiments.html"]


# ── 基础 ────────────────────────────────────────────────────────────────────
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=False)
    return r.returncode, (r.stdout or "")[-300:] or (r.stderr or "")[-300:]


# ── WCAG 2.2 对比度（算出来，不靠眼睛）──────────────────────────────────────
def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(hexcolor: str) -> float:
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


#: 令牌 → 判定阈值：正文类 ≥4.5（AA 正文），图形/态点类 ≥3.0（AA 非文本）
CONTRAST_RULES: list[tuple[str, str, float, str]] = [
    ("--color-text", "--color-bg", 4.5, "正文"),
    ("--color-text-dim", "--color-bg", 4.5, "次级文字"),
    ("--color-text-mute", "--color-bg", 4.5, "三级说明"),
    ("--color-accent", "--color-bg", 4.5, "链接/焦点"),
    ("--color-pass", "--color-bg", 3.0, "四态色点（非文本）"),
    ("--color-pass-exception", "--color-bg", 3.0, "四态色点（非文本）"),
    ("--color-fail", "--color-bg", 3.0, "四态色点（非文本）"),
    ("--color-unknown", "--color-bg", 3.0, "四态色点（非文本）"),
    # 667 新增：四态色在 667 起**也用作文字**（判决表的状态标签 `.state-pill`），
    # 文字就不再是"图形阈值 3.0"而是 **4.5**；且它压在卡面（surface）上而不是页面底（bg）上。
    ("--color-pass", "--color-surface", 4.5, "状态标签文字"),
    ("--color-pass-exception", "--color-surface", 4.5, "状态标签文字"),
    ("--color-fail", "--color-surface", 4.5, "状态标签文字"),
    ("--color-unknown", "--color-surface", 4.5, "状态标签文字"),
    ("--color-accent", "--color-surface", 4.5, "表头排序文字"),
]


def parse_tokens(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", text):
        out[m.group(1)] = m.group(2)[:7]
    return out


def _block(text: str, selector: str) -> str:
    """取出某个选择器后**第一段** `{...}` 的内容（令牌文件里没有嵌套花括号）。"""
    m = re.search(re.escape(selector) + r"\s*\{", text)
    if not m:
        return ""
    end = text.find("}", m.end())
    return text[m.end():end] if end > 0 else ""


def parse_token_blocks(text: str) -> dict[str, dict[str, str]]:
    """**分主题**解析令牌。

    667 修正：旧版 `parse_tokens` 对同名变量**取最后一次出现**，而文件里浅色块写在后面
    ⇒ `--check` 实际**只验了浅色主题**，深色主题从未被算过（666 B1 却声称"深浅两套都过"）。
    这里按块分开取，两套都算。
    """
    return {
        "dark": parse_tokens(_block(text, ":root")),
        "light": parse_tokens(_block(text, "html[data-theme='light']"))
                 or parse_tokens(_block(text, 'html[data-theme="light"]')),
    }


def check_contrast() -> tuple[bool, list[dict[str, Any]]]:
    if not TOKENS.is_file():
        return False, [{"error": "缺少 css/design-tokens.css"}]
    blocks = parse_token_blocks(TOKENS.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    ok = True
    for theme in ("dark", "light"):
        tk = blocks.get(theme) or {}
        if not tk:
            rows.append({"fg": theme, "bg": theme, "ratio": None, "need": 0,
                         "ok": False, "label": "主题块", "note": f"{theme} 主题令牌块未找到"})
            ok = False
            continue
        for fg, bg, need, label in CONTRAST_RULES:
            f, b = tk.get(fg), tk.get(bg)
            if not f or not b:
                rows.append({"fg": f"[{theme}] {fg}", "bg": bg, "ratio": None, "need": need,
                             "ok": False, "label": label, "note": "令牌缺失"})
                ok = False
                continue
            ratio = contrast(f, b)
            passed = ratio >= need
            ok = ok and passed
            rows.append({"fg": f"[{theme}] {fg}", "bg": bg, "ratio": ratio, "need": need,
                         "ok": passed, "label": label})
    return ok, rows


# ── 校验 ────────────────────────────────────────────────────────────────────
def check_schemas() -> tuple[bool, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    ok = True
    for name, required in SCHEMAS.items():
        p = DATA / name
        if not p.is_file():
            rows.append({"file": name, "ok": False, "note": "文件缺失"})
            ok = False
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            rows.append({"file": name, "ok": False, "note": f"JSON 非法：{e}"})
            ok = False
            continue
        missing = [k for k in required if k not in d]
        rows.append({"file": name, "ok": not missing, "note": ("缺字段：" + ",".join(missing)) if missing else "schema OK"})
        ok = ok and not missing
    return ok, rows


def check_index() -> tuple[bool, list[dict[str, Any]]]:
    """index.json 是否与实际 data 文件一致（漂移可见）。"""
    rows: list[dict[str, Any]] = []
    if not INDEX.is_file():
        return False, [{"file": "index.json", "ok": False, "note": "未生成（跑 --build）"}]
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    ok = True
    for name, meta in (idx.get("files") or {}).items():
        p = DATA / name
        if not p.is_file():
            rows.append({"file": name, "ok": False, "note": "索引里有但磁盘上没有"})
            ok = False
            continue
        actual = sha256_file(p)
        same = actual == meta.get("sha256")
        ok = ok and same
        rows.append({"file": name, "ok": same, "note": "哈希一致" if same else "已漂移（需 --build）"})
    for p in sorted(DATA.glob("*.json")):
        if p.name == "index.json":
            continue
        if p.name not in (idx.get("files") or {}):
            rows.append({"file": p.name, "ok": False, "note": "磁盘上有但索引里没有"})
            ok = False
    return ok, rows


#: `web/card.js` 真正会读的字段（数据与页面的**契约**）。少一个 ⇒ 页面某处会渲染成 undefined
CARD_CONTRACT: tuple[str, ...] = ("id", "path", "meta", "claim", "boundary", "verdict",
                                  "prerequisites", "props", "evidence", "selfcheck",
                                  "related_verified_same_domain", "misconceptions")


def check_cards_contract() -> tuple[bool, list[dict[str, Any]]]:
    """`cards.json` 与 `card.js` 的字段契约（页面读不到的字段 = 静默 undefined，必须挡在构建期）。"""
    rows: list[dict[str, Any]] = []
    p = DATA / "cards.json"
    if not p.is_file():
        return False, [{"file": "cards.json", "ok": False, "note": "未生成（跑 --all）"}]
    d = json.loads(p.read_text(encoding="utf-8"))
    cards = d.get("cards") or {}
    ok = True
    if not cards:
        return False, [{"file": "cards.json", "ok": False, "note": "cards 为空"}]
    for cid, c in cards.items():
        missing = [k for k in CARD_CONTRACT if k not in c]
        bad_sc = [i for i, s in enumerate(c.get("selfcheck") or [])
                  if not (s.get("q") and s.get("a") and s.get("source"))]
        bad_ev = [e.get("id") for e in (c.get("evidence") or []) if not e.get("exists")]
        if missing or bad_sc or bad_ev:
            ok = False
            rows.append({"file": cid, "ok": False, "note": (
                (f"缺字段 {missing} " if missing else "")
                + (f"自测题缺 q/a/source：{bad_sc} " if bad_sc else "")
                + (f"证据卡缺失：{bad_ev}" if bad_ev else ""))})
    if ok:
        rows.append({"file": "cards.json", "ok": True,
                     "note": f"{len(cards)} 张卡全部满足契约（含自测题 q/a/source）"})
    return ok, rows


def check_wiring() -> tuple[bool, list[dict[str, Any]]]:
    """三个页面必须：① 引用设计令牌 ② 引用组件出口 ③ 用上 <qy-nav>（统一导航）。"""
    rows: list[dict[str, Any]] = []
    ok = True
    for page in PAGES:
        p = WEB / page
        if not p.is_file():
            rows.append({"page": page, "ok": False, "note": "页面缺失"})
            ok = False
            continue
        t = p.read_text(encoding="utf-8")
        has_tokens = "css/design-tokens.css" in t
        has_components = "components/index.js" in t or "components/qy-" in t
        has_nav = "<qy-nav" in t
        good = has_tokens and has_components and has_nav
        ok = ok and good
        rows.append({"page": page, "ok": good, "note": ",".join(
            ([] if has_tokens else ["缺 tokens"]) +
            ([] if has_components else ["缺组件"]) +
            ([] if has_nav else ["缺 <qy-nav>"])) or "接线 OK"})
    for f in ("index.js", "qy-nav.js", "qy-card.js", "qy-panel.js", "qy-button.js",
              "qy-tag.js", "qy-status.js"):
        if not (COMPONENTS / f).is_file():
            rows.append({"page": f"components/{f}", "ok": False, "note": "组件缺失"})
            ok = False
    return ok, rows


# ── 构建 ────────────────────────────────────────────────────────────────────
def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return "\n".join(ln.rstrip() for ln in text.splitlines() if ln.strip())


def minify_js(text: str) -> str:
    """保守压缩：只删**整行注释**、空行、行尾空白。不动字符串/正则里的任何东西。"""
    out: list[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("//"):
            continue
        out.append(ln.rstrip())
    return "\n".join(out)


def build(dist_only: bool = False) -> dict[str, Any]:
    """`dist_only=True`（674a）：**跳过数据生成器与 index.json 写入**，只产出 `dist/`。

    为什么需要这个模式：`--build` 的第 1 步会重跑数据生成器，**重写受跟踪的
    `web/data/*.json`**（实测 5 个受跟踪文件 + 23 个新文件）。CI 的 pytest job 需要
    `web/dist/` 才能跑 `test_dist_perf_670c2`（4 项），但那一步会把工作树里的 web/data 改脏
    ⇒ ① 违反"不碰 web/ 前端"的红线；② 本地同树跑前端自测会因此 3/23 红（实测）。
    `dist_only` 只**读** `web/data/`（`dist/data/` 是复制，不写回源），故对源零改动。
    """
    rep: dict[str, Any] = {"steps": [], "files": {}}
    if not dist_only:
        for cmd in GENERATORS:
            rc, tail = run(cmd)
            rep["steps"].append({"cmd": " ".join(Path(cmd[1]).name for cmd in [cmd]) + " " + " ".join(cmd[2:]),
                                 "rc": rc, "tail": tail[-120:]})

    files: dict[str, Any] = {}
    for p in sorted(DATA.glob("*.json")):
        if p.name == "index.json":
            continue
        files[p.name] = {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
    if not dist_only:
        (DATA / "index.json").write_text(json.dumps({
            "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
            "tool": "tools/web_data_pipeline_656.py",
            "files": files,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    rep["files"] = files

    # dist：保守压缩 + 版本号 + manifest
    DIST.mkdir(parents=True, exist_ok=True)
    node = shutil.which("node")
    items: dict[str, Any] = {}
    for rel in ASSETS:
        src = WEB / rel
        if not src.is_file():
            items[rel] = {"present": False}
            continue
        raw = src.read_text(encoding="utf-8")
        mini = minify_css(raw) if rel.endswith(".css") else (minify_js(raw) if rel.endswith(".js") else raw)
        ok_mini = True
        if rel.endswith(".js") and node:
            tmp = DIST / (rel.replace("/", "_") + ".check.mjs")
            tmp.write_text(mini, encoding="utf-8", newline="\n")
            r = subprocess.run([node, "--check", str(tmp)], capture_output=True, text=True, check=False)
            ok_mini = r.returncode == 0
            tmp.unlink(missing_ok=True)
        final = mini if ok_mini else raw
        dst = DIST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(final, encoding="utf-8", newline="\n")
        digest = sha256_file(dst)
        items[rel] = {"present": True, "raw_bytes": len(raw.encode("utf-8")),
                      "bytes": dst.stat().st_size, "sha256": digest,
                      "version": digest[:8], "minified": bool(ok_mini and final == mini)}
    # 670c：dist 也要带上页面 fetch 的数据。
    # 病（670c 实测）：ASSETS 只列 html/css/js ⇒ dist/*.html 里的 fetch('data/*.json')
    # 全部 404，dist 版本页面数据永远加载不出来。这里把 web/data/**.json 原样复制过去。
    data_files = 0
    for p in sorted(DATA.rglob("*.json")):
        # 注意：变量名不能叫 rel —— 上面的 ASSETS 循环里 rel 已被用作 str（mypy 会报类型冲突）
        drel = p.relative_to(DATA)
        dst = DIST / "data" / drel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(p.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        data_files += 1

    DIST_MANIFEST.write_text(json.dumps({
        "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": "tools/web_data_pipeline_656.py",
        "assets": items,
        "data_files": data_files,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    rep["dist"] = {"manifest": "dist/manifest.json", "assets": len(items), "data_files": data_files,
                   "minified": sum(1 for v in items.values() if v.get("minified")),
                   "raw_total": sum(v.get("raw_bytes", 0) for v in items.values()),
                   "dist_total": sum(v.get("bytes", 0) for v in items.values())}
    return rep


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 C3/C4：前端数据管线与构建")
    ap.add_argument("--build", action="store_true", help="跑齐生成器 + 写 index.json + 产出 dist/")
    ap.add_argument("--dist-only", action="store_true",
                    help="674a：只产出 dist/（**不**重跑数据生成器、**不**写 web/data/index.json）——"
                         "给 CI 补 dist 用，对 web/ 源码与数据零改动")
    ap.add_argument("--check", action="store_true", help="只读校验（schema / 漂移 / 对比度 / 接线）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.build or a.dist_only:
        rep = build(dist_only=a.dist_only)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print(f"[pipeline656] 生成步骤 {len(rep['steps'])} 个；data 文件 {len(rep['files'])} 个"
                  f"；dist 资源 {rep['dist']['assets']} 个（压缩 {rep['dist']['minified']}）"
                  f"　{rep['dist']['raw_total']}B → {rep['dist']['dist_total']}B")
        return 0

    ok_schema, rows_schema = check_schemas()
    ok_index, rows_index = check_index()
    ok_contrast, rows_contrast = check_contrast()
    ok_wire, rows_wire = check_wiring()
    ok_cards, rows_cards = check_cards_contract()
    payload = {
        "schema": rows_schema, "index": rows_index,
        "contrast": rows_contrast, "wiring": rows_wire, "cards_contract": rows_cards,
        "ok": ok_schema and ok_index and ok_contrast and ok_wire and ok_cards,
    }
    if a.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["ok"] else 1
    for name, rows, okk in (("schema", rows_schema, ok_schema), ("index/drift", rows_index, ok_index),
                            ("WCAG AA 对比度", rows_contrast, ok_contrast),
                            ("组件接线", rows_wire, ok_wire),
                            ("卡片数据契约", rows_cards, ok_cards)):
        print(f"── {name}：{'PASS' if okk else 'FAIL'}")
        for r in rows:
            if not r.get("ok", True) or name == "WCAG AA 对比度":
                note = r.get("note")
                if not note:
                    note = "%s:1 (需 ≥%s) %s" % (r.get("ratio"), r.get("need"), r.get("label"))
                key = r.get("file") or r.get("page") or r.get("fg")
                print("   %s %s · %s" % ("ok" if r.get("ok") else "FAIL", key, note))
    print(f"[pipeline656] --check：{'PASS' if payload['ok'] else 'FAIL'}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
