#include <cstdint>
#define GPIOA_BSRR (*(volatile std::uint32_t*)0x40020018)
void led_on_macro() { GPIOA_BSRR |= (1u<<5); }
