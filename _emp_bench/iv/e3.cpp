#include <cstdint>
constexpr std::uintptr_t GPIOA_BASE = 0x40020000;
constexpr std::uintptr_t ODR_OFFSET = 0x14;
inline volatile std::uint32_t& GPIOA_ODR =
    *reinterpret_cast<volatile std::uint32_t*>(GPIOA_BASE + ODR_OFFSET);
void toggle_pin5() { GPIOA_ODR ^= (1u << 5); }
