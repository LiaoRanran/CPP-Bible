# -*- coding: utf-8 -*-
# 676c-G spec part1: OpenSSL asan 组 I (G001-G005)
PART = [
("G001", dict(
  defect_type="heap_overread", func="tls1_process_heartbeat", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2014-0160", url="https://nvd.nist.gov/vuln/detail/CVE-2014-0160",
           project="openssl", commit="", simplification="剥离 TLS/DTLS 网络层，心跳请求包硬编码在 main 中构造，保留『信任 payload_length、按声明长度 memcpy』的核心缺陷"),
  trigger="心跳载荷长度字段声明 65535，实际载荷仅 1 字节",
  notes="Heartbleed：tls1_process_heartbeat 不校验 payload_length 与请求缓冲区实际大小，按声明长度把堆上请求缓冲之外的内存作为心跳响应回显（最多 64KB 进程内存泄露）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2014-0160 (Heartbleed): 未校验 payload_length 与实际请求缓冲区大小 → 堆越界读
struct HeartbeatRequest {
    uint8_t  type;         // 1 = heartbeat_request
    uint16_t payload_len;  // 声明的载荷长度
    // 载荷紧随其后（本样本实际仅 1 字节）
};

static void tls1_process_heartbeat(const uint8_t* p, size_t n) {
    if (n < 4) { std::printf("packet too small\n"); return; }
    uint16_t payload_len = (uint16_t)((p[1] << 8) | p[2]);

    uint8_t* response = new uint8_t[3 + payload_len];
    response[0] = 2;                      // heartbeat_response
    response[1] = p[1];
    response[2] = p[2];
    /* DEFECT */ std::memcpy(response + 3, p + 3, payload_len);  // 声明 65535, 实际仅 1 字节 → 堆越界读
    std::printf("hb: echo %u bytes, first=%02x\n", (unsigned)payload_len, response[3]);
    delete[] response;
}

int main() {
    // 硬编码恶意心跳请求: type=1, length=0xFFFF, 载荷实际只有 'A'
    uint8_t* req = new uint8_t[4]{ 1, 0xFF, 0xFF, 'A' };
    tls1_process_heartbeat(req, 4);
    delete[] req;
    return 0;
}
'''),

("G002", dict(
  defect_type="heap_overread", func="OBJ_obj2txt", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2014-3508", url="https://nvd.nist.gov/vuln/detail/CVE-2014-3508",
           project="openssl", commit="", simplification="剥离 OID 解码逻辑，保留『分配的文本缓冲不保证 NUL 结尾』核心缺陷，调用方按 C 字符串使用"),
  trigger="OID pretty-print 返回不含 NUL 的精确长度缓冲，调用方 printf 按字符串读越界",
  notes="OBJ_obj2txt 在 pretty print 时分配精确大小的缓冲但不保证写入 '\\0'（CVE 描述: does not ensure the presence of '\\0' characters），调用方以 C 字符串处理 → 读越界，泄露进程内存。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2014-3508: OBJ_obj2txt(pretty print) 不保证 '\0' → 调用方按 C 字符串读 → 越界读
static char* OBJ_obj2txt_pretty(const unsigned char* oid, size_t oid_len) {
    // 原始缺陷: 缓冲按解码后文本精确大小分配, 不含 '\0'
    char* buf = new char[oid_len];
    for (size_t i = 0; i < oid_len; ++i)
        buf[i] = (char)('0' + (oid[i] % 10));
    return buf;
}

int main() {
    unsigned char* oid = new unsigned char[16]
        { 42, 1, 2, 84, 113, 1, 1, 11, 5, 0, 3, 13, 1, 4, 7, 9 };
    char* text = OBJ_obj2txt_pretty(oid, 16);
    /* DEFECT */ std::printf("oid=%s\n", text);   // printf/%s 需要 strlen → 越过 16 字节缓冲
    delete[] text;
    delete[] oid;
    return 0;
}
'''),

("G003", dict(
  defect_type="null_deref", func="dtls1_read_timeout", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2014-3571", url="https://nvd.nist.gov/vuln/detail/CVE-2014-3571",
           project="openssl", commit="", simplification="剥离 DTLS 网络层与重传队列，保留『一条读路径释放/置空消息对象后另一读路径仍解引用』的核心缺陷"),
  trigger="DTLS 握手消息在缓冲读路径被释放后，超时读路径仍解引用该指针",
  notes="CVE-2014-3571: crafted DTLS 消息在『header 读』与『消息体读』两条路径处理不一致，导致 NULL 指针解引用（CVE 描述: NULL pointer dereference and application crash）。本样本镜像该模式。",
), r'''
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
'''),

("G004", dict(
  defect_type="memory_leak", func="dtls1_buffer_record", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-0206", url="https://nvd.nist.gov/vuln/detail/CVE-2015-0206",
           project="openssl", commit="", simplification="剥离 DTLS 网络层，epoch 判定用参数硬编码，保留『为下一 epoch 缓冲记录时错误路径不释放 rdata』核心缺陷"),
  trigger="重复收到下一 epoch 的重复记录（8 次），每次缓冲路径都走错误返回",
  notes="CVE-2015-0206: dtls1_buffer_record 为 next epoch 缓冲重复记录时 memory leak（CVE 描述: Memory leak in dtls1_buffer_record ... by sending many duplicate records for the next epoch）→ 攻击者可耗尽内存。LeakSanitizer 捕获。",
), r'''
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
'''),

("G005", dict(
  defect_type="double_free", func="dtls1_process_fragment", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2014-3505", url="https://nvd.nist.gov/vuln/detail/CVE-2014-3505",
           project="openssl", commit="", simplification="剥离 DTLS 网络层，保留『错误路径释放 fragment 后公共清理路径再次释放』核心缺陷"),
  trigger="crafted DTLS 握手分片触发错误路径，随后公共清理再次 free",
  notes="CVE-2014-3505: d1_both.c 中 DTLS 错误路径的 double free（CVE 描述: Double free vulnerability in d1_both.c ... crafted DTLS packets that trigger an error path）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2014-3505: DTLS 握手分片错误路径 double free
struct HmFragment {
    unsigned char* frag;
    int            frag_len;
};

static void dtls1_hm_fragment_free(HmFragment* f) {
    if (!f) return;
    delete[] f->frag;
    delete f;
}

static int dtls1_process_fragment(bool crafted_error) {
    HmFragment* f = new HmFragment{ new unsigned char[256], 256 };
    std::memset(f->frag, 0, 256);

    if (crafted_error) {
        dtls1_hm_fragment_free(f);     // 错误路径第一次释放
        std::printf("fragment error path: freed once\n");
        /* DEFECT */
    }
    // 公共清理路径不区分错误与否, 再次释放 → double free
    dtls1_hm_fragment_free(f);
    return 0;
}

int main() {
    dtls1_process_fragment(true);   // crafted DTLS 分片 → 错误路径 + 公共清理 = 双重释放
    return 0;
}
'''),
]
