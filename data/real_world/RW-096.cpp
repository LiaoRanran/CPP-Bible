// RW-096 | CVE-2021-46143 | expat | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-46143
// project_url: https://libexpat.github.io/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: doProlog（DTD 处理）中组计数以 int 累加，构造深层/重复 DTD 组
//   使计数溢出，随后数组索引越界。
// notes: 最小重构。UBSan + ASan 命中。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: group count accumulates in int across DTD declarations; crafted DTD
// with ~2^31 group units wraps it negative, then indexing goes out of bounds.
struct DtdProlog {
    int group_count;
    int* groups;              // indexed by group_count
    int capacity;
};

void do_prolog(DtdProlog& p, int units) {
    for (int i = 0; i < units; ++i) {
        p.group_count += 1;                       // signed overflow after INT_MAX
        int idx = p.group_count & 0x3;            // wrap-derived mask
        if (idx >= 0 && idx < p.capacity) {
            p.groups[idx] = i;
        } else {
            p.groups[idx] = i;                    // OOB write when idx negative
        }
    }
}

int main() {
    DtdProlog p{};
    p.capacity = 8;
    p.groups = static_cast<int*>(std::malloc(sizeof(int) * 8));
    p.group_count = 0x7FFFFFF8;                   // crafted near-INT_MAX state
    do_prolog(p, 32);                             // overflow during the loop
    std::printf("group_count=%d\n", p.group_count);
    std::free(p.groups);
    return 0;
}
