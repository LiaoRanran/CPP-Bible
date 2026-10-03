// sample_G055
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-10989 (https://nvd.nist.gov/vuln/detail/CVE-2017-10989) [sqlite]
// (authoritative annotation in sample_G055.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2017-10989: getNodeSize 对 undersized blob 越界读
struct RtreeBlob {
    unsigned char* data;
    int            data_len;   // blob 实际大小(攻击者 crafted 过小)
    int            n_dim;      // 头部声明的维度数
};

static int getNodeSize(const RtreeBlob* b) {
    int cell_size = 8 * b->n_dim + 4;
    /* DEFECT */ // 原始缺陷: 未校验 blob 大小是否容纳声明的单元
    double first_coord;
    std::memcpy(&first_coord, b->data + 4, sizeof(first_coord));   // 读 4..12, blob 仅 8 字节
    return cell_size;
}

int main() {
    // crafted 数据库页中的 undersized rtree blob
    RtreeBlob b;
    b.data_len = 8;
    b.n_dim = 7;                       // 声明 7 维 → 单元 60 字节, 但 blob 只有 8 字节
    b.data = new unsigned char[8]{ 0, 0, 0, 7, 0x3F, 0xF0, 0, 0 };
    std::printf("node size=%d\n", getNodeSize(&b));   // memcpy 读 data[4..12] → 越界 4 字节
    delete[] b.data;
    return 0;
}
