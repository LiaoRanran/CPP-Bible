// 文件：Examples/_ch159_future.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_future.cpp -o Examples/_ch159_future.exe
// 说明：std::packaged_task / std::async / 异常传播 对比。
#include <cstdio>
#include <exception>
#include <future>
#include <stdexcept>

int compute(int x) { return x * x; }

int risky(bool fail) {
    if (fail) throw std::runtime_error("boom from task");
    return 42;
}

int main() {
    // packaged_task：可手动调度、获取 future
    std::packaged_task<int(int)> pt(compute);
    std::future<int> f = pt.get_future();
    pt(9);  // 在线程池里这步由 worker 执行
    std::printf("packaged_task result = %d\n", f.get());

    // async：fire-and-forget 由运行时决定线程
    auto fa = std::async(std::launch::async, compute, 7);
    std::printf("async result = %d\n", fa.get());

    // 异常传播：task 抛异常 -> future.get() 重抛
    std::packaged_task<int(bool)> pt2(risky);
    std::future<int> f2 = pt2.get_future();
    pt2(true);
    try {
        f2.get();
    } catch (const std::exception& e) {
        std::printf("caught exception: %s\n", e.what());
    }
}
