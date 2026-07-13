// C13 steady_clock 精度查询：duration 的 ticks 每 period 多少
#include <iostream>
#include <chrono>
int main() {
    using namespace std::chrono;
    std::cout << "steady period = 1/" << steady_clock::period::den << " s"
              << " (即 ~" << (1e9 / steady_clock::period::den) << " ns 分辨率)\n";
    auto now = steady_clock::now();
    std::cout << "now ticks = " << now.time_since_epoch().count() << "\n";
    return 0;
}