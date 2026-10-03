// sample_G089
// defect_type: resource_exhaustion
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2019-9512 (https://nvd.nist.gov/vuln/detail/CVE-2019-9512) [http2]
// (authoritative annotation in sample_G089.json)
#include <cstdio>
#include <vector>
// CVE-2019-9512 (有界模拟): HTTP/2 SETTINGS 帧洪泛 → 处理队列无上限增长
struct H2SettingsFrame {
    int  n_settings;
    bool ack_required;
};

static std::vector<H2SettingsFrame*> g_pending_settings;

static void h2_on_settings_frame(int n_settings) {
    /* DEFECT */ // 原始缺陷: 每帧都分配处理对象入队, 无速率限制/队列上限
    g_pending_settings.push_back(new H2SettingsFrame{ n_settings, true });
}

int main() {
    // 攻击者: 持续发送 SETTINGS(有界模拟 20000 帧)
    for (int i = 0; i < 20000; ++i)
        h2_on_settings_frame(6);
    std::printf("pending settings frames=%zu (正确行为: 队列应有上限或丢弃策略)\n",
                g_pending_settings.size());
    for (H2SettingsFrame* f : g_pending_settings) delete f;
    return 0;
}
