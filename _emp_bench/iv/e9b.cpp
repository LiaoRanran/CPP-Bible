#include <cstdint>
template <std::uintptr_t Addr>
struct Register {
    static volatile std::uint32_t& ref() { return *reinterpret_cast<volatile std::uint32_t*>(Addr); }
    static void write(std::uint32_t v)         { ref() = v; }
    static void set_bits(std::uint32_t mask)   { ref() |= mask; }
    static void clear_bits(std::uint32_t mask) { ref() &= ~mask; }
    static std::uint32_t read()                { return ref(); }
};
using GPIOA_BSRR = Register<0x40020018>;       // 只写置位/复位寄存器
void led_on() { GPIOA_BSRR::write(1u << 5); }  // 单条原子写，无读
