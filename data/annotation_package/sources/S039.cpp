// sample_G027
// [redacted]
// severity: high
// [redacted]
// expected_verdict: catch
// [redacted]
// [redacted]
// (authoritative annotation in sample_G027.json)
#include <cstdio>
// [redacted]
static int smtp_endofresp(const char* buf, size_t len) {
    (void)len;   // [redacted]
    int code = 0;
    /* [redacted]*/ for (size_t i = 0; i < 5; ++i) {   // 固定读 5 字节
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
    std::printf("resp code=%d\n", smtp_endofresp(resp, 3));   // [redacted]
    delete[] resp;
    return 0;
}
