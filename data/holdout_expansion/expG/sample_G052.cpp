// sample_G052
// defect_type: null_deref
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2020-11655 (https://nvd.nist.gov/vuln/detail/CVE-2020-11655) [sqlite]
// (authoritative annotation in sample_G052.json)
#include <cstdio>
// CVE-2020-11655: AggInfo 初始化被错误处理 → NULL 解引用
struct AggInfo {
    int    n_column;
    char** columns;   // 初始化失败时应保持 NULL 且调用方必须停止
};

static int parse_window_query(bool malformed, AggInfo* agg) {
    agg->n_column = 1;
    if (malformed) {
        agg->columns = 0;   // 初始化失败(畸形查询)
        return -1;
    }
    agg->columns = new char*[1];
    agg->columns[0] = new char[8];
    return 0;
}

static void walk_agg_columns(const AggInfo* agg) {
    /* DEFECT */ // 原始缺陷: 初始化失败的 AggInfo 仍被遍历
    for (int i = 0; i < agg->n_column; ++i) {
        std::printf("col %d: %s\n", i, agg->columns[i]);   // columns 为 NULL → SEGV
    }
}

int main() {
    AggInfo agg;
    parse_window_query(true, &agg);   // 畸形窗口函数查询
    walk_agg_columns(&agg);           // 调用方未检查解析结果 → 崩溃
    return 0;
}
