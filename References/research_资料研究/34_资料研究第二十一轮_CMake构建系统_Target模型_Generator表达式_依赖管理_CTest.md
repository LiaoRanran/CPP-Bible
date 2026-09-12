# 资料研究第二十一轮：CMake 构建系统——Target 模型、Generator 表达式、依赖管理与大型项目组织

> 2026-09-11，底层工程资料研究员。主题：现代 CMake 的 target 模型（PRIVATE/PUBLIC/INTERFACE）、target_* 命令 vs 全局命令、generator 表达式、依赖管理（find_package/FetchContent/ExternalProject/CPM/vcpkg/conan）、CTest 测试集成、大型项目组织与常见反模式。
> 检索方式：general_search + CMake 官方文档（cmake-buildsystem/cmake-generator-expressions/FetchContent/find_package）+ SimplifyC++ Mastering Modern CMake + CPM.cmake GitHub + CMake 官方 Testing 指南。
> **工程工具链域第一轮**。

---

## 一、现代 CMake 的核心理念：Target 模型

### 1. 哲学：把 target 当作对象

> **"Prefer targets over global flags."**
>
> 把每个可执行文件/库当作一个对象，给它附加属性（include 路径、编译定义、编译选项、链接库）。依赖通过 `target_link_libraries()` 显式声明，属性自动传递。

### 2. target_* 命令 vs 全局命令

| 功能 | 推荐（Target Specific） | 不推荐（Global） |
|---|---|---|
| 包含目录 | `target_include_directories()` | `include_directories()` |
| 编译定义 | `target_compile_definitions()` | `add_definitions()` |
| 编译选项 | `target_compile_options()` | `add_compile_options()` |
| 链接库 | `target_link_libraries()` | `link_libraries()` |
| C++ 标准 | `target_compile_features()` | `set(CMAKE_CXX_STANDARD ...)` |

### 3. 为什么全局命令是坏的？

- `include_directories()` 会把路径加到**所有**后续 target 的编译命令中——包括不需要的
- 导致编译命令膨胀、IDE 智能提示混乱、交叉污染
- 无法追踪"哪个 target 需要哪个 include 路径"
- target 模型让依赖关系显式化，属性只在需要的地方生效

- **来源**：CMake cmake-buildsystem(7) + SimplifyC++ Mastering Modern CMake + IPADS CMake 培训
- **可信度**：S

---

## 二、可见性：PRIVATE / PUBLIC / INTERFACE

### 1. 三种可见性

| 关键字 | 含义 | 类比 |
|---|---|---|
| `PRIVATE` | 只有 target 自己用，不传递 | 类的 private 成员 |
| `PUBLIC` | target 自己用 + 链接它的 target 也用 | 类的 public 成员 |
| `INTERFACE` | target 自己不用，只传递给链接它的 target | 纯接口（header-only 库） |

### 2. 经典示例

```cmake
add_library(mylib src/mylib.cpp)

# mylib 自己需要 src/（PRIVATE）
# 链接 mylib 的人需要 include/（PUBLIC，因为头文件在那里）
target_include_directories(mylib
    PRIVATE src
    PUBLIC  include
)

# mylib 自己用 spdlog 实现细节（PRIVATE）
# 链接 mylib 的人也需要 fmt（因为 mylib 的头文件用了 fmt 类型）（PUBLIC）
target_link_libraries(mylib
    PRIVATE spdlog::spdlog
    PUBLIC  fmt::fmt
)
```

### 3. header-only 库

```cmake
add_library(myheaderonly INTERFACE)  # 没有源文件，只有头文件
target_include_directories(myheaderonly INTERFACE include)
target_compile_features(myheaderonly INTERFACE cxx_std_20)
```

- `INTERFACE` 库没有编译输出，只是属性的集合
- 链接它的 target 自动获得所有 INTERFACE 属性

- **来源**：CMake cmake-buildsystem(7) + BenjaminYde CPP-Guide
- **可信度**：S

---

## 三、Generator 表达式（$<...>）

### 1. 什么是 generator 表达式？

- 在**生成构建系统时**求值（不是 configure 时）
- 语法：`$<表达式>` 或 `$<条件:值>`
- 用于根据配置（Debug/Release）、平台、语言等动态生成内容

### 2. 最常用的 generator 表达式

| 表达式 | 含义 | 典型用途 |
|---|---|---|
| `$<BUILD_INTERFACE:...>` | 构建时值为 `...`，安装时为空 | include 路径区分 |
| `$<INSTALL_INTERFACE:...>` | 安装时值为 `...`，构建时为空 | include 路径区分 |
| `$<CONFIG:cfg>` | 当前配置是 cfg 时为 1 | Debug/Release 区分 |
| `$<COMPILE_LANGUAGE:lang>` | 当前源文件语言是 lang 时为 1 | C/C++ 区分选项 |
| `$<IF:cond,then,else>` | 条件选择 | 三元表达式 |
| `$<TARGET_FILE:tgt>` | target 的输出文件路径 | 测试/安装 |
| `$<TARGET_PROPERTY:tgt,prop>` | target 的属性值 | 高级用法 |

### 3. 最经典模式：BUILD_INTERFACE vs INSTALL_INTERFACE

```cmake
target_include_directories(mylib PUBLIC
    # 构建时：用源码目录的 include
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    # 安装后：用安装目录的 include
    $<INSTALL_INTERFACE:include>
)
```

- 构建时，mylib 的头文件在源码目录的 `include/`
- 安装后，头文件被复制到 `CMAKE_INSTALL_PREFIX/include/`
- 同一个 target 在两种场景下都能正确找到头文件
- **这是创建可安装库的关键模式**

### 4. 按配置区分选项

```cmake
target_compile_options(mylib PRIVATE
    $<$<CONFIG:Debug>:-O0 -g>
    $<$<CONFIG:Release>:-O3 -DNDEBUG>
)
```

### 5. 按语言区分选项

```cmake
target_compile_options(mylib PRIVATE
    $<$<COMPILE_LANGUAGE:CXX>:-std=c++20>
    $<$<COMPILE_LANGUAGE:C>:-std=c11>
)
```

- **来源**：CMake cmake-generator-expressions(7) + X-Gen-Lab generator 表达式教程
- **可信度**：S

---

## 四、依赖管理：四种方式对比

### 1. find_package（找系统已安装的库）

```cmake
find_package(Boost 1.74 REQUIRED COMPONENTS filesystem system)
target_link_libraries(myapp PRIVATE Boost::filesystem Boost::system)
```

- **两种模式**：
  - **Config 模式**：找 `<Package>Config.cmake`（库自己提供，推荐）
  - **Module 模式**：找 `Find<Package>.cmake`（CMake 自带或第三方，传统方式）
- 现代 CMake 推荐用 `CONFIG` 关键字明确指定 Config 模式
- 优点：库已安装，构建快；缺点：需要系统预装，版本不可控

### 2. FetchContent（configure 时下载源码）

```cmake
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
FetchContent_MakeAvailable(googletest)
target_link_libraries(mytest PRIVATE GTest::gtest_main)
```

- CMake 3.11+ 内置
- **configure 时**下载，然后 `add_subdirectory()` 集成
- 依赖的 target 直接可用，可以 `target_link_libraries`
- 优点：无需预安装，版本可控；缺点：configure 慢（首次下载），无版本冲突解决

### 3. ExternalProject（build 时下载构建）

```cmake
include(ExternalProject)
ExternalProject_Add(
    mydep
    GIT_REPOSITORY https://github.com/user/mydep.git
    GIT_TAG        v1.0
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/external
)
```

- **build 时**下载、配置、构建、安装
- 独立构建，不能直接 `target_link_libraries`（需要手动指定路径）
- 适合需要特殊构建参数或交叉编译的依赖
- 现代项目中逐渐被 FetchContent 取代

### 4. 外部包管理器

| 工具 | 特点 | 适用场景 |
|---|---|---|
| **CPM.cmake** | FetchContent 的轻量包装器，加版本管理和缓存 | 小中型项目，不想引入外部工具 |
| **vcpkg** | Microsoft 开发，manifest 模式（vcpkg.json），源码编译+二进制缓存 | Windows 优先，跨平台 |
| **Conan** | 去中心化，二进制包+源码编译，跨构建系统 | 大型项目，复杂依赖图 |
| **Hunter** | 基于 CMake 的包管理器，纯 CMake 驱动 | 追求 CMake 原生体验 |

### 5. 选择决策

```
需要系统已安装的库？
├─ 是 → find_package（CONFIG 模式）
└─ 否 → 需要版本可控？
    ├─ 是 → 小项目？
    │   ├─ 是 → CPM.cmake / FetchContent
    │   └─ 否 → vcpkg / Conan
    └─ 否 → 特殊构建需求？
        ├─ 是 → ExternalProject
        └─ 否 → FetchContent
```

- **来源**：CMake Using Dependencies Guide + CPM.cmake GitHub + NDX 依赖管理
- **可信度**：S

---

## 五、CTest 测试集成

### 1. 基础设置

```cmake
# 顶层 CMakeLists.txt
include(CTest)  # 等价于 enable_testing()，但更完整
# 或
enable_testing()
```

### 2. 手动注册测试

```cmake
add_test(
    NAME mytest
    COMMAND mytest_executable --arg1 value1
)
```

### 3. GoogleTest 自动发现

```cmake
include(GoogleTest)
gtest_discover_tests(mytest_target)
```

- `gtest_discover_tests()` 在**构建后**扫描可执行文件，自动发现所有 `TEST()` 宏
- 比 `add_test()` 手动注册更方便，新增测试不需要改 CMake
- 每个 TEST 成为独立的 CTest 用例，可以单独运行

### 4. CTest 命令行

```bash
ctest                    # 运行所有测试
ctest -R mytest          # 运行名称匹配正则的测试
ctest -L integration     # 运行带标签的测试
ctest -j 4               # 并行运行 4 个
ctest --output-on-failure  # 失败时打印输出
ctest -C Debug           # 指定配置
```

### 5. 测试组织模式

```
project/
├── CMakeLists.txt       # 顶层：project, include(CTest)
├── src/
│   ├── CMakeLists.txt   # 库 target
│   └── ...
└── tests/
    ├── CMakeLists.txt   # 测试 targets
    ├── unit_test.cpp
    └── integration_test.cpp
```

- 大型项目按 scope 分测试 target（unit / integration / performance）
- 用 `set_tests_properties(... PROPERTIES LABELS "integration")` 打标签

- **来源**：CMake Testing 指南 + C++Now Effective CTest + Dr-Sergey GTest 集成
- **可信度**：S

---

## 六、大型项目组织

### 1. 推荐目录结构

```
myproject/
├── CMakeLists.txt          # 顶层：project(), 全局设置, add_subdirectory
├── cmake/                  # 自定义模块、工具链文件
│   ├── CompilerWarnings.cmake
│   └── Sanitizers.cmake
├── src/
│   ├── CMakeLists.txt      # 库/可执行文件 target
│   ├── core/
│   │   ├── CMakeLists.txt
│   │   └── ...
│   └── utils/
│       ├── CMakeLists.txt
│       └── ...
├── include/
│   └── myproject/          # 公共头文件
├── tests/
│   ├── CMakeLists.txt
│   └── ...
├── examples/
│   └── ...
└── third_party/            # 第三方依赖（可选）
```

### 2. 分层 CMakeLists

- 顶层：`project()`、全局编译选项（警告、标准）、`add_subdirectory(src)`、`add_subdirectory(tests)`
- 每个子目录：定义自己的 target，设置 target 属性
- 避免在顶层设置 `include_directories()` 等全局命令

### 3. Superbuild 模式

- 用 `ExternalProject_Add()` 管理多个子项目
- 每个子项目独立构建、独立安装
- 适合：项目之间有复杂依赖、需要不同编译选项、交叉编译
- 缺点：配置复杂，IDE 支持差

### 4. Monorepo 模式

- 所有子项目在一个仓库，用 `add_subdirectory()` 集成
- 共享构建配置、统一版本
- 适合：紧密耦合的组件、内部库
- 现代 CMake 推荐的模式

- **来源**：Professional CMake + pr0g cmake-examples + Wasil Zafar CMake 测试
- **可信度**：A

---

## 七、常见反模式

### 1. 用全局命令

```cmake
# ❌ 坏：所有 target 都加这个路径
include_directories(${CMAKE_SOURCE_DIR}/include)

# ✅ 好：只给需要的 target
target_include_directories(mylib PUBLIC include)
```

### 2. file(GLOB) 收集源文件

```cmake
# ❌ 坏：新增文件不触发重新配置，可能漏掉
file(GLOB SOURCES "src/*.cpp")
add_executable(myapp ${SOURCES})

# ✅ 好：显式列出
add_executable(myapp
    src/main.cpp
    src/utils.cpp
)
```

- CMake 3.12+ 加了 `CONFIGURE_DEPENDS` 选项，但仍不推荐（性能问题）

### 3. 用 CMAKE_CXX_STANDARD 而不是 target_compile_features

```cmake
# ❌ 坏：全局生效，无法区分 target
set(CMAKE_CXX_STANDARD 20)

# ✅ 好：只给需要的 target，且是"最低要求"
target_compile_features(mylib PUBLIC cxx_std_20)
```

### 4. 用 _LIBRARIES 变量而不是 target 名

```cmake
# ❌ 坏：传统 Find 模块的变量方式
target_link_libraries(myapp ${Boost_LIBRARIES})

# ✅ 好：现代 Config 模式的 target 方式
target_link_libraries(myapp PRIVATE Boost::filesystem)
```

### 5. In-source build

```bash
# ❌ 坏：构建产物污染源码目录
cmake .
make

# ✅ 好：out-of-source build
cmake -B build
cmake --build build
```

### 6. 不加 REQUIRED

```cmake
# ❌ 坏：找不到库时静默继续，后面报奇怪的链接错误
find_package(Boost)

# ✅ 好：找不到就立即报错，信息明确
find_package(Boost REQUIRED COMPONENTS filesystem)
```

- **来源**：SimplifyC++ Mastering Modern CMake + IPADS CMake 培训
- **可信度**：A+

---

## 八、知识网络

```
CMake 构建系统
├── 核心理念：Target 模型
│   ├── target 当作对象
│   ├── target_* 命令代替全局命令
│   └── 属性附加到 target，依赖自动传递
│
├── 可见性
│   ├── PRIVATE（自己用）
│   ├── PUBLIC（自己用+传递）
│   ├── INTERFACE（只传递，header-only）
│   └── 类比 C++ 访问控制
│
├── Generator 表达式
│   ├── $<BUILD_INTERFACE> / $<INSTALL_INTERFACE>
│   ├── $<CONFIG:cfg>（Debug/Release）
│   ├── $<COMPILE_LANGUAGE:lang>
│   ├── $<IF:cond,then,else>
│   └── $<TARGET_FILE:tgt>
│
├── 依赖管理
│   ├── find_package（系统已安装，Config 模式）
│   ├── FetchContent（configure 下载源码）
│   ├── ExternalProject（build 下载构建）
│   ├── CPM.cmake（FetchContent 包装器）
│   ├── vcpkg（Microsoft，manifest）
│   └── Conan（去中心化，二进制包）
│
├── CTest 测试
│   ├── include(CTest) / enable_testing()
│   ├── add_test()（手动）
│   ├── gtest_discover_tests()（自动发现）
│   ├── ctest 命令行（-R/-L/-j/--output-on-failure）
│   └── 按 scope 分测试 target
│
├── 大型项目组织
│   ├── 目录结构（src/include/tests/cmake/examples）
│   ├── 分层 CMakeLists
│   ├── Superbuild（ExternalProject）
│   └── Monorepo（add_subdirectory）
│
└── 常见反模式
    ├── 全局命令（include_directories 等）
    ├── file(GLOB) 收集源文件
    ├── CMAKE_CXX_STANDARD 代替 target_compile_features
    ├── _LIBRARIES 变量代替 target 名
    ├── In-source build
    └── find_package 不加 REQUIRED
```

---

## 九、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | CMake cmake-buildsystem(7) 官方文档 | S | Target 模型的权威定义 |
| 2 | CMake cmake-generator-expressions(7) | S | Generator 表达式的完整参考 |
| 3 | CMake Using Dependencies Guide | S | 依赖管理的官方指南 |
| 4 | CMake FetchContent 模块文档 | S | FetchContent 的权威说明 |
| 5 | SimplifyC++ Mastering Modern CMake PDF | A+ | 现代 CMake 的快速参考 |
| 6 | CPM.cmake GitHub | A | FetchContent 包装器的工业实践 |
| 7 | CMake Testing and CTest 指南 | S | CTest 的官方教程 |
| 8 | C++Now Effective CTest PDF | A | CTest 高级用法 |
| 9 | IPADS 现代 CMake 培训 | A | 中文视角的清晰教学 |
| 10 | pr0g cmake-examples GitHub | A | 大量现代 CMake 示例 |

## 十、强烈建议深入研究的 5 个资料

1. **CMake cmake-buildsystem(7)**——Target 模型和使用需求的完整定义
2. **SimplifyC++ Mastering Modern CMake PDF**——现代 CMake 的快速参考，适合随时查阅
3. **CPM.cmake**——读源码理解 FetchContent 的版本管理和缓存机制
4. **一个真实的大型 CMake 项目**——比如 LLVM、Qt、或 ClickHouse 的 CMakeLists.txt
5. **CMake Testing 指南**——CTest 的完整用法和最佳实践

## 十一、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| Target 模型 | "现代 CMake 的核心思想" | TOOL 域原子 |
| 可见性 | "PRIVATE/PUBLIC/INTERFACE 到底什么意思" | TOOL 域原子 |
| Generator 表达式 | "BUILD_INTERFACE 和 INSTALL_INTERFACE 的区别" | TOOL 域原子 |
| 依赖管理对比 | "四种引入第三方库的方式" | TOOL 域专题 |
| 常见反模式 | "CMake 最常见的 6 个错误" | TOOL 域专题 |

## 十二、对 CPP-Bible 的工程升级建议

1. **TOOL 域新增"现代 CMake"原子**——Target 模型+可见性+target_* 命令，这是 C++ 工程的基础
2. **TOOL 域新增"CMake 依赖管理"专题**——find_package/FetchContent/ExternalProject/CPM/vcpkg/conan 对比
3. **TOOL 域新增"CMake 常见反模式"专题**——6 大反模式+正确写法，最实用
4. **项目自身 CMake 升级**：检查是否用了全局命令、file(GLOB)、CMAKE_CXX_STANDARD 等反模式，逐步迁移到 target 模型
5. **证据卡新增构建实验**——性能类证据卡可以加"不同 CMake 配置的构建时间对比"

## 十三、发现的知识空白

1. **CMake 完全空白**——项目没有任何构建系统教学内容
2. **Target 模型空白**——现代 CMake 的核心思想完全没讲
3. **依赖管理空白**——find_package/FetchContent 等完全没讲
4. **CTest 空白**——测试集成完全没讲
5. **CMake 反模式空白**——最实用的避坑指南完全没讲

## 十四、下一轮推荐搜索方向

1. **编译器前端（按顺序）**——词法/语法分析、AST、语义分析、模板两阶段查找、name mangling、SFINAE
2. **C++ 对象模型与 ABI**——vtable、vptr、RTTI、内存布局、多重继承、虚继承、Itanium ABI
3. **性能分析与 profiling**——perf、gprof、Valgrind、cachegrind、火焰图、性能优化方法论
4. **数据库存储引擎**——B+树、LSM-tree、WAL、缓冲池、事务、MVCC
5. **网络编程与异步 IO**——epoll/io_uring、Reactor/Proactor、Boost.Asio、零拷贝

---

*本轮新增知识节点：CMake、现代 CMake、Target 模型、target_include_directories、target_compile_definitions、target_compile_options、target_link_libraries、target_compile_features、PRIVATE、PUBLIC、INTERFACE、使用需求、usage requirements、generator 表达式、BUILD_INTERFACE、INSTALL_INTERFACE、CONFIG、COMPILE_LANGUAGE、IF、TARGET_FILE、find_package、Config 模式、Module 模式、FetchContent、ExternalProject、CPM.cmake、vcpkg、Conan、Hunter、CTest、enable_testing、add_test、gtest_discover_tests、Superbuild、Monorepo、file(GLOB)、in-source build、out-of-source build、cxx_std_20、add_subdirectory、FetchContent_MakeAvailable。补齐了"CMake 构建系统"域的全部核心空白——这是工程工具链域的第一轮，也是所有 C++ 项目的基础。*
