// sample_G034
// defect_type: use_after_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-22945 (https://nvd.nist.gov/vuln/detail/CVE-2021-22945) [curl]
// (authoritative annotation in sample_G034.json)
#include <cstdio>
#include <cstring>
// CVE-2021-22945: MQTT 断连后仍使用/再次释放已释放的发送缓冲
struct MqttConn {
    bool  disconnected;
    char* pending;      // 待发送数据(断连后本应作废)
};

static void mqtt_disconnect(MqttConn* c) {
    /* DEFECT */ delete[] c->pending;   // 原始缺陷: 释放后未置空 c->pending
    std::printf("mqtt: disconnected\n");
}

static void mqtt_send_pending(MqttConn* c) {
    for (size_t i = 0; c->pending[i]; ++i)   // UAF 读
        std::putchar(c->pending[i]);
    std::putchar('\n');
    /* DEFECT */ delete[] c->pending;        // 再次释放 → double free
}

int main() {
    MqttConn c{ false, new char[8] };
    std::memcpy(c.pending, "PUBLISH", 8);
    c.disconnected = true;
    mqtt_disconnect(&c);      // 服务器断连 → 释放
    mqtt_send_pending(&c);    // 后续发送仍使用该指针 → UAF + double free
    return 0;
}
