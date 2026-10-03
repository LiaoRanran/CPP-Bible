# -*- coding: utf-8 -*-
# 676c-G spec part7: curl asan 组 II (socks5/rtsp/imap/mqtt/2026)
PART = [
("G031", dict(
  defect_type="heap_overflow", func="socks5_send_hostname", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2023-38545", url="https://nvd.nist.gov/vuln/detail/CVE-2023-38545",
           project="curl", commit="", simplification="剥离 SOCKS5 握手状态机，主机名硬编码 20000 字节，保留『主机名超限未校验即整段拷贝进固定堆缓冲』核心缺陷"),
  trigger="代理远程解析路径下主机名 20000 字节 > 16KB 请求缓冲 → 堆越界写约 4KB",
  notes="CVE-2023-38545: SOCKS5 代理握手堆缓冲溢出（CVE 描述: This flaw makes curl overflow a heap based buffer in the SOCKS5 proxy handshake），主机名超长且走慢速握手路径时整段拷贝。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2023-38545: SOCKS5 握手把超长主机名整段拷贝进固定缓冲 → 堆越界写
static const size_t SOCKS5_REQ_MAX = 16 * 1024;   // 请求缓冲上限

static void socks5_send_hostname(const std::string& host) {
    unsigned char* req = new unsigned char[SOCKS5_REQ_MAX + 8]();
    req[0] = 5; req[1] = 1; req[2] = 0; req[3] = 3;   // VER/CMD/RSV/ATYP=domain
    size_t hlen = host.size();                        // 20000
    /* DEFECT */ // 原始缺陷: 慢速路径未检查 hlen 是否超过缓冲容量即整段拷贝
    std::memcpy(req + 5, host.c_str(), hlen);
    std::printf("socks5 req sent, host_len=%zu\n", hlen);
    delete[] req;
}

int main() {
    socks5_send_hostname(std::string(20000, 'h'));   // 超长主机名
    return 0;
}
'''),

("G033", dict(
  defect_type="heap_overread", func="rtp_parse", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-1000122", url="https://nvd.nist.gov/vuln/detail/CVE-2018-1000122",
           project="curl", commit="", simplification="剥离 RTSP 传输层，RTP interleaved 帧硬编码 2 字节，保留『检测到 '$' 后按固定偏移读 4 字节头而不检查剩余长度』核心缺陷"),
  trigger="帧缓冲仅 2 字节('$' + 1 字节)，RTP 头按固定偏移读第 3/4 字节 → 堆越界读",
  notes="CVE-2018-1000122: RTSP+RTP 处理代码缓冲越界读（CVE 描述: A buffer over-read exists ... in the RTSP+RTP handling code that allows an attacker to cause a denial of service or information leakage）。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2018-1000122: RTSP interleaved RTP 帧头固定偏移读取 → 越界读
static int rtp_parse(const char* frame, size_t len) {
    const char* p = frame;
    const char* end = frame + len;
    while (p + 1 < end) {
        if (*p == '$') {   // interleaved 帧头: '$' channel seq_len(2)
            /* DEFECT */ // 原始缺陷: 未检查 p+3 < end
            unsigned short plen = (unsigned short)(((unsigned char)p[2] << 8) | (unsigned char)p[3]);
            return plen;
        }
        ++p;
    }
    return -1;
}

int main() {
    // crafted RTSP 帧: 仅 "$C" → 读 p[2]/p[3] 越过 2 字节堆分配
    char* frame = new char[2]{ '$', 'C' };
    std::printf("rtp len=%d\n", rtp_parse(frame, 2));
    delete[] frame;
    return 0;
}
'''),

("G034", dict(
  defect_type="heap_overflow", func="deliver_data", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-1000257", url="https://nvd.nist.gov/vuln/detail/CVE-2017-1000257",
           project="curl", commit="", simplification="剥离 IMAP FETCH 响应解析，行缓冲硬编码 4 字节，保留『size=0 时仍向数据指针写入终结符』核心缺陷"),
  trigger="IMAP FETCH 响应声明 0 字节数据，deliver_data 仍写 datap[0]='\\0'，而 datap 已指向缓冲区末尾",
  notes="CVE-2017-1000257: IMAP FETCH 零字节数据时 deliver-data 收到越界指针（CVE 描述: libcurl would pass on that (non-existing) data with a pointer and the size (zero) ... 可写越界 1 字节）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2017-1000257: IMAP FETCH size=0 → 向缓冲区末尾写终结符 → 越界写 1 字节
static void deliver_data(char* datap, size_t size) {
    /* DEFECT */ datap[size] = '\0';   // 原始缺陷: size=0 且 datap 指向缓冲区末尾 → 写 datap[0] 越界
    std::printf("delivered %zu bytes\n", size);
}

int main() {
    // crafted IMAP 响应行: 4 字节堆分配, 数据指针推进到末尾, size=0
    char* line = new char[4]{ '1', '2', ' ', 'x' };
    deliver_data(line + 4, 0);         // 写 line[4] → 堆越界写 1 字节
    delete[] line;
    return 0;
}
'''),

("G035", dict(
  defect_type="use_after_free", func="mqtt_send_pending", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-22945", url="https://nvd.nist.gov/vuln/detail/CVE-2021-22945",
           project="curl", commit="", simplification="剥离 MQTT 传输层与断连状态机，保留『断连释放缓冲后指针未置空，后续发送再次使用并再次释放』核心缺陷"),
  trigger="向 MQTT 服务器发送数据时服务器断连，断连释放 pending 缓冲后仍被使用",
  notes="CVE-2021-22945: MQTT 发送时错误地保留已释放内存指针（CVE 描述: erroneously keep a pointer to an already freed memory area and both use that again ... and also free it again）→ UAF + double free。",
), r'''
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
'''),

("G036", dict(
  defect_type="use_after_free", func="smb_request2", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2026-3805", url="https://nvd.nist.gov/vuln/detail/CVE-2026-3805",
           project="curl", commit="", simplification="剥离 SMB 传输层，保留官方公告描述的『第二次请求使用指向已释放内存的数据指针』核心缺陷，share 树指针挂在会话上"),
  trigger="第一个 SMB 请求把指向请求内部数据的指针存入会话，请求销毁后第二个请求仍使用该指针",
  notes="CVE-2026-3805: SMB 第二次请求使用已释放内存的数据指针（官方公告: making a second SMB request curl uses data pointers to freed memory, Medium, CWE-416）。2026-03-11 披露。",
), r'''
#include <cstdio>
#include <string>
// CVE-2026-3805: SMB 第二次请求使用已释放请求数据的指针 → UAF
struct SmbRequest {
    std::string path;    // 14 字节, SSO: 存储在对象内部
};

struct SmbSession {
    const char* tree;    // 指向 request 内部数据的指针(悬垂来源)
};

static void smb_first_request(SmbSession* s) {
    SmbRequest* r = new SmbRequest;
    r->path = "//server/share";              // SSO: c_str() 指向对象内部
    s->tree = r->path.c_str();
    /* DEFECT */ delete r;                    // 原始缺陷: 请求销毁未清空 s->tree
}

static void smb_second_request(SmbSession* s) {
    std::printf("tree=%s\n", s->tree);        // 第二次请求读已释放内存 → UAF
}

int main() {
    SmbSession s{ 0 };
    smb_first_request(&s);
    smb_second_request(&s);
    return 0;
}
'''),

("G037", dict(
  defect_type="double_free", func="sasl_gsasl_cleanup", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2026-8925", url="https://nvd.nist.gov/vuln/detail/CVE-2026-8925",
           project="curl", commit="", simplification="剥离 GSASL 认证流程，保留官方公告描述的『GSASL 上下文被清理两次且中间未清空指针』核心缺陷"),
  trigger="SASL 认证错误重试路径对同一上下文调用两次 cleanup，中间未置 NULL",
  notes="CVE-2026-8925: GSASL 上下文 double free（官方公告: GSASL context is cleaned up twice without clearing the pointer in between, Medium, CWE-415）。2026-09-02 披露。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2026-8925: GSASL 上下文清理两次 → double free
struct GsaslCtx {
    char* out;    // 认证输出缓冲
};

static void gsasl_cleanup(GsaslCtx** ctx) {
    if (!ctx || !*ctx) return;
    delete[] (*ctx)->out;
    delete *ctx;
    /* DEFECT */ // 原始缺陷: 清理后未置 *ctx = NULL
}

static int sasl_authenticate(bool retry_needed) {
    GsaslCtx* c = new GsaslCtx{ new char[64] };
    std::memcpy(c->out, "AUTH-RESPONSE", 14);
    gsasl_cleanup(&c);
    if (retry_needed)
        gsasl_cleanup(&c);   /* DEFECT */ // 第二次清理(错误重试路径) → double free
    return 0;
}

int main() {
    sasl_authenticate(true);
    return 0;
}
'''),
]
