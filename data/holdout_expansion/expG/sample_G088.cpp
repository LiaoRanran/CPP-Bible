// sample_G088
// defect_type: resource_exhaustion
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2019-9514 (https://nvd.nist.gov/vuln/detail/CVE-2019-9514) [http2]
// (authoritative annotation in sample_G088.json)
#include <cstdio>
#include <vector>
// CVE-2019-9514 (有界模拟): HTTP/2 reset flood → 流对象无上限增长
struct H2Stream {
    int  id;
    bool reset_pending;
};

static std::vector<H2Stream*> g_open_streams;

static void h2_on_incoming_stream(int id, bool invalid_request) {
    H2Stream* s = new H2Stream{ id, false };
    g_open_streams.push_back(s);
    if (invalid_request) {
        /* DEFECT */ // 原始缺陷: 服务端为每个待 reset 的流保留/重建对象, 无速率限制
        s->reset_pending = true;
        g_open_streams.push_back(new H2Stream{ id + 1000000, false });   // reset 触发新对象
    }
}

int main() {
    // 攻击者: 10000 次开流 + 立即 reset(有界模拟, 原始为持续洪泛)
    for (int i = 0; i < 10000; ++i)
        h2_on_incoming_stream(i, true);
    std::printf("open_streams=%zu (正确行为: 服务端应限流, 例如 <= 100)\n", g_open_streams.size());
    for (H2Stream* s : g_open_streams) delete s;   // 进程结束回收(缺陷本质是运行期无上限)
    return 0;
}
