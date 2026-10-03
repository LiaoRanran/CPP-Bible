// sample_G033
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-1000257 (https://nvd.nist.gov/vuln/detail/CVE-2017-1000257) [curl]
// (authoritative annotation in sample_G033.json)
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
