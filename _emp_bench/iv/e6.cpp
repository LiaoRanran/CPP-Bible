#include <cstdint>
constexpr std::uint32_t kBaud = 115200;
constexpr std::uint32_t kSysClk = 168000000;
constexpr std::uint16_t timer_psc(std::uint32_t clk, std::uint32_t baud){
    return static_cast<std::uint16_t>(clk / baud - 1);
}
static_assert(timer_psc(kSysClk, kBaud) == 1457);
int main(){ return timer_psc(kSysClk,kBaud); }
