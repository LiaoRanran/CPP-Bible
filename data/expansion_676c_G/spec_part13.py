# -*- coding: utf-8 -*-
# 676c-G spec part13: php/procps/openssh/glibc 组 (G066-G072)
PART = [
("G068", dict(
  defect_type="heap_overread", func="exif_process_IFD_TAG", severity="medium", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2019-11034", url="https://nvd.nist.gov/vuln/detail/CVE-2019-11034",
           project="php", commit="", simplification="剥离 PHP EXIF 扩展，IFD 数据硬编码 100 字节，保留『value_offset+byte_count 未按文件大小校验』核心缺陷"),
  trigger="IFD 条目 value_offset=90、byte_count=64，文件缓冲仅 100 字节 → 读越界 54 字节",
  notes="CVE-2019-11034: exif_process_IFD_TAG 读越界（CVE 描述: can be caused to read past allocated buffer in exif_process_IFD_TAG function. This may lead to information disclosure or crash）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-11034: exif_process_IFD_TAG 偏移+长度未按文件大小校验 → 堆越界读
static int exif_process_IFD_TAG(const unsigned char* data, size_t size,
                                unsigned value_offset, unsigned byte_count) {
    unsigned char value[64];
    size_t copy = byte_count < sizeof(value) ? byte_count : sizeof(value);
    /* DEFECT */ // 原始缺陷: 未检查 value_offset + byte_count <= size
    std::memcpy(value, data + value_offset, copy);
    return value[0];
}

int main() {
    // crafted EXIF: 文件缓冲 100 字节, IFD 条目指向 offset=90, 长度 64
    unsigned char* file = new unsigned char[100]();
    std::memset(file, 0x41, 100);
    std::printf("value[0]=%d\n", exif_process_IFD_TAG(file, 100, 90, 64));   // 读 90..154 → 越界
    delete[] file;
    return 0;
}
'''),

("G069", dict(
  defect_type="heap_overread", func="exif_read_signed_short", severity="medium", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2019-11036", url="https://nvd.nist.gov/vuln/detail/CVE-2019-11036",
           project="php", commit="", simplification="剥离 PHP EXIF 扩展，保留『components 计数参与偏移计算且未按文件大小校验』核心缺陷（与 11034 同函数不同触发路径）"),
  trigger="IFD 条目 components=100000 → 偏移 8+200000 远超 64 字节缓冲 → 野指针读",
  notes="CVE-2019-11036: exif_process_IFD_TAG 读越界（CVE 描述: can be caused to read past allocated buffer in exif_process_IFD_TAG function ... information disclosure or crash）。components 计数路径。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2019-11036: components 计数未校验 → 偏移远超缓冲 → 越界读
static int exif_read_signed_short(const unsigned char* data, size_t size, unsigned components) {
    /* DEFECT */ unsigned offset = 8 + components * 2;   // 未检查 offset + 2 <= size
    return (short)((data[offset] << 8) | data[offset + 1]);   // 野指针读 → SEGV
}

int main() {
    // crafted EXIF: 文件 64 字节, IFD 条目声明 components=100000 (LONG 格式)
    unsigned char* file = new unsigned char[64]();
    std::printf("value=%d\n", exif_read_signed_short(file, 64, 100000));   // offset=200008 → 越界
    delete[] file;
    return 0;
}
'''),

("G070", dict(
  defect_type="heap_overflow", func="file2strvec", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-1124", url="https://nvd.nist.gov/vuln/detail/CVE-2018-1124",
           project="procps-ng", commit="", simplification="基于 CVE 描述（file2strvec 多处整数溢出导致堆损坏, CWE-122/CWE-190）以『(int) 截断长度 → 小分配大拷贝』等价机制重构，非原始代码镜像，故标 planted=true"),
  trigger="procfs 条目长度 2^31 级别，(int)(i-start) 截断为负，按原始长度拷贝",
  notes="CVE-2018-1124: procps-ng file2strvec 多处整数溢出 → 堆损坏（CVE 描述: multiple integer overflows leading to a heap corruption in file2strvec function ... privilege escalation）。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2018-1124: file2strvec 整数溢出 → 堆损坏(用户态等价重构)
static char** file2strvec(const unsigned char* buf, size_t buf_len) {
    char** vec = new char*[4];
    size_t start = 0;
    /* DEFECT */ // 原始缺陷: 段长按 int 计算/分配, 巨大段长溢出为负
    int len = (int)(buf_len - start);          // 巨大长度 → (int) 截断为负
    char* dst = new char[len > 0 ? len + 1 : 1];   // 分配 1 字节
    std::memcpy(dst, buf, buf_len);            // 按真实长度拷贝 → 堆越界写
    vec[0] = dst;
    vec[1] = 0;
    return vec;
}

int main() {
    // crafted procfs 条目: 段长 2^31 + 8(运行时变量绕过常量折叠)
    volatile size_t seg = 0x80000008ULL;
    unsigned char* buf = new unsigned char[16];
    std::memset(buf, 'A', 16);
    char** v = file2strvec(buf, seg);
    std::printf("vec[0]=%s\n", v[0]);
    delete[] buf;
    return 0;
}
'''),

("G071", dict(
  defect_type="info_leak", func="resend_bytes", severity="high", planted=False,
  verdict="miss", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-0777", url="https://nvd.nist.gov/vuln/detail/CVE-2016-0777",
           project="openssh", commit="", simplification="剥离 roaming 协议层，保留『服务器请求重传时按整个缓冲区而非剩余未确认字节发送』核心缺陷"),
  trigger="服务器请求重传：应只发 offset 之后的 16 字节，实际把含私钥残留的整个 64 字节缓冲发出",
  notes="CVE-2016-0777: resend_bytes 重传整个缓冲区 → 进程内存泄露（CVE 描述: allows remote servers to obtain sensitive information from process memory by requesting transmission of an entire buffer）。纯信息泄露（读不越界），sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2016-0777: resend_bytes 重传整个缓冲区 → 泄露已确认部分(含私钥残留)
static const size_t SEND_BUF = 64;

static void resend_bytes(const unsigned char* buf, size_t confirmed_offset) {
    // 原始缺陷: 应从 buf+confirmed_offset 只发剩余字节
    /* DEFECT */ size_t resend_len = SEND_BUF;          // 发送了整个缓冲区
    std::printf("resend: 发送 %zu 字节 (confirmed_offset=%zu, 应仅发送 %zu 字节)\n",
                resend_len, confirmed_offset, SEND_BUF - confirmed_offset);
    // 缓冲内 [0, confirmed_offset) 为已确认历史数据 —— 含此前写入的私钥残留
}

int main() {
    unsigned char send_buf[SEND_BUF];
    std::memcpy(send_buf, "-----BEGIN OPENSSH PRIVATE KEY-----", 35);   // 模拟私钥残留(恰为字面量长度)
    resend_bytes(send_buf, 48);   // 恶意 roaming 服务器请求重传
    std::printf("(正确行为: 只重传 offset 之后的 16 字节)\n");
    return 0;
}
'''),

("G072", dict(
  defect_type="heap_overflow", func="nss_hostname_digits_dots", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-0235", url="https://nvd.nist.gov/vuln/detail/CVE-2015-0235",
           project="glibc", commit="", simplification="基于 CVE 描述（__nss_hostname_digits_dots 缓冲区尺寸计算错误，主机名接近边界时溢出）以等价的 off-by-one 尺寸计算重构，非原始代码镜像，故标 planted=true"),
  trigger="主机名恰 1024 字节 = 缓冲大小，尺寸计算缺少 NUL 的 +1 → 写入 buffer[1024]",
  notes="CVE-2015-0235 (GHOST): glibc gethostbyname 缓冲溢出（CVE 描述: buffer overflow in __nss_hostname_digits_dots ... hostname length close to buffer boundary）。用户态等价重构（planted=true）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2015-0235 (GHOST): 缓冲尺寸计算缺少 NUL 的 +1 → 边界处越界写 1 字节
static const size_t HOST_BUF_SIZE = 1024;

static bool digits_dots(const char* name, char* buffer, size_t buffer_size) {
    /* DEFECT */ size_t size_needed = std::strlen(name);   // 原始缺陷: 未 +1 给 '\0'
    if (size_needed > buffer_size) return false;
    std::memcpy(buffer, name, size_needed);
    buffer[size_needed] = '\0';   // size_needed == buffer_size 时写 buffer[buffer_size] → 越界
    return true;
}

int main() {
    char* hostbuf = new char[HOST_BUF_SIZE];
    // crafted 主机名: 恰好 1024 个 'a'
    char* name = new char[HOST_BUF_SIZE + 1];
    std::memset(name, 'a', HOST_BUF_SIZE);
    name[HOST_BUF_SIZE] = '\0';
    if (digits_dots(name, hostbuf, HOST_BUF_SIZE))
        std::printf("hostname accepted: %.8s...\n", hostbuf);
    delete[] name;
    delete[] hostbuf;
    return 0;
}
'''),

("G073", dict(
  defect_type="stack_overflow_write", func="send_dg", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2015-7547", url="https://nvd.nist.gov/vuln/detail/CVE-2015-7547",
           project="glibc", commit="", simplification="基于 CVE 描述（send_dg/send_vc 对 crafted DNS 响应的栈缓冲溢出）以『响应长度未按接收缓冲校验』等价机制重构，非原始代码镜像，故标 planted=true"),
  trigger="crafted DNS 响应 2048 字节 > 512 字节栈接收缓冲 → 整段拷贝",
  notes="CVE-2015-7547: glibc libresolv send_dg/send_vc 栈溢出（CVE 描述: Multiple stack-based buffer overflows in the (1) send_dg and (2) send_vc functions ... via a crafted DNS response）。用户态等价重构（planted=true）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2015-7547: send_dg 接收 crafted DNS 响应 → 栈缓冲溢出
static void send_dg(const unsigned char* response, size_t response_len) {
    unsigned char ans[512];       // 栈上接收缓冲
    /* DEFECT */ // 原始缺陷: 响应长度攻击者可控, 未按 anssiz 截断
    std::memcpy(ans, response, response_len);
    std::printf("dns answer: %02x %02x (len=%zu)\n", ans[0], ans[1], response_len);
}

int main() {
    // 恶意 DNS 服务器返回 2048 字节响应
    unsigned char* crafted = new unsigned char[2048];
    std::memset(crafted, 0x5A, 2048);
    send_dg(crafted, 2048);
    delete[] crafted;
    return 0;
}
'''),
]
