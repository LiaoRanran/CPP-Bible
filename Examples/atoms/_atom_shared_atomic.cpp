// Examples/_atom_shared_atomic.cpp
// 服务 ATOM-MEM-SHARED-002：控制块引用计数是**原子**的——多线程各持一份 shared_ptr 副本并发
// 拷贝/销毁是安全的（计数收敛回 1），而 unique_ptr 恰恰禁止拷贝（类型系统层面）。
// 观测纪律（红队 S3 拦截后的修正）：
//   ① 线程只操作**各自的副本**，不并发读写同一个 shared_ptr 实例；
//   ② 夹具**自身不引入任何原子计数器**——每线程把拷贝次数写进自己的 vector 槽位，join 后主线程
//      求和。这样工件里出现的每一条 `lock` 指令都能归因于 shared_ptr 控制块，而不是夹具自己
//      （原版用 std::atomic<long> 计数，使断言对"引用计数失去原子性"的变异免疫）。
// 原子性的指令级证据由工件承担（见 EV-MEM-034）。
#include <cstdio>
#include <memory>
#include <thread>
#include <type_traits>
#include <vector>

int main() {
    const int nthreads = 4;
    const int iters = 2000;
    std::vector<long> per_thread(static_cast<std::size_t>(nthreads), 0);

    std::printf("threads=%d iterations=%d\n", nthreads, iters);
    std::printf("sizeof shared_ptr=%d\n", (int)sizeof(std::shared_ptr<int>));
    std::printf("shared_ptr copyable=%d\n", (int)std::is_copy_constructible<std::shared_ptr<int>>::value);
    std::printf("unique_ptr copyable=%d\n", (int)std::is_copy_constructible<std::unique_ptr<int>>::value);

    auto sp = std::make_shared<int>(42);
    std::printf("use_count before copies=%ld\n", (long)sp.use_count());

    {   // 确定性拷贝观测：把"拷贝会改变引用计数"钉住（定值 2，非并发窗口）
        std::shared_ptr<int> one_more = sp;
        std::printf("use_count after one copy=%ld\n", (long)sp.use_count());
    }

    std::vector<std::thread> ts;
    ts.reserve(static_cast<std::size_t>(nthreads));
    for (int i = 0; i < nthreads; ++i) {
        ts.emplace_back([sp, iters, &per_thread, i]() {       // 捕获即拷贝一份副本
            long local = 0;
            for (int k = 0; k < iters; ++k) {
                auto copy = sp;                               // 原子 ++ / 原子 --
                (void)copy;
                local = local + 1;
            }
            per_thread[static_cast<std::size_t>(i)] = local;   // 各写各的槽：夹具自身无需原子
        });
    }
    for (auto& t : ts) t.join();                               // join 后计数必然收敛

    long total = 0;
    for (long v : per_thread) total = total + v;

    std::printf("copies observed=%ld\n", total);
    std::printf("use_count after join=%ld\n", (long)sp.use_count());
    std::printf("value=%d\n", *sp);
    return 0;
}
