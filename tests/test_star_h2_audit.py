"""锁定 star_h2_audit（星级格 / H2 分层）的行为，防回潮。"""
import star_h2_audit as sa


def _chapter(tmp_path, name="chT_demo.md", lines=None):
    book = tmp_path / "Book"
    (book / "part").mkdir(parents=True, exist_ok=True)
    f = book / "part" / name
    f.write_bytes(("\n".join(lines or []) + "\n").encode("utf-8"))
    return book, f


def test_h2_title_strips_markers_and_badges():
    assert sa._h2_title("⑪ 常见误区（版本 / ABI）") == "常见误区"
    assert sa._h2_title('⑬ 关键提案 <span class="badge badge-std">标准</span>') == "关键提案"
    assert sa._h2_title("3.2 初始化顺序") == "初始化顺序"


def test_classify_splits_main_and_ext(tmp_path, monkeypatch):
    book, _ = _chapter(tmp_path, lines=[
        "# 章标题",
        "## ① 核心机制",
        "## ② 对象模型",
        "## ⑪ 常见误区",
        "## FAQ",
        "## 附录 D5：真实基准",
        "## 相关章节",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    cls = sa.h2_classify()
    got = cls["part/chT_demo.md"]
    assert got["main"] == ["核心机制", "对象模型"], "机制类应归主线"
    assert "常见误区" in got["ext"] and "FAQ" in got["ext"]
    assert any(t.startswith("附录") for t in got["ext"]), "附录* 应归扩展"
    assert "相关章节" in got["ext"], "固定尾三件套应归扩展"


def test_classify_marks_question_section_as_ext(tmp_path, monkeypatch):
    """「我们真正要回答的问题」按关键词归扩展；但 h2_demote 会保留章首首个 H2 不降
    （否则 H3 无父级）——两者分工不同，此处锁定 classify 侧语义。"""
    book, _ = _chapter(tmp_path, name="chU_demo.md", lines=[
        "# 章标题",
        "## 我们真正要回答的问题",
        "## ① 机制",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    cls = sa.h2_classify()
    assert cls["part/chU_demo.md"]["main"] == ["机制"]
    assert cls["part/chU_demo.md"]["ext"] == ["我们真正要回答的问题"]


def test_fix_star_normalizes_bracket_style(tmp_path, monkeypatch):
    book, f = _chapter(tmp_path, name="chV_demo.md", lines=[
        "> **示例 1** [难度 ★★★☆☆] [主题：概念 <span class=\"badge badge-impl\">实现</span>]",
        "",
        "```cpp title=\"示例 1 · ★★★☆☆\"",
        "int main() {}",
        "```",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    sa.star_scan(fix=True)
    out = f.read_bytes().decode("utf-8")
    assert '<span class="badge badge-exp">难度 ★★★☆☆</span> · 概念' in out
    assert "[难度" not in out, "方括号风格必须清零"


def test_fix_star_handles_unclosed_theme_bracket(tmp_path, monkeypatch):
    """变体 B：主题段缺闭合 `]`（全库 71 处），同样要归一。"""
    book, f = _chapter(tmp_path, name="chW_demo.md", lines=[
        "> **示例 2** [难度 ★★☆☆☆] [主题：源码分析（libstdc++）<span class=\"badge badge-impl\">实现</span>",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    sa.star_scan(fix=True)
    out = f.read_bytes().decode("utf-8")
    assert "[难度" not in out
    assert out.count("]") == 0, "残缺的闭合括号应被剥除"


def test_check_star_passes_after_fix(tmp_path, monkeypatch):
    book, _ = _chapter(tmp_path, name="chX_demo.md", lines=[
        '> **示例 3** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 主线',
        "### 练习 1（难度 ★★）",
        '```cpp title="示例 3 · ★☆☆☆☆"',
        "int main() {}",
        "```",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    violations, _ = sa.star_scan(fix=False)
    assert violations == [], f"合规章不应报违规: {violations}"


def test_check_star_flags_bad_exercise(tmp_path, monkeypatch):
    """练习头用 ☆（5 格制）属违规：练习应为实心个数制。"""
    book, _ = _chapter(tmp_path, name="chY_demo.md", lines=[
        "### 练习 2（难度 ★★☆☆☆）",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    violations, _ = sa.star_scan(fix=False)
    assert any(v.startswith("exercise") for v in violations)


def test_demote_is_dry_run_by_default(tmp_path, monkeypatch):
    book, f = _chapter(tmp_path, name="chZ_demo.md", lines=[
        "# 章标题",
        "## ① 主线",
        "## ⑪ 常见误区",
    ])
    monkeypatch.setattr(sa, "BOOK", book)
    before = f.read_bytes()
    sa.h2_demote("chZ_demo", apply_=False)
    assert f.read_bytes() == before, "dry-run 不得写盘"
    sa.h2_demote("chZ_demo", apply_=True)
    out = f.read_bytes().decode("utf-8")
    assert "## ① 主线" in out and "### ⑪ 常见误区" in out, "主线保留 H2、扩展降 H3"
