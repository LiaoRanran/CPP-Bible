// sample_G085
// defect_type: logic_error
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2022-0847 (https://nvd.nist.gov/vuln/detail/CVE-2022-0847) [linux-kernel]
// (authoritative annotation in sample_G085.json)
#include <cstdio>
#include <cstring>
// CVE-2022-0847 (用户态等价): pipe_buffer.flags 脏值 → 越权合并写
static const int PIPE_BUF_CAN_MERGE = 0x10;

struct PipeBuffer {
    int  flags;       // 原始缺陷: 新槽位未初始化 → 沿用脏值
    char page[32];
    int  page_owner;  // 该页当前归属的"文件"
};

static PipeBuffer g_ring[2];
static int g_victim_content = 0;

static void pipe_write_init_slot(int idx, const char* data, int owner) {
    /* DEFECT */ // 原始缺陷: flags 未初始化(copy_page_to_iter_pipe 路径)
    g_ring[idx].page_owner = owner;
    std::strncpy(g_ring[idx].page, data, 31);
}

int main() {
    // 第 1 轮: 槽位 0 写满, flags 被置为 CAN_MERGE(本轮合法)
    g_ring[0].flags = PIPE_BUF_CAN_MERGE;
    pipe_write_init_slot(0, "DATA-ROUND-1", 1);
    // 页被回收到页池并转分配给"受害文件"(页内容被替换)
    g_ring[0].flags = 0;                     // ← 注意: 真实缺陷是这里【没有】清 flags
    g_ring[0].flags = PIPE_BUF_CAN_MERGE;    // 模拟脏值残留
    pipe_write_init_slot(0, "DATA-ROUND-2", 2);   // 页 now 归属受害文件
    // 第 2 轮: 因为 flags 仍是 CAN_MERGE(脏值), 写入越过本文件数据边界,
    // 直接改写页内"受害文件"的内容 —— 页缓存被穿透
    g_victim_content = 42;
    std::strncpy(g_ring[0].page + 12, "HACKED", 7);   // 越过 round-2 数据边界写
    std::printf("victim page content after write: %s (期望: DATA-ROUND-2 前缀完好)\n",
                g_ring[0].page);
    std::printf("(正确行为: 新 pipe_buffer 的 flags 必须清零, 不可合并写)\n");
    return 0;
}
