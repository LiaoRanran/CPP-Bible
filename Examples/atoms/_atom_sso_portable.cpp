// ATOM-MEM-PERF-003 夹具一：SSO 容量与阈值**跨实现**可测（不依赖任何实现内部布局）。
//
// 观测手法（两条互相独立、都不预设实现）：
//   1) 地址归属：短串时 `s.data()` 是否落在 `s` 对象自身的字节范围内 ⇒ SSO 生效的**充分判据**；
//   2) capacity 读数：`s.capacity()` 在 SSO 生效时为实现内置容量。
// 阈值扫描：n 从 1 递增，记录第一个"数据落在堆上"的 n ⇒ SSO 容量 = n-1。
//
// 输出纪律（M2 §3）：每行 `标签=值`，值一律运行时算出；不写死任何期望值（S3 会拦）。
// 本夹具**不重载** operator new/delete ⇒ 断言可安全使用堆符号（P4 自证断言规则）。
#include <cstdio>
#include <string>

int main() {
    std::string probe;
    // 判据必须用**被检对象自身**的字节范围：每个 string 的 SSO 缓冲区在它自己内部。
    // （初版误用固定 probe 的范围去判别的对象 ⇒ 判据恒假、阈值扫描在 n=1 即停、
    //   输出 sso_capacity=0 这种荒谬值——观测通路活性对照正是为此而设。）
    const auto on_object = [](const std::string& s) {
        const char* b = reinterpret_cast<const char*>(&s);
        const char* p = s.data();
        return p >= b && p < b + sizeof(s);       // 数据落在对象字节内 ⇒ 无堆分配
    };

    std::printf("sizeof_string=%zu\n", sizeof(std::string));
    std::printf("sizeof_size_t=%zu\n", sizeof(std::size_t));

    // SSO 生效时的 capacity：先用一个短串读出来（实现自报的内置容量）
    probe.assign(1, 'a');
    std::printf("capacity_at_len1=%zu\n", probe.capacity());
    std::printf("capacity_at_len8=%zu\n", std::string(8, 'a').capacity());

    // 阈值扫描：首个“数据不在对象内”的长度
    std::size_t first_heap = 0;
    for (std::size_t n = 1; n <= 64; ++n) {
        std::string s(n, 'x');
        if (!on_object(s)) { first_heap = n; break; }
    }
    const std::size_t sso_cap = first_heap ? first_heap - 1 : 0;
    std::printf("first_heap_len=%zu\n", first_heap);        // 0 表示 64 内未触发堆
    std::printf("sso_capacity=%zu\n", sso_cap);

    // 阈值 ±1 的逐点确认（不靠推断，直接各测一次）
    for (std::size_t n = (sso_cap > 1 ? sso_cap - 1 : 1); n <= sso_cap + 2; ++n) {
        std::string s(n, 'x');
        std::printf("heap_at_len%zu=%d\n", n, on_object(s) ? 0 : 1);
    }

    // SSO 生效时 capacity 与 size 的关系（实现自报）
    std::string full(sso_cap, 'y');
    std::printf("capacity_at_sso_capacity=%zu\n", full.capacity());
    std::printf("size_at_sso_capacity=%zu\n", full.size());

    // 观测通路活性对照：把数据显式搬到堆上，同一条判据必须翻转
    std::string forced(sso_cap + 8, 'z');
    std::printf("heap_at_sso_capacity_plus8=%d\n", on_object(forced) ? 0 : 1);
    return 0;
}
