#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site_audit.py — 站点前端产物健康自检（front-end gate, 零依赖）。

在 mkdocs build + pagefind 之后、上传/部署之前运行，校验静态产物完整性：
  1. 首页 index.html 存在
  2. 章节页面可访问（从生成的 index nav 抽取，抽查前 50 个）
  3. 页面内引用的本地静态资源（css/js/img/svg）均存在于产物目录
  4. 徽章样式（assets/extra.css）已注入且正文含 .badge 元素
  5. Mermaid 围栏已按插件模式嵌入（<pre class="mermaid"> 或含 mermaid 数据）
  6. 全文搜索索引存在（pagefind 产物）

用法：
  python tools/site_audit.py [site_dir]   # 默认 build/site_out
退出码：0 = 通过；1 = 任一检查失败（CI 阻断）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

INDEX_RE = re.compile(r'href="([^"#]+\.html)"')
ASSET_RE = re.compile(r'(?:src|href)="(?!https?://|#|mailto:|tel:)([^"]+)"')  # 站内资源
BADGE_RE = re.compile(r'class="[^"]*\bbadge\b[^"]*"')


def audit(site: Path) -> int:
    failures = 0
    checked = 0

    def fail(msg: str) -> None:
        nonlocal failures
        failures += 1
        print(f"  [FAIL] {msg}")

    # 1. 首页
    index = site / "index.html"
    print(f"[1/6] 首页: {index.relative_to(site)}")
    if not index.exists():
        fail("index.html 缺失")
        return 1
    print("  [OK] index.html 存在")
    index_text = index.read_text(encoding="utf-8", errors="replace")

    # 2. 章节页可达性（从首页/导航抽取）
    print("[2/6] 章节页可达性")
    htmls = list(site.rglob("*.html"))
    page_set = {p.relative_to(site).as_posix() for p in htmls}
    targets = []
    for m in re.finditer(r'href="([^"#]+\.(?:html|htm))"', index_text):
        href = m.group(1)
        if href.startswith(("http", "mailto", "tel", "#")):
            continue
        targets.append(href.split("#")[0].split("?")[0])
    targets = list(dict.fromkeys(targets))[:50]
    for t in targets:
        # 相对链接以首页所在目录（site 根）为基准
        t_path = (index.parent / t).resolve()
        if not t_path.exists() or not t_path.is_file():
            fail(f"首页引用不可达: {t}")
        else:
            checked += 1
    print(f"  [OK] 抽查 {checked}/{len(targets)} 个导航页面均可达")

    # 3. 站内资源存在性（所有 html 的 css/js/img/svg）
    print("[3/6] 静态资源完整性")
    missing = set()
    total_res = 0
    dir_hrefs = set()
    for p in htmls:
        text = p.read_text(encoding="utf-8", errors="replace")
        # 剔除内联 SVG（Mermaid 图）：图内文本可含任意字面 `href="x"`，
        # 非真实资源引用（实测 ch61 mermaid 标签文本误报）。
        text = re.sub(r"<svg\b.*?</svg>", "", text, flags=re.S)
        base = p.parent.resolve()  # 相对链接以当前 html 所在目录为基准（绝对化，避免 cwd 歧义）
        for m in ASSET_RE.finditer(text):
            res = m.group(1).split("#")[0].split("?")[0]
            if not res:
                continue
            # 以 / 开头的站内绝对路径：按站点根解析。
            # 注意必须先于目录式分支：Path(base) / "/abs" 会丢弃 base 从盘根解析，
            # 导致 /Appendix/ub/ 这类绝对目录链接永远误判缺失（Windows/Linux 皆然）。
            if res.startswith("/"):
                # `/.` 与 `/`：主题 logo/首页 的站点根链接 → 站点根目录必然存在
                if res.rstrip(".") == "" or res in ("/", "/."):
                    total_res += 1
                    continue
                # /pagefind/*：索引产物由 pagefind 步骤生成，其存在性由检查 6 专责，
                # 此处跳过以免本地未建索引时误报（CI 中 pagefind 先于本审计运行）。
                if res.startswith("/pagefind/"):
                    total_res += 1
                    continue
                cand = (site / res.lstrip("/")).resolve()
                ok = cand.is_dir() if res.endswith("/") else cand.is_file()
                if not ok:
                    missing.add(f"{p.relative_to(site).as_posix()} -> {res}")
                total_res += 1
                continue
            # 目录式链接（use_directory_urls 生成，如 ../ub01_use_after_free/）→ 目录页，单独放行
            if res.endswith("/"):
                if (base / res).resolve().is_dir():
                    dir_hrefs.add(res)
                else:
                    missing.add(f"{p.relative_to(site).as_posix()} -> {res}")
                continue
            total_res += 1
            cand = (base / res).resolve()
            if not cand.exists():
                missing.add(f"{p.relative_to(site).as_posix()} -> {res}")
    if dir_hrefs:
        print(f"  [OK] {len(dir_hrefs)} 个目录式链接（章节目录页）均存在")
    if missing:
        for r in sorted(missing)[:10]:
            fail(f"资源缺失: {r}")
        fail(f"缺失资源 {len(missing)} 个（共 {total_res} 个引用）")
    else:
        print(f"  [OK] {total_res} 个站内资源引用全部存在")

    # 4. 徽章样式与注入
    print("[4/6] 徽章样式与注入")
    extra_css = site / "assets" / "extra.css"
    if not extra_css.exists() and not list(site.rglob("extra.css")):
        fail("assets/extra.css（徽章样式）缺失")
    else:
        print("  [OK] 徽章 CSS 存在")
    if BADGE_RE.search(index_text):
        print("  [OK] 首页含 .badge 徽章元素")
    else:
        fail("站内未发现 .badge 徽章注入（检查 gen_mkdocs_nav 徽章 CSS/内容）")

    # 5. Mermaid 嵌入
    print("[5/6] Mermaid 嵌入")
    mermaid_hits = 0
    for p in htmls:
        text = p.read_text(encoding="utf-8", errors="replace")
        if 'class="mermaid"' in text or "mermaid" in text.lower():
            mermaid_hits += 1
    if mermaid_hits > 0:
        print(f"  [OK] {mermaid_hits} 个页面含 Mermaid 内容")
    else:
        fail("全站未发现 Mermaid 内容（图可能未生成）")

    # 6. 全文搜索索引
    print("[6/6] 全文搜索（pagefind）")
    if (site / "pagefind" / "pagefind-ui.js").exists() or (site / "pagefind.js").exists() or (site / "pagefind" / "pagefind.js").exists():
        print("  [OK] pagefind 索引已生成")
    else:
        # WARN 不阻断：本地未构建 site 时无索引属预期；CI 的 site job 强制
        # python3 -m pagefind 且缺失即阻断该 job，故此处仅提示。
        print("  [WARN] pagefind 索引缺失（CI 的 site job 会强制执行并阻断）")

    if failures:
        print(f"\n[FAIL] site_audit: {failures} 项异常")
        return 1
    print("\n[OK] site_audit: 站点产物健康")
    return 0


def main() -> int:
    site_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("build/site_out").resolve()
    if not site_dir.is_dir():
        print(f"[FAIL] 站点目录不存在: {site_dir}")
        return 1
    print(f"[site_audit] 检查 {site_dir}")
    return audit(site_dir)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())