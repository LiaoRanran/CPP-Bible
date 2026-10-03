// sample_G003
// defect_type: null_deref
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2014-3571 (https://nvd.nist.gov/vuln/detail/CVE-2014-3571) [openssl]
// (authoritative annotation in sample_G003.json)
#include <cstdio>
// CVE-2014-3571: DTLS 两条读路径对消息对象的处理不一致 → 空指针解引用
struct DtlsMessage {
    int   frag_off;
    int   frag_len;
    unsigned char* body;
};

static DtlsMessage* g_buffered_msg = new DtlsMessage{ 0, 128, new unsigned char[128] };

// 读路径 A（消息体读）: 错误处理时释放缓冲消息
static int dtls1_read_message_body() {
    delete[] g_buffered_msg->body;
    delete g_buffered_msg;
    g_buffered_msg = 0;      // 已置空 —— 但另一条读路径并不知道
    return -1;
}

// 读路径 B（header 读 / 超时重读）: 仍假定消息对象存在
static int dtls1_read_timeout() {
    /* DEFECT */ return g_buffered_msg->frag_len;   // 解引用已释放/空指针 → SEGV
}

int main() {
    std::printf("dtls: buffered msg len=%d\n", g_buffered_msg->frag_len);
    dtls1_read_message_body();   // crafted DTLS 消息触发错误路径
    dtls1_read_timeout();        // 另一条读路径使用已释放的消息 → 崩溃
    return 0;
}
