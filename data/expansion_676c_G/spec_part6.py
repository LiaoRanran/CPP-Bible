# -*- coding: utf-8 -*-
# 676c-G spec part6: curl asan 组 I (G026-G030)
PART = [
("G026", dict(
  defect_type="stack_overread", func="tftp_send_first", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-1000100", url="https://nvd.nist.gov/vuln/detail/CVE-2017-1000100",
           project="curl", commit="", simplification="剥离 TFTP 传输层，文件名硬编码为 600 字节，保留『文件名被截断但缓冲区尺寸仍按未截断长度使用』核心缺陷"),
  trigger="TFTP URL 文件名 600 字节 > 515 缓冲，发送尺寸仍按 600 计算 → 栈越界读 89 字节",
  notes="CVE-2017-1000100: 超长文件名被截断入 515 缓冲，但缓冲尺寸仍按未截断长度更新，sendto 按错误尺寸发送（CVE 描述: the file name is truncated to fit within the buffer boundaries, but the buffer size is still wrongly updated）。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2017-1000100: TFTP 文件名截断后缓冲尺寸仍按原始长度 → 越界读
static const size_t TFTP_BUFFER_SIZE = 515;

static void tftp_send_first(const std::string& filename) {
    char buffer[TFTP_BUFFER_SIZE];                 // TFTP 包缓冲(栈)
    size_t name_len = filename.size();             // 600
    if (name_len > TFTP_BUFFER_SIZE - 4) {         // 截断入缓冲
        std::memcpy(buffer + 2, filename.c_str(), TFTP_BUFFER_SIZE - 4);
        name_len = TFTP_BUFFER_SIZE - 4;
    } else {
        std::memcpy(buffer + 2, filename.c_str(), name_len);
    }
    buffer[0] = 0; buffer[1] = 1;                  // RRQ
    /* DEFECT */ size_t send_size = 2 + filename.size() + 1;   // 原始缺陷: 用未截断的原始长度(603)
    char* sendbuf = new char[send_size];
    std::memcpy(sendbuf, buffer, send_size);       // 从 515 栈缓冲读 603 字节 → 越界读 88 字节
    std::printf("tftp rrq sent %zu bytes, head=%c%c\n", send_size, sendbuf[0], sendbuf[1]);
    delete[] sendbuf;
}

int main() {
    tftp_send_first(std::string(600, 'a'));   // 超长文件名
    return 0;
}
'''),

("G032", dict(
  defect_type="heap_overread", func="smtp_endofresp", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2019-3823", url="https://nvd.nist.gov/vuln/detail/CVE-2019-3823",
           project="curl", commit="", simplification="剥离 SMTP 传输层，响应缓冲硬编码为 3 字节堆分配，保留『按固定 5 字节模式读且忽略 len』核心缺陷"),
  trigger="SMTP 响应缓冲 3 字节且无 NUL，endofresp 仍按固定 5 字节扫描",
  notes="CVE-2019-3823: smtp_endofresp 对未 NUL 结尾且 len=5 的缓冲堆越界读（CVE 描述: heap out-of-bounds read in the code handling the end-of-response for SMTP ... if the buffer ... isn't NUL terminated and contains no character ending the parsed number）。",
), r'''
#include <cstdio>
// CVE-2019-3823: smtp_endofresp 固定 5 字节扫描, 缓冲未 NUL 结尾 → 堆越界读
static int smtp_endofresp(const char* buf, size_t len) {
    (void)len;   // 原始缺陷: len 未参与边界控制
    int code = 0;
    /* DEFECT */ for (size_t i = 0; i < 5; ++i) {   // 固定读 5 字节
        if (buf[i] >= '0' && buf[i] <= '9')
            code = code * 10 + (buf[i] - '0');
        else if (buf[i] == ' ')
            return code;
    }
    return -1;
}

int main() {
    // crafted SMTP 响应: 3 字节堆分配, 无 NUL, 无空格/数字结尾
    char* resp = new char[3]{ '2', '5', '0' };
    std::printf("resp code=%d\n", smtp_endofresp(resp, 3));   // 读 buf[3..4] → 越界
    delete[] resp;
    return 0;
}
'''),

("G028", dict(
  defect_type="integer_overflow", func="ntlm_encode_size", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2017-8816", url="https://nvd.nist.gov/vuln/detail/CVE-2017-8816",
           project="curl", commit="", simplification="剥离 NTLM 编码主体，保留『32 位平台上用户名/域/密码长度按 int 累加』核心缺陷，长度由运行时变量给出"),
  trigger="用户名/域/密码各 2^29 字节，长度和乘 2 溢出 int",
  notes="CVE-2017-8816: NTLM 认证在 32 位平台整数溢出（CVE 描述: denial of service (integer overflow and resultant buffer overflow) via vectors involving long user and password fields）。本样本镜像长度计算溢出点。",
), r'''
#include <cstdio>
// CVE-2017-8816: NTLM 长度按 int 累加(32 位平台) → 溢出
static int ntlm_encode_size(int userlen, int domlen, int passwdlen) {
    /* DEFECT */ int total = 2 * (userlen + domlen + passwdlen) + 64;   // int 溢出
    return total;
}

int main() {
    // crafted: 超长用户名/域/密码(各 2^29), 运行时变量绕过常量折叠
    volatile int ul = 0x20000000, dl = 0x20000000, pl = 0x20000000;
    int total = ntlm_encode_size(ul, dl, pl);
    std::printf("ntlm total=%d (应为 %lld)\n", total, 2LL * (ul + dl + pl) + 64);
    return 0;
}
'''),

("G029", dict(
  defect_type="heap_overread", func="ntlm_decode_type2_target", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-16890", url="https://nvd.nist.gov/vuln/detail/CVE-2018-16890",
           project="curl", commit="", simplification="剥离 NTLM 握手流程，type-2 消息硬编码为 32 字节堆缓冲，保留『target 长度/偏移字段未校验即 memcpy』核心缺陷"),
  trigger="type-2 消息 target_info_len=1000，消息实际仅 32 字节 → 读越界",
  notes="CVE-2018-16890: ntlm_decode_type2_target 未正确校验传入数据（CVE 描述: does not validate incoming data correctly and is subject to an integer overflow / out-of-bounds read），堆越界读。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2018-16890: ntlm_decode_type2_target 未校验 target 长度/偏移 → 堆越界读
static int ntlm_decode_type2_target(const unsigned char* buffer, size_t size) {
    unsigned short target_info_len = (unsigned short)(buffer[12] | (buffer[13] << 8));
    unsigned int   target_info_off = (unsigned int)(buffer[16] | (buffer[17] << 8));
    unsigned char  target[1024];
    /* DEFECT */ // 原始缺陷: 未检查 target_info_off + target_info_len <= size
    std::memcpy(target, buffer + target_info_off, target_info_len);
    return target[0];
}

int main() {
    // crafted NTLM type-2 消息: 32 字节, 声明 target_info_len=1000, offset=20
    unsigned char* msg = new unsigned char[32]();
    msg[12] = 0xE8; msg[13] = 0x03;    // len = 1000
    msg[16] = 20;                      // offset = 20
    std::printf("target[0]=%d\n", ntlm_decode_type2_target(msg, 32));   // 读 20..1020 → 越界
    delete[] msg;
    return 0;
}
'''),

("G030", dict(
  defect_type="heap_overflow", func="tftp_receive_packet", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2019-5436", url="https://nvd.nist.gov/vuln/detail/CVE-2019-5436",
           project="curl", commit="", simplification="剥离 TFTP 传输层，服务器选项响应硬编码，保留『blksize 大于接收缓冲时直接 memcpy』核心缺陷（修复版将 blksize 上限设为 512）"),
  trigger="服务器响应 blksize=1024，接收缓冲固定 512 → 堆越界写 512 字节",
  notes="CVE-2019-5436: TFTP 接收代码堆溢出（CVE 描述: A heap buffer overflow in the TFTP receiving code allows for DoS or arbitrary code execution）。修复版 blksize 上限 512，本样本保留未限制版本。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-5436: TFTP 接收 blksize 大于接收缓冲 → 堆越界写
static const size_t TFTP_RECV_BUF = 512;

static void tftp_receive_packet(const unsigned char* pkt, size_t pktlen) {
    // pkt: [opcode(2)][blksize 选项值(2)][数据...]
    unsigned short blksize = (unsigned short)((pkt[2] << 8) | pkt[3]);   // 服务器可任意声明
    unsigned char* rbuf = new unsigned char[TFTP_RECV_BUF];
    /* DEFECT */ std::memcpy(rbuf, pkt + 4, blksize);   // blksize=1024 > 512 → 越界写
    std::printf("tftp received blksize=%u\n", blksize);
    delete[] rbuf;
}

int main() {
    // crafted 服务器响应: blksize 选项 = 1024, 数据足够长
    unsigned char* pkt = new unsigned char[1032]();
    pkt[2] = 0x04; pkt[3] = 0x00;      // blksize = 1024
    std::memset(pkt + 4, 'D', 1028);
    tftp_receive_packet(pkt, 1032);
    delete[] pkt;
    return 0;
}
'''),
]
