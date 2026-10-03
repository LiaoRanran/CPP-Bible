// sample_G091
// defect_type: heap_overread
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: nlohmann/json#3492 (https://github.com/nlohmann/json/issues/3492) [nlohmann/json]
// (authoritative annotation in sample_G091.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// nlohmann/json#3492 (等价重构): BJData 解析按声明长度读 → 堆越界读
// BJData string 编码: 'S' 'i' <int8 len> <bytes...>
static int bjdata_parse(const unsigned char* in, size_t in_size) {
    size_t pos = 0;
    if (pos >= in_size || in[pos] != 'S') return -1;
    ++pos;
    if (pos >= in_size || in[pos] != 'i') return -1;
    ++pos;
    if (pos >= in_size) return -1;
    unsigned char declared = in[pos++];       // 头部声明的字符串长度
    char out[64];
    /* DEFECT */ for (unsigned char i = 0; i < declared; ++i) {   // 未校验 declared <= in_size - pos
        out[i] = (char)in[pos + i];           // declared=32, 剩余 5 字节 → 越界读
    }
    out[declared < 64 ? declared : 63] = '\0';
    std::printf("bjdata string=%s\n", out);
    return 0;
}

int main() {
    // crafted BJData(对应 OSS-Fuzz 最小化用例的结构): 'S','i',32,5 字节数据
    unsigned char in[8] = { 'S', 'i', 32, 'a', 'b', 'c', 'd', 'e' };
    bjdata_parse(in, 8);
    return 0;
}
