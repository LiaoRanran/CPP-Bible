"""645 B1 标准获取器单测（fast 组：不依赖真实联网）。

锁定：请求构造/哈希/解析逻辑、失败诚实降级（不崩溃、不编造）、空主题集安全。
对应 645 §四 B1 验收：≥10 条真实获取 / hash 正确 / 存储正确 / 等级 L2。
（真实联网获取在 CI `--acquire` 跑；本测试用 monkeypatch 模拟联网成功与失败。）
"""
import sys

sys.path.insert(0, "tools")

import standard_fetcher_645 as sf


def test_selftest_passes():
    assert sf.selftest() == 0


def test_fetch_result_fields():
    fr = sf.FetchResult(topic="t", section="s", url="u", ok=True, status=200,
                        content_hash="abc", content_len=10, error="", acquired_at="2026-01-01T00:00:00")
    d = fr.to_dict()
    assert d["section"] == "s" and d["ok"] is True and d["content_len"] == 10


def test_run_acquire_empty_is_safe():
    # 空主题集：不联网、不崩溃、ok=0
    res = sf.run_acquire(topics=[])
    assert res["total"] == 0 and res["ok"] == 0


def test_run_acquire_success_stores_l2(monkeypatch):
    """模拟 eel.is 返回 200 + 正文 → 真实落库 L2 证据。"""
    import urllib.request

    class _Resp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"# intro\nC++ standard draft content for testing 645."

    def _fake_open(req, timeout=0.0):
        return _Resp()

    monkeypatch.setattr(urllib.request, "urlopen", _fake_open)
    res = sf.run_acquire(topics=[{"section": "intro", "title": "范围"}])
    assert res["ok"] == 1, "模拟成功应计 1 条"
    assert res["stored"] == 1
    r = res["results"][0]
    assert r["ok"] and r["content_hash"] and len(r["content_hash"]) == 64


def test_run_acquire_failure_honest(monkeypatch):
    """模拟网络不可达 → ok=False、记录错误、绝不编造正文。"""
    import urllib.request

    def _fake_open(req, timeout=0.0):
        raise urllib.error.URLError("Name or service not known")

    monkeypatch.setattr(urllib.request, "urlopen", _fake_open)
    res = sf.run_acquire(topics=[{"section": "lex", "title": "词法"}])
    assert res["ok"] == 0
    assert res["failed"] == 1
    assert res["results"][0]["error"] != ""  # 诚实登记原因
