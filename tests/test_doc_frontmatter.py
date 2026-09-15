"""doc_frontmatter 回归锁（498 任务 1）。

锁三件易错事：①字段推导（编号/archive/无编号 slug）②幂等（第二次 apply 改动 0）
③**原内容与行尾零改动**（字节级插入；CRLF 文件不得被归一成 LF——494 的同款教训）。
测试全部走 tmp_path，不触碰真实文档目录。
"""
from __future__ import annotations

from pathlib import Path

import doc_frontmatter as df


def test_build_frontmatter_numbered(tmp_path: Path):
    p = tmp_path / "415_阙疑知识图谱推理_从静态relations到可推理知识系统.md"
    p.write_text("x", encoding="utf-8")
    fm = df.build_frontmatter(p)
    assert fm["id"] == "415"
    assert fm["title"] == "阙疑知识图谱推理 从静态relations到可推理知识系统"
    assert fm["status"] == "active" and fm["type"] == "architecture-note"
    assert len(fm["created_at"]) == 10 and fm["created_at"][4] == "-"


def test_build_frontmatter_archive(tmp_path: Path):
    p = tmp_path / "archive_312_backup_pre_compress.md"
    p.write_text("x", encoding="utf-8")
    fm = df.build_frontmatter(p)
    assert fm["id"] == "archive-312" and fm["status"] == "archived"
    assert fm["title"] == "backup pre compress"


def test_archive_with_letter_suffix_keeps_it(tmp_path: Path):
    """回归锁：`archive_365B_…` 的字母后缀属于编号（id=archive-365B），不得漏进 title。"""
    p = tmp_path / "archive_365B_独立红队Agent_投喂提示词.md"
    p.write_text("x", encoding="utf-8")
    fm = df.build_frontmatter(p)
    assert fm["id"] == "archive-365B", fm
    assert fm["status"] == "archived"
    assert fm["title"].startswith("独立红队Agent"), fm["title"]


def test_build_frontmatter_slug_for_unnumbered(tmp_path: Path):
    p = tmp_path / "README_INDEX.md"
    p.write_text("x", encoding="utf-8")
    fm = df.build_frontmatter(p)
    assert fm["id"] == "README_INDEX" and fm["status"] == "active"


def test_apply_is_idempotent_and_content_preserved(tmp_path: Path):
    doc = tmp_path / "410_demo_note.md"
    original = "# 标题\n\n正文第一行\n第二行\n"
    doc.write_bytes(original.encode("utf-8"))
    added1, skipped1 = df.process(tmp_path, apply=True)
    assert (added1, skipped1) == (1, 0)
    added2, skipped2 = df.process(tmp_path, apply=True)      # 幂等
    assert (added2, skipped2) == (0, 1)
    out = doc.read_bytes().decode("utf-8")
    assert out.startswith("---\nid: 410\n")
    assert out.endswith(original), "原有内容必须一字不动地保留在末尾"
    assert out.count("---\n") == 2, "frontmatter 只有一对分隔符"


def test_crlf_preserved(tmp_path: Path):
    doc = tmp_path / "420_crlf.md"
    doc.write_bytes("# 标题\r\n正文\r\n".encode("utf-8"))
    df.process(tmp_path, apply=True)
    raw = doc.read_bytes()
    # 判据：**没有孤立 LF**（每个 \n 前都必须是 \r）——若走 read_text/write_text 归一，会留下裸 LF
    assert raw.count(b"\n") == raw.count(b"\r\n"), "原 CRLF 行尾不得被改写（出现裸 LF）"
    assert raw.startswith(b"---\r\nid: 420\r\n"), "frontmatter 须沿用原文件行尾"


def test_existing_frontmatter_skipped(tmp_path: Path):
    doc = tmp_path / "430_with_fm.md"
    doc.write_bytes("---\nid: 430\n---\n正文\n".encode("utf-8"))
    added, skipped = df.process(tmp_path, apply=True)
    assert (added, skipped) == (0, 1)
    assert doc.read_bytes().decode("utf-8").count("id: 430") == 1


def test_rendered_frontmatter_is_valid_yaml(tmp_path: Path):
    """硬化回归（528 任务5）：注入的 frontmatter 必须能被 yaml.safe_load 解析为映射。

    498 只校验了「内容零改动 / 幂等」，未校验注入体本身是合法 YAML——若某字段值含
    `:`/`#` 等特殊字符，`render` 的 `k: v` 拼接可能产出歧义 YAML，下游文档生命周期工具
    消费时会炸。本测试补上这层校验。
    """
    import yaml

    doc = tmp_path / "412_valid_yaml.md"
    doc.write_text("# 标题\n正文\n", encoding="utf-8")
    df.process(tmp_path, apply=True)
    raw = doc.read_bytes().decode("utf-8")
    fm_block = raw.split("---", 2)[1]          # 第一对 `---` 之间的内容
    parsed = yaml.safe_load(fm_block)
    assert isinstance(parsed, dict), f"frontmatter 必须是映射，实际：{parsed!r}"
    for k in ("id", "title", "status", "type", "created_at"):
        assert k in parsed, f"缺字段 {k}"
    assert parsed["type"] == "architecture-note"
