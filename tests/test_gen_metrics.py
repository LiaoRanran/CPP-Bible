"""锁定 gen_metrics._fix_prose 的真实回归：整文件行尾伪 diff。"""
import gen_metrics as gm


def test_fix_prose_updates_number_and_preserves_bytes(tmp_path, monkeypatch):
    """事故：初版用文本模式 open(...,'w') 回写 → Windows 把 \\n 翻成 \\r\\n，
    未触及的行也全部改变，产出 362 行伪 diff。改为原始字节读写后修复。"""
    monkeypatch.setattr(gm, "ROOT", tmp_path)
    doc = tmp_path / "README.md"
    doc.write_bytes(
        "# T\r\n\r\n> 147 章 · 9999 个 cpp 代码块\r\n\r\n其它行保持原样\r\n".encode("utf-8"))
    schema = {"checks": [
        {"file": "README.md", "regex": r"(\d+) 个 cpp 代码块", "expect": ["cpp_blocks"]},
    ]}
    changed = gm._fix_prose(schema, {"cpp_blocks": 7515})
    raw = doc.read_bytes()
    assert "7515 个 cpp 代码块".encode("utf-8") in raw, "数字应被回填"
    assert raw.count(b"\n") == raw.count(b"\r\n"), "不得引入裸 LF（行尾翻转）"
    assert "\r\n\r\n其它行保持原样\r\n".encode("utf-8") in raw, "未触及内容必须逐字节不变"
    assert changed and "README.md" in changed[0]


def test_fix_prose_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(gm, "ROOT", tmp_path)
    doc = tmp_path / "README.md"
    doc.write_bytes("> 7515 个 cpp 代码块\r\n".encode("utf-8"))
    schema = {"checks": [
        {"file": "README.md", "regex": r"(\d+) 个 cpp 代码块", "expect": ["cpp_blocks"]},
    ]}
    gm._fix_prose(schema, {"cpp_blocks": 7515})
    first = doc.read_bytes()
    second_run = gm._fix_prose(schema, {"cpp_blocks": 7515})
    assert doc.read_bytes() == first, "二次运行不得改动文件"
    assert second_run == [], "值已一致时不应产生变更描述"


def test_fix_prose_warns_on_regex_miss(tmp_path, monkeypatch):
    """正则失配 = 文档结构漂移，必须告警而不是静默跳过。"""
    monkeypatch.setattr(gm, "ROOT", tmp_path)
    doc = tmp_path / "README.md"
    doc.write_bytes("> 完全不同的写法\r\n".encode("utf-8"))
    schema = {"checks": [
        {"file": "README.md", "regex": r"(\d+) 个 cpp 代码块", "expect": ["cpp_blocks"]},
    ]}
    changed = gm._fix_prose(schema, {"cpp_blocks": 7515})
    assert changed and "未匹配" in changed[0]
