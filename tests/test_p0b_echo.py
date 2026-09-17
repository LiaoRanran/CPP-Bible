"""470 P0-B → 472 P1-2 回归锁（452 E05 cat 式证据）。

状态迁移：470 落地为 **experimental**（零 Finding、门禁零影响）→ 472 P1-2 **升 warn**
（依据：v5 复测实证 exp 零输出时卡照样 confirm 直推 verified；存量 56 卡 0 命中，升格零误伤）。
"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import pytest

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


def test_promoted_to_warn_rule(sb: Path):
    """472 P1-2 升格：experimental → 注册为 **warn**（可见化，但不阻断卡）。

    旧断言（`not in ids`）是 470 experimental 阶段的锁，升格后必须同步——
    否则「升了格但测试仍锁未注册」会让套件长红，掩盖真实回归。
    """
    rule = next((r for r in ge.RULES if r.id == "EV-FIXTURE-NO-ECHO-DATA"), None)
    assert rule is not None, "升格后必须注册进 RULES（--exp-scan 仅留作手工排查）"
    assert rule.severity == "warn", f"升格只到 warn（存量不可阻断）：{rule.severity}"
    (sb / "cat2.cpp").write_text(
        "#include <cstdio>\n#include <fstream>\n#include <string>\n"
        "int main(){ std::ifstream f(\"data.txt\"); std::string line;\n"
        "  while (std::getline(f, line)) std::printf(\"%s\\n\", line.c_str()); }\n",
        encoding="utf-8")
    _card(sb, "EV-ECHO2", "cat2.cpp")
    findings = ge.run(include_advice=False)
    hits = [f for f in findings if f.rule_id == "EV-FIXTURE-NO-ECHO-DATA"]
    assert hits, "cat 式证据必须产出 Finding（否则等于没升格，P1-2 失效）"
    assert all(f.severity == "warn" for f in hits), "命中不得升 block（存量 0 命中，先观察）"
