"""锁定工具链层的真实回归（每一条都对应一次线上/本地事故）。"""
from pathlib import Path

import metrics_snapshot as ms
import run_expected as re_
import compile_triage as ct


# 1) metrics_snapshot.git() 缺 errors="replace"
#    事故：历史提交信息有 GBK 落库的（PowerShell 中文提交），`git log` 输出非 UTF-8
#    字节 → subprocess 读者线程崩溃，commits-since-CHANGELOG 指标**静默变 0**（真数据错误）。
def test_git_survives_non_utf8_history():
    out = ms.git("log", "--oneline", "-50")
    assert isinstance(out, str), "git() 必须始终返回 str（失败返回空串）"


def test_git_returns_empty_on_invalid_command():
    assert ms.git("definitely-not-a-git-subcommand") == ""


# 2) run_expected 运行 exe 未注入编译器目录
#    事故：MinGW 的 std::thread/std::async 程序依赖同目录 libwinpthread-1.dll，
#    调用方 shell 未把 bin 加入 PATH 时，exe 以 0xC0000139 启动失败，被误判 RUN_ERR。
def test_run_env_injects_compiler_dir():
    """编译器目录必须在 PATH 中；已在 PATH（如 CI 的 /usr/bin/g++）则不需重复注入置首。
    语义：注入的是「缺失时补上」，不是「无条件置首」。"""
    env = re_._run_env()
    bindir = str(Path(re_.GCC).resolve().parent)
    assert bindir in env["PATH"], "编译器目录必须出现在 PATH 中"


def test_run_env_does_not_duplicate_entries():
    first = re_._run_env()["PATH"]
    second = re_._run_env()["PATH"]
    assert first == second, "重复调用不应累积插入同一目录"


# 3) compile_triage 基线路径分隔符不一致
#    事故：基线在 Windows 生成含反斜杠、局部扫描用正斜杠 → 字典键错位，
#    把「预存坏块」全误判为 NEW（我的回归），triage 失去意义。
def test_norm_path_unifies_separators():
    assert ct._norm_path("Book\\part03\\ch28.md") == "Book/part03/ch28.md"
    assert ct._norm_path("Book/part03/ch28.md") == "Book/part03/ch28.md"
    assert ct._norm_path("") == ""


def test_fails_by_path_normalizes_keys():
    report = {"failures": [
        {"path": "Book\\part03\\ch28.md", "failures": [{"block": 5, "error": "e5"}]},
    ]}
    assert ct.fails_by_path(report) == {"Book/part03/ch28.md": {5}}


def _run_triage(monkeypatch, *argv):
    """compile_triage.main() 无参（读 sys.argv），测试需注入 argv 后调用。"""
    monkeypatch.setattr("sys.argv", ["compile_triage.py", *argv])
    return ct.main()


def test_preexisting_is_not_reported_as_new(tmp_path, monkeypatch):
    """同一失败块，基线用反斜杠、当前用正斜杠 → 必须判 PREEXISTING（NEW=0, exit 0）。"""
    import json

    base = tmp_path / "base.json"
    after = tmp_path / "after.json"
    base.write_text(json.dumps({"failures": [
        {"path": "Book\\part03\\ch28.md", "failures": [{"block": 5, "error": "e5"}]},
    ]}), encoding="utf-8")
    after.write_text(json.dumps({
        "processed_paths": ["Book/part03/ch28.md"],
        "failures": [
            {"path": "Book/part03/ch28.md", "failures": [{"block": 5, "error": "e5"}]},
        ]}), encoding="utf-8")
    rc = _run_triage(monkeypatch, "--before", str(base), "--after", str(after), "--check")
    assert rc == 0, "路径分隔符差异不得造成假 NEW"


def test_new_regression_is_detected(tmp_path, monkeypatch):
    """基线没有、当前新增的失败块 → 必须 exit 1（门禁价值所在）。"""
    import json

    base = tmp_path / "base.json"
    after = tmp_path / "after.json"
    base.write_text(json.dumps({"failures": []}), encoding="utf-8")
    after.write_text(json.dumps({
        "processed_paths": ["Book/part03/ch28.md"],
        "failures": [
            {"path": "Book/part03/ch28.md", "failures": [{"block": 7, "error": "e7"}]},
        ]}), encoding="utf-8")
    rc = _run_triage(monkeypatch, "--before", str(base), "--after", str(after), "--check")
    assert rc == 1


def test_missing_files_are_reported_cleanly(monkeypatch, capsys):
    """缺失报告文件：必须打印可读提示且**退出码非 0**（门禁不得静默放行），
    同时不得抛 traceback。"""
    rc = _run_triage(monkeypatch, "--before", "nope.json", "--after", "nope.json",
                     "--check")
    err = capsys.readouterr().err
    assert "无法读取报告" in err, f"应给出可读提示，实际 stderr={err!r}"
    assert rc != 0, "报告缺失时门禁必须失败（不得 exit 0 放行）"
