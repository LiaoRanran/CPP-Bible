// sample_G051
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2019-8457 (https://nvd.nist.gov/vuln/detail/CVE-2019-8457) [sqlite]
// (authoritative annotation in sample_G051.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-8457: rtreenode 处理 invalid rtree 表 → 堆越界读
struct RtreeNode {
    unsigned char* data;
    int            data_len;   // 实际缓冲大小
    int            n_cell;     // 头部声明的单元数(攻击者可控)
};

static double rtreenode_read_coord(const RtreeNode* n, int cell, int dim) {
    // 每单元 8 字节坐标 × 4 维
    size_t off = sizeof(int) + (size_t)cell * 32 + (size_t)dim * 8;
    double v;
    /* DEFECT */ // 原始缺陷: 未校验 cell 数与 data_len 的一致性
    std::memcpy(&v, n->data + off, sizeof(v));
    return v;
}

int main() {
    // crafted rtree 节点: 缓冲只有 2 个单元(8+64 字节), 头部声明 n_cell=9
    RtreeNode n;
    n.data_len = 8 + 2 * 32;
    n.n_cell = 9;
    n.data = new unsigned char[n.data_len];
    std::memset(n.data, 0x3F, n.data_len);
    std::memcpy(n.data, &n.n_cell, sizeof(int));
    for (int c = 0; c < n.n_cell; ++c)
        std::printf("cell %d coord0=%f\n", c, rtreenode_read_coord(&n, c, 0));   // c>=2 越界
    delete[] n.data;
    return 0;
}
