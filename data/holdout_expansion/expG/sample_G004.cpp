// sample_G004
// defect_type: memory_leak
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-0206 (https://nvd.nist.gov/vuln/detail/CVE-2015-0206) [openssl]
// (authoritative annotation in sample_G004.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2015-0206: dtls1_buffer_record 在 next-epoch 错误路径泄漏已分配的记录对象
struct DtlsRecord {
    unsigned char* data;
    int            len;
};

static int dtls1_buffer_record(int current_epoch, int rec_epoch) {
    // 原始代码: 在 epoch 检查**之前**就已分配 rdata
    DtlsRecord* r = new DtlsRecord{ new unsigned char[512], 512 };
    std::memset(r->data, 0xAB, 512);

    if (rec_epoch != current_epoch) {
        // wrong epoch → 记录不能缓冲在本 epoch 队列
        /* DEFECT */ return -1;   // 原始缺陷: 错误返回未释放 r（数据+对象）→ 泄漏
    }
    std::printf("record buffered (epoch=%d, len=%d)\n", rec_epoch, r->len);
    delete[] r->data;
    delete r;
    return 0;
}

int main() {
    // 攻击者重复发送下一 epoch 的重复记录（简化为 8 次, 原始为持续发送）
    for (int i = 0; i < 8; ++i) {
        if (dtls1_buffer_record(1, 2) != 0)
            std::printf("record dropped (leaked)\n");
    }
    return 0;
}
