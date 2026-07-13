# 文件：Examples/_ch17_arm_toolchain.cmake
# CMake 交叉编译工具链文件：目标 = ARM Cortex-M4（arm-none-eabi）
# 用法：cmake -B build -DCMAKE_TOOLCHAIN_FILE=Examples/_ch17_arm_toolchain.cmake -S .

set(CMAKE_SYSTEM_NAME Generic)        # 无 OS（裸机）
set(CMAKE_SYSTEM_PROCESSOR arm)

# 交叉编译器（需先安装 GNU Arm Embedded / arm-none-eabi-gcc）
set(CMAKE_C_COMPILER   arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

# 告诉 find_* 不要去主机系统找库/头
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# 目标专用编译标志（裸机 + 软浮点 + Cortex-M4）
set(CMAKE_CXX_FLAGS_INIT "-mcpu=cortex-m4 -mthumb -mfloat-abi=soft -ffreestanding -nostdlib")
