// RW-061 | CVE-2020-15358 | SQLite | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-15358
// project_url: https://sqlite.org/
// year: 2020 | severity: MEDIUM | source_type: cve
// mechanism: multiSelectOrderBy（多列 ORDER BY）对表达式列表的处理越界，
//   特制 SQL 触发堆缓冲区溢出。
// notes: 最小重构（order-by 项数组从不含长度校验的解析器进入）。
#include <cstdio>
#include <vector>

struct OrderByTerm {
    int col;
    int flags;
};

// BUG: the number of ORDER BY terms from a compound SELECT is copied into a
// fixed array without checking (real bug shape: reused buffer across branches).
void apply_order_by(OrderByTerm* fixed8, int n_terms, const OrderByTerm* terms) {
    for (int i = 0; i < n_terms; ++i) {
        fixed8[i] = terms[i];        // n_terms > 8 -> overflow
    }
}

int main() {
    OrderByTerm fixed[8];                       // capacity 8
    std::vector<OrderByTerm> crafted(20);       // crafted SELECT with 20 terms
    for (int i = 0; i < 20; ++i) crafted[i] = OrderByTerm{i, 0};
    apply_order_by(fixed, (int)crafted.size(), crafted.data());
    std::printf("applied 20 order-by terms into an 8-slot array\n");
    return 0;
}
