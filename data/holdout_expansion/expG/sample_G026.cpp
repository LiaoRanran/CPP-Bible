// sample_G026
// defect_type: stack_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-1000100 (https://nvd.nist.gov/vuln/detail/CVE-2017-1000100) [curl]
// (authoritative annotation in sample_G026.json)
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
