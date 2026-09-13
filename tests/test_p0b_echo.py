"""470 P0-B 回归锁（452 E05 cat 式证据，experimental 扫描：只记录不参与门禁）。"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge


CARD_TMPL = (
    "---\nid: {cid}\nserves: []\nhypothesis: h\nkind: run\n"
    "command: 'g++ {fx} -o a.exe && ./a.exe'\nfixture: {fx}\n"
    "artifact: a.asm\nartifact_sha256: " + "0" * 64 + "\n"
    "verdict: confirm\nfalsification: f\n---\n")


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "evidence").mkdir()
    (tmp_path / "data.txt").write_text("result=42\n", encoding="utf-8")
    return tmp_path


def _card(sb: Path, cid: str, fx: str) -> Path:
    p = sb / "evidence" / f"{cid}.md"
    p.write_text(CARD_TMPL.format(cid=cid, fx=fx), encoding="utf-8")
    return p


def test_echo_data_detected(sb: Path):
    """正例（E05 形态）：ifstream → getline → printf 原样打印 → 命中。"""
    (sb / "cat.cpp").write_text(
        "#include <cstdio>\n#include <fstream>\n#include <string>\n"
        "int main(){ std::ifstream f(\"data.txt\"); std::string line;\n"
        "  while (std::getline(f, line)) std::printf(\"%s\\n\", line.c_str()); }\n",
        encoding="utf-8")
    hits = ge.check_fixture_no_echo_data([_card(sb, "EV-ECHO", "cat.cpp")])
    assert hits and hits[0][1] == "cat.cpp"


def test_compute_then_print_passes(sb: Path):
    """阴性：读入后经计算再输出 → 不命中。"""
    (sb / "calc.cpp").write_text(
        "#include <cstdio>\n#include <fstream>\n#include <string>\n"
        "int main(){ std::ifstream f(\"data.txt\"); std::string line;\n"
        "  std::getline(f, line); int v = std::stoi(line.substr(7)) + 1;\n"
        "  std::printf(\"result=%d\\n\", v); }\n",
        encoding="utf-8")
    hits = ge.check_fixture_no_echo_data([_card(sb, "EV-CALC", "calc.cpp")])
    assert hits == [], f"计算型夹具不得命中：{hits}"


def test_external_path_not_scanned(sb: Path):
    """只关心仓库内相对路径：不存在/绝对路径文件不命中。"""
    (sb / "ext.cpp").write_text(
        "#include <cstdio>\n#include <fstream>\n#include <string>\n"
        "int main(){ std::ifstream f(\"/etc/hostname\"); std::string line;\n"
        "  std::getline(f, line); std::printf(\"%s\\n\", line.c_str()); }\n",
        encoding="utf-8")
    assert ge.check_fixture_no_echo_data([_card(sb, "EV-EXT", "ext.cpp")]) == []


def test_not_registered_in_gate_rules(sb: Path):
    """experimental：不得注册进规则集、不产生 Finding（门禁零影响）。"""
    ids = {r.id for r in ge.RULES}
    assert "EV-FIXTURE-NO-ECHO-DATA" not in ids
    (sb / "cat2.cpp").write_text(
        "#include <cstdio>\n#include <fstream>\n#include <string>\n"
        "int main(){ std::ifstream f(\"data.txt\"); std::string line;\n"
        "  while (std::getline(f, line)) std::printf(\"%s\\n\", line.c_str()); }\n",
        encoding="utf-8")
    _card(sb, "EV-ECHO2", "cat2.cpp")
    findings = ge.run(include_advice=False)
    assert all(f.rule_id != "EV-FIXTURE-NO-ECHO-DATA" for f in findings)
