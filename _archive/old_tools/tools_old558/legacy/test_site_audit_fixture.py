# -*- coding: utf-8 -*-
"""site_audit 自测：构造最小站点，验证 PASS 与 FAIL 两条路径。"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path("build/fixture_site")
GOOD = ROOT / "good"
BAD = ROOT / "bad"
shutil.rmtree(ROOT, ignore_errors=True)

# ---------- GOOD：完整站点 ----------
for p in ["index.html", "part01/ch01.html", "assets/extra.css", "sub/page.html"]:
    f = GOOD / p
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("", encoding="utf-8")
(GOOD / "index.html").write_text(
    '<a href="part01/ch01.html">c1</a> '
    '<a href="assets/extra.css">css</a> '
    '<span class="badge badge-std">x</span> '
    '<pre class="mermaid">flowchart LR</pre> pagefind-index',
    encoding="utf-8",
)
# 从 part01/ch01.html 上溯一层到 good 根，再进入 Appendix/ub（目录式链接）
(GOOD / "part01/ch01.html").write_text('<a href="../Appendix/ub/">dir</a>', encoding="utf-8")
(GOOD / "Appendix/ub").mkdir(parents=True, exist_ok=True)

# ---------- BAD：缺失资源 + 无徽章 ----------
(BAD / "index.html").parent.mkdir(parents=True, exist_ok=True)
(BAD / "index.html").write_text('<a href="missing.css">x</a> 无 badge 无 mermaid', encoding="utf-8")

# ---------- 运行 ----------
for name, path in [("GOOD", GOOD), ("BAD", BAD)]:
    r = subprocess.run([sys.executable, "tools/site_audit.py", str(path)],
                       capture_output=True, text=True, encoding="utf-8")
    print(f"===== {name} exit={r.returncode} =====")
    print(r.stdout.strip()[-400:])
    ok = (name == "GOOD" and r.returncode == 0) or (name == "BAD" and r.returncode == 1)
    if not ok:
        sys.exit(f"FAIL: {name} 行为与预期不符")
    print(f"===== {name} 行为正确 =====\n")
print("[PASS] site_audit 自测通过")