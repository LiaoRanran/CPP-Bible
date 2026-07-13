/* 文件：Examples/_ch17_stm32.ld
 * STM32F4（Cortex-M4）最小链接脚本示意：描述 Flash/RAM 布局与入口。
 * 交叉链接：arm-none-eabi-ld -T Examples/_ch17_stm32.ld ... -o firmware.elf
 */
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

ENTRY(_start)

SECTIONS
{
  .text : {
    KEEP(*(.isr_vector))   /* 中断向量表必须最先放 */
    *(.text*)
  } > FLASH

  .rodata : { *(.rodata*) } > FLASH
  .data   : { *(.data*) } > RAM AT > FLASH
  .bss    : { *(.bss*) } > RAM

  /* 提供 _sdata/_edata/_sbss/_ebss 供启动代码搬移 .data */
  _sdata = .;
  _edata = .;
  _sbss  = .;
  _ebss  = .;
}
