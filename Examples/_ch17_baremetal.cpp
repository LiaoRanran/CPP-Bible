// 文件：Examples/_ch17_baremetal.cpp
// 裸机（freestanding）最小程序示例：不依赖 libc，自定义入口 _start。
// 注意：本机 MinGW 无裸机运行环境，此文件用于说明源码形态，不在此链接运行。
// 交叉编译示意（arm-none-eabi-gcc 本机未安装）：
//   arm-none-eabi-g++ -std=c++23 -ffreestanding -nostdlib \
//       -T Examples/_ch17_stm32.ld -o firmware.elf _ch17_baremetal.cpp

#include <cstdint>

// 假定 MCU 寄存器映射（仅示意，非真实地址）
volatile uint32_t& RCC_AHB1ENR = *reinterpret_cast<uint32_t*>(0x40023830u);
volatile uint32_t& GPIOA_ODR   = *reinterpret_cast<uint32_t*>(0x40020014u);

// 自定义入口；链接脚本把它放进复位向量
extern "C" void _start() {
    RCC_AHB1ENR |= (1u << 0);   // 使能 GPIOA 时钟
    GPIOA_ODR   |= (1u << 5);   // PA5 置高（点亮 LED）
    for (;;) {                   // 裸机无退出，原地自旋
        GPIOA_ODR ^= (1u << 5);
    }
}
