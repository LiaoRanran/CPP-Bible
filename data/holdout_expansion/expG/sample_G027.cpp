// sample_G027
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2019-3823 (https://nvd.nist.gov/vuln/detail/CVE-2019-3823) [curl]
// (authoritative annotation in sample_G027.json)
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
