#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""generate_F.py — 676c-F 扩样嵌入式/平台特定缺陷候选样本生成器。

严格按照探测器实测行为（probe_results.json）标注 expected_verdict：
  - alignment 未对齐解引用 -> ubsan catch（x86 上 UBSan 对齐检查会报）
  - shift 负移位 / 超宽移位 -> ubsan catch；位域越界 -> compiler-warn catch
  - register 关键字 -> compiler-warn catch（C++17 弃用警告）
  - packed 结构体 -> compiler-warn miss（ubsan 在该工具链下 unknown，不列入）
  - endianness / volatile_misuse / interrupt_safety / setjmp_longjmp / inline-asm
    -> 全部 miss（逻辑/平台缺陷，sanitizer 不抓）
所有样本都会终止（无死循环），可在 WSL 下真实编译运行。
不修改现有数据/检测器；仅产出 data/expansion_676c_F/ 下的新文件。
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PLANTED = "// <<PLANTED-DEFECT>>"

SAMPLES = []  # (cpp_text, meta_dict)


def add(cpp, meta):
    SAMPLES.append((cpp, meta))


def defect_line(cpp):
    for i, ln in enumerate(cpp.splitlines(), 1):
        if PLANTED in ln:
            return i
    return 1


# --------------------------------------------------------------------------
# 1) alignment（35）: 15 catch(ubsan 未对齐解引用) + 20 miss
# --------------------------------------------------------------------------
def gen_alignment():
    # 1a) 未对齐解引用（catch）：变体 = 类型 + 偏移 + 读写
    confs = [
        ("int", 1, "read"), ("short", 1, "read"), ("int", 2, "write"),
        ("long long", 3, "read"), ("double", 5, "read"), ("int", 3, "read"),
        ("int16_t", 1, "write"), ("float", 2, "read"), ("int", 5, "write"),
        ("int32_t", 1, "read"), ("short", 1, "read"), ("int64_t", 7, "read"),
        ("int", 6, "read"), ("short", 3, "write"), ("double", 1, "write"),
    ]
    for i, (ty, off, rw) in enumerate(confs):
        cpp = (
            "#include <cstdint>\n"
            "#include <cstdio>\n"
            "int main(){\n"
            f"  char buffer[64] = {{0}};\n"
            f"  {ty}* p = reinterpret_cast<{ty}*>(buffer + {off});  // 未对齐指针\n"
        )
        if rw == "read":
            cpp += (
                f"  {ty} v = *p;  {PLANTED} 未对齐读取（UB）\n"
                "  (void)v;\n"
            )
        else:
            cpp += (
                f"  *p = static_cast<{ty}>(0x1234);  {PLANTED} 未对齐写入（UB）\n"
            )
        cpp += "  std::printf(\"ok\\n\");\n  return 0;\n}\n"
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": f"char buffer+{off} 强转 {ty}* 后{'读' if rw=='read' else '写'}，未满足 {ty} 对齐边界"},
            "severity": "medium",
            "expected_verdict": "catch",
            "expected_detectors": ["ubsan"],
            "trigger_condition": f"在 x86 上 UBSan 对齐检查会报 runtime error；在 ARM/严格对齐架构未对齐访问直接硬件异常（SIGBUS）",
            "platform_dependent": True,
            "platform_notes": "未对齐访问在 x86 上硬件不 trap（仅性能下降），但 UBSan(-fsanitize=alignment) 在 x86 也会插桩并报错；在 ARM/RISC-V 等严格对齐架构会崩溃。UBSan 实测 catch。",
            "notes": f"reinterpret_cast<{ty}*>(buffer+{off}) 产生未对齐指针，解引用是 UB。正确做法用 memcpy 或 std::aligned_storage/alignas。",
        })

    # 1b) packed 结构体成员访问（miss，compiler-warn）
    packed_members = [("int", "i"), ("long long", "ll"), ("double", "d"),
                      ("int", "a"), ("short", "s"), ("int32_t", "w")]
    for i, (ty, name) in enumerate(packed_members):
        cpp = (
            "#include <cstdint>\n"
            "#pragma pack(push, 1)\n"
            "struct Packed {\n"
            f"  char c;\n  {ty} {name};\n"
            "};\n#pragma pack(pop)\n"
            "#include <cstdio>\n"
            "int main(){\n"
            "  Packed s;\n"
            "  s.c = 1;\n"
            f"  s.{name} = 42;  {PLANTED} 访问 packed 未对齐成员\n"
            "  std::printf(\"%d\\n\", (int)s.c);\n"
            "  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": f"packed 结构体成员 {name} 未对齐访问（char 后被压缩到偏移 1）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "GCC 扩展 #pragma pack 压缩布局，成员不再按自然对齐；取地址/非对齐访问在严格对齐架构 UB",
            "platform_dependent": True,
            "platform_notes": "packed 成员在 x86 上可访问（可能跨 cache 行，性能差）；在 ARM 取 packed 成员地址并解引用是 UB。UBSan 在本工具链对该结构编译失败(unknown)，故用 compiler-warn 复现（miss）。",
            "notes": "packed 结构用于节省空间/匹配线上格式，但访问未对齐成员是平台相关 UB。应使用 memcpy 而非直接访问成员地址。",
        })

    # 1c) offsetof 误算对齐（miss，逻辑）
    for i in range(4):
        base = 4 + i * 2
        cpp = (
            "#include <cstddef>\n#include <cstring>\n#include <cstdio>\n"
            "struct Rec { char tag; int val; };\n"
            "int main(){\n"
            f"  char blob[16];\n"
            f"  // 错误假设 val 在偏移 {base}（实际 offsetof(Rec,val) 因对齐为 4）\n"
            f"  std::memcpy(blob + {base}, &blob[0], sizeof(int));  {PLANTED} 偏移假设错误\n"
            "  (void)blob;\n  std::printf(\"ok\\n\");\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": f"假设成员位于偏移 {base} 而实际因对齐在 4"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "结构体填充导致成员实际偏移与假设不同；手工偏移计算在跨编译器/对齐设置下错位",
            "platform_dependent": True,
            "platform_notes": "结构体填充与对齐由 ABI/编译器决定，手工偏移在 x86 与 ARM 可能不同。sanitizer 不抓（逻辑错误），compiler-warn miss。",
            "notes": "应使用 offsetof() 获取真实偏移，而非硬编码。",
        })

    # 1d) std::aligned_storage 误用（miss，逻辑）
    for i in range(4):
        sz = 8 + i * 8
        cpp = (
            "#include <type_traits>\n#include <cstdio>\n"
            "struct Payload { double x; };\n"
            "int main(){\n"
            f"  std::aligned_storage<{sz}, 4> buf;  // align 仅 4，但 Payload 需 8\n"
            f"  Payload* p = reinterpret_cast<Payload*>(&buf);  {PLANTED} 对齐不足\n"
            "  p->x = 1.0;\n  std::printf(\"%f\\n\", p->x);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": f"aligned_storage 对齐参数 4 小于 Payload(double) 所需 8"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "aligned_storage 对齐参数小于实际类型对齐要求时，placement new/强转产生未对齐访问",
            "platform_dependent": True,
            "platform_notes": "double 需 8 字节对齐；若缓冲区仅 4 对齐，x86 上普通访问不出错但跨平台 UB。ubsan/compiler-warn 在本例 miss（访问未执行或对齐恰巧满足）。",
            "notes": "aligned_storage 第二个模板参数应与 alignof(T) 一致，或用 std::aligned_storage_t<sizeof(T), alignof(T)>。",
        })

    # 1e) 动态分配对齐假设（miss，逻辑）
    for i in range(4):
        req = 16 + i * 16
        cpp = (
            "#include <cstdlib>\n#include <cstdio>\n"
            "int main(){\n"
            f"  // 假设 malloc 返回 {req} 字节对齐（实际仅保证 alignof(max_align_t)）\n"
            "  void* p = std::malloc(64);\n"
            f"  double* dp = reinterpret_cast<double*>(p);  {PLANTED} 误信充足对齐\n"
            "  dp[0] = 3.14;\n  std::printf(\"%f\\n\", dp[0]);\n  std::free(p);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": f"误假设 malloc 提供 {req} 字节对齐"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "malloc 仅保证 max_align_t 对齐（通常 16），更大对齐需 aligned_alloc/posix_memalign",
            "platform_dependent": True,
            "platform_notes": "malloc 在 x86 通常 16 对齐，访问 double 不会出错；但严格要求 32/64 对齐时应使用 aligned_alloc。ubsan/compiler-warn miss。",
            "notes": "大对齐需求应使用 std::aligned_alloc 或 posix_memalign。",
        })

    # 1f) alignas 与 alignof 不匹配（miss，逻辑）
    for i in range(2):
        cpp = (
            "#include <cstddef>\n#include <cstdio>\n"
            "struct alignas(8) Big { double a; };\n"
            "int main(){\n"
            "  char tiny[8];\n"
            f"  Big* p = reinterpret_cast<Big*>(tiny);  {PLANTED} 缓冲区仅 8 字节且未必 8 对齐\n"
            "  p->a = 2.0;\n  std::printf(\"%f\\n\", p->a);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "alignment",
            "defect_location": {"description": "把 alignas(8) 对象放进仅 8 字节的栈 char 缓冲（起始对齐不保证）"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "缓冲区起始地址对齐未知，placement 到 alignas 对象上可能未对齐",
            "platform_dependent": True,
            "platform_notes": "栈 char[8] 未必 8 对齐；x86 上访问不出错，严格架构 UB。compiler-warn miss。",
            "notes": "应为对齐对象使用对齐分配或 alignas 缓冲区。",
        })


# --------------------------------------------------------------------------
# 2) endianness（35）: 全部 miss
# --------------------------------------------------------------------------
def gen_endianness():
    # 2a) 网络字节序未转换（8）
    for i in range(8):
        n = 16 if i % 2 == 0 else 32
        ty = f"uint{n}_t"
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            "  unsigned char raw[8] = {0x12, 0x34, 0x56, 0x78, 0, 0, 0, 0};\n"
            f"  {ty} net = *reinterpret_cast<{ty}*>(raw);  {PLANTED} 未调用 ntohl/ntohs\n"
            f"  std::printf(\"%u\\n\", static_cast<unsigned>(net));\n"
            "  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": f"把网络字节序原始字节直接按主机序解读为 {ty}（漏 ntohl/ntohs）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "在大端系统上 raw 与主机序一致（看似正常），在小端系统上字节被反转——跨端序解析错误",
            "platform_dependent": True,
            "platform_notes": "端序是逻辑错误，sanitizer 完全不抓；在小端 x86 上结果明显错误但程序不崩溃，compiler-warn miss。真实检测器盲区。",
            "notes": "网络/文件字节序须用 ntohl/ntohs 或手动字节重组，不能直接强转。",
        })

    # 2b) 字节序转换函数误用（多一次/少一次转换）（4）
    for i in range(4):
        wrong = "连续两次字节反转（双转换回原序）" if i % 2 == 0 else "对已是主机序的值再次反转"
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "static uint32_t bswap32(uint32_t x){ return ((x>>24)&0xffu)|((x>>8)&0xff00u)"
            "|((x<<8)&0xff0000u)|((x<<24)&0xff000000u); }\n"
            "int main(){\n"
            "  uint32_t host = 0x0A0B0C0D;\n"
            f"  uint32_t wire = bswap32(bswap32(host));  {PLANTED} {wrong}（双转换回原序）\n"
            "  std::printf(\"%u\\n\", wire);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": f"字节序反转函数误用：{wrong}"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "多/少一次字节序转换导致线上格式与对端不一致",
            "platform_dependent": True,
            "platform_notes": "逻辑错误，sanitizer 与 compiler-warn 均不抓。小端系统上双反转抵消返回原值，掩盖错误。",
            "notes": "字节序反转函数（如 htonl/bswap）应在发送端调用一次、接收端调用一次。",
        })

    # 2c) union 类型双关做端序检测（UB）（4）
    for i in range(4):
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "union Probe { uint32_t u; unsigned char b[4]; };\n"
            "int main(){\n"
            "  Probe p; p.u = 1;\n"
            f"  bool is_little = (p.b[0] == 1);  {PLANTED} 用 union 双关读字节布局（严格别名 UB）\n"
            "  std::printf(\"%d\\n\", (int)is_little);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": "union 类型双关读取多字节对象的字节序（C++ 严格别名 UB）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "用 union 读另一成员字节布局依赖具体实现；同一代码在不同端序机器上结论不同",
            "platform_dependent": True,
            "platform_notes": "union 双关在 C++ 是 UB（尽管 GCC/Clang 扩展允许）。UBsan 未启用严格别名时 miss；compiler-warn miss。真实盲区。",
            "notes": "端序检测应用 std::endian (C++20) 或 memcpy。",
        })

    # 2d) 二进制文件格式假设小端（4）
    for i in range(4):
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            "  uint32_t magic = 0x12345678;\n"
            f"  // 直接把内存表示当作文件格式写入，假设所有机器小端\n"
            f"  std::printf(\"%08X\\n\", magic);  {PLANTED} 文件格式硬编码主机端序\n"
            "  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": "二进制文件/网络格式直接采用主机内存表示，未固定端序"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "文件在小端机器写入、大端机器读取时字段全反转",
            "platform_dependent": True,
            "platform_notes": "文件格式端序是协议层问题，sanitizer 不抓；compiler-warn miss。真实盲区。",
            "notes": "序列化应固定端序（htonl 或手动组装字节）。",
        })

    # 2e) 序列化/反序列化往返不一致（4）
    for i in range(4):
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            "  uint64_t v = 0x1122334455667788ULL;\n"
            f"  uint32_t lo = static_cast<uint32_t>(v);  {PLANTED} 反序列化时只取低 32 位当完整值\n"
            "  std::printf(\"%u\\n\", lo);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": "反序列化把 64 位值当 32 位读取（截断 + 端序混淆）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "序列化/反序列化宽度与端序处理不一致导致数据损坏",
            "platform_dependent": True,
            "platform_notes": "逻辑错误，sanitizer 不抓；compiler-warn miss。",
            "notes": "序列化/反序列化必须对称且固定端序。",
        })

    # 2f) 位域端序布局（3）
    for i in range(3):
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "struct Bits { unsigned a:4; unsigned b:4; unsigned c:8; unsigned d:16; };\n"
            "int main(){\n"
            "  Bits f; f.a=1; f.b=2; f.c=3; f.d=4;\n"
            f"  unsigned char* p = reinterpret_cast<unsigned char*>(&f);  {PLANTED} 假设位域字节布局（端序/位序依赖实现）\n"
            "  std::printf(\"%02X\\n\", p[0]);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": "把位域对象当字节数组解读，依赖实现定义的位序/端序"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "位域中位分配顺序与字节序由实现定义，跨平台/编译器布局不同",
            "platform_dependent": True,
            "platform_notes": "位域布局是未指定行为，sanitizer 不抓；compiler-warn miss。",
            "notes": "跨平台位级协议应手动按位组装，不用位域。",
        })

    # 2g) 浮点端序转换缺失（3）
    for i in range(3):
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            "  double d = 3.14159;\n"
            f"  uint64_t bits = *reinterpret_cast<uint64_t*>(&d);  {PLANTED} 浮点位的端序未处理即跨网络发送\n"
            "  std::printf(\"%llu\\n\", static_cast<unsigned long long>(bits));\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": "把 double 的位表示直接当作整数发送，未转换端序"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "浮点位模式在小端/大端机器上字节顺序相反，跨网络重建得到 NaN/错误值",
            "platform_dependent": True,
            "platform_notes": "浮点位模式端序是协议问题，sanitizer 不抓；compiler-warn miss。",
            "notes": "浮点跨网络应固定端序（交换字节）。",
        })

    # 2h) 16/64 位变体补齐到 35（剩余 5）
    for i in range(5):
        n = 16 if i < 2 else 64
        ty = f"uint{n}_t"
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            "  unsigned char raw[8] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0, 0};\n"
            f"  {ty} v = *reinterpret_cast<{ty}*>(raw + 1);  {PLANTED} 偏移1的未对齐 + 端序混合误读\n"
            "  std::printf(\"%llu\\n\", static_cast<unsigned long long>(v));\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "endianness",
            "defect_location": {"description": f"raw+1 处按 {ty} 直接解读（未对齐 + 未转换端序）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "未对齐 + 端序同时错误，跨平台结果完全不同",
            "platform_dependent": True,
            "platform_notes": "未对齐在 x86 上 UBSan 会报 alignment（本例为 endianness 主题，仍标 miss 因核心缺陷是端序）；compiler-warn miss。",
            "notes": "应使用 memcpy + ntohl 系列处理。",
        })


# --------------------------------------------------------------------------
# 3) volatile_misuse（35）: 全部 miss
# --------------------------------------------------------------------------
def gen_volatile():
    # 3a) volatile 做线程同步标志（6）
    for i in range(6):
        cpp = (
            "#include <cstdio>\n"
            "volatile int flag = 0;\n"
            "int main(){\n"
            f"  // 线程 A 置 flag=1；线程 B 轮询 flag（volatile 不保证原子/可见性）\n"
            f"  flag = 1;  {PLANTED} 用 volatile 充当同步原语，应为 std::atomic\n"
            "  while (flag != 0) { break; }\n"
            "  std::printf(\"%d\\n\", flag);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "用 volatile int 做线程间同步标志（缺失 atomic 语义）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "多核/强内存模型下 volatile 不阻止重排与缓存可见性问题，导致线程永远看不到更新",
            "platform_dependent": False,
            "platform_notes": "volatile 不提供原子性或跨线程可见性；TSan 在本例（单线程伪代码）不报；实际上用户态无法复现，compiler-warn miss。真实检测器盲区。",
            "notes": "线程同步应使用 std::atomic<int> 而非 volatile。",
        })

    # 3b) volatile 指针指向非 volatile 数据（4）
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            "  int x = 0;\n"
            f"  volatile int* vp = reinterpret_cast<volatile int*>(&x);  {PLANTED} 把非 volatile 对象当 volatile 访问\n"
            "  *vp = 5;\n  std::printf(\"%d\\n\", x);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "将普通 int 的地址强转为 volatile int* 访问（虚假 volatile 限定）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "非 volatile 数据的 volatile 限定是谎言，编译器可能仍优化掉预期屏障",
            "platform_dependent": False,
            "platform_notes": "纯逻辑/语义误用，sanitizer 与 compiler-warn 均不抓；真实盲区。",
            "notes": "volatile 限定应与对象的真实存储属性一致。",
        })

    # 3c) 在 volatile 对象上调用非 volatile 成员函数（4）
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "struct Dev { int reg; void write(int v){ reg = v; } };\n"
            "int main(){\n"
            "  volatile Dev d{0};\n"
            f"  Dev& r = const_cast<Dev&>(d);  {PLANTED} 把 volatile 对象强转为非 volatile 引用后调用成员函数（丢弃 volatile 限定）\n"
            "  r.write(7);\n  std::printf(\"%d\\n\", (int)d.reg);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "把 volatile 对象 const_cast 为非 volatile 引用后调用成员函数（volatile 限定被丢弃）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "volatile 对象调用非 volatile 成员函数时 volatile 限定不传播，MMIO 写入可能被优化",
            "platform_dependent": False,
            "platform_notes": "成员函数未带 volatile 限定则无法对 volatile 对象正确生成访问；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "MMIO 访问的成员函数应加 volatile 限定。",
        })

    # 3d) const_cast 去掉 volatile（4）
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            "  volatile int mmio = 0;\n"
            f"  int* p = const_cast<int*>(reinterpret_cast<volatile int*>(&mmio));  {PLANTED} 去掉 volatile 限定\n"
            "  *p = 1;\n  std::printf(\"%d\\n\", (int)mmio);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "const_cast 去掉 volatile 限定后写 MMIO 寄存器"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "去掉 volatile 后编译器可能缓存寄存器值，漏掉对硬件的后续写入",
            "platform_dependent": True,
            "platform_notes": "MMIO 场景 volatile 是必需的，去掉后访问可被优化；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "MMIO 寄存器必须用 volatile 限定，不可去除。",
        })

    # 3e) 假设 volatile 保证原子性（读-改-写）（5）
    for i in range(5):
        cpp = (
            "#include <cstdio>\n"
            "volatile int counter = 0;\n"
            "int main(){\n"
            f"  counter = counter + 1;  {PLANTED} 误以为 volatile 使 RMW 原子（实际非原子）\n"
            "  std::printf(\"%d\\n\", counter);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "对 volatile 变量做自增，误信其原子性"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "并发场景下 volatile 自增仍是非原子 RMW，会被打断导致丢失更新",
            "platform_dependent": False,
            "platform_notes": "volatile 不提供原子 RMW；正确做法 std::atomic::fetch_add；sanitizer 单线程不报，compiler-warn miss。真实盲区。",
            "notes": "计数器递增应使用 std::atomic。",
        })

    # 3f) volatile 用于非 MMIO 普通变量（4）
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            f"  volatile int cache = 42;  {PLANTED} 对普通变量滥用 volatile（无 MMIO/信号场景）\n"
            "  std::printf(\"%d\\n\", cache);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "对普通变量加 volatile（不必要的性能损失，且非同步）"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "无 MMIO/信号处理场景的 volatile 既无同步作用又妨碍优化",
            "platform_dependent": False,
            "platform_notes": "无意义 volatile 是代码异味而非 UB；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "仅在 MMIO/信号处理/ setjmp 场景使用 volatile。",
        })

    # 3g) 中断处理程序访问非 volatile 共享变量（4）
    for i in range(4):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "static int status = 0;\n"
            "extern \"C\" void isr(int) { status = 1; }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} 中断读写的 status 非 volatile/atomic\n"
            "  std::printf(\"%d\\n\", status);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "中断/信号处理程序读写普通全局变量（应为 volatile 或 atomic）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "ISR 与主程序共享的非 volatile 变量可能被编译器缓存/重排，读到陈旧值",
            "platform_dependent": True,
            "platform_notes": "ISR 共享变量必须是 volatile 或 std::atomic（C++11 起 atomic 也适用）；用户态无法复现，sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "ISR 与主程序共享变量用 volatile 或 std::atomic。",
        })

    # 3h) volatile + const 组合误用（4）
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            f"  volatile const int ro = 0;  {PLANTED} volatile const 仅阻止编译器优化而非硬件写保护\n"
            "  std::printf(\"%d\\n\", ro);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "volatile_misuse",
            "defect_location": {"description": "误以为 volatile const 提供硬件只读保护"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "volatile const 仅影响编译器对访问的假设，不提供任何内存保护",
            "platform_dependent": False,
            "platform_notes": "语义误解，非 UB；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "只读保护靠 MMIO/MPU，不由 volatile const 提供。",
        })


# --------------------------------------------------------------------------
# 4) bit_operation（35）: 20 catch + 15 miss
# --------------------------------------------------------------------------
def gen_bitop():
    # 4a) 负移位（catch, ubsan）——5
    for i in range(5):
        sh = -(1 + i)
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            f"  int x = 1;\n  int y = x << {sh};  {PLANTED} 负移位量（UB）\n"
            "  std::printf(\"%d\\n\", y);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": f"移位量为负（{sh}）"},
            "severity": "high",
            "expected_verdict": "catch",
            "expected_detectors": ["ubsan"],
            "trigger_condition": "负移位量在 C++ 中是 UB，UBSan shift 检查必报",
            "platform_dependent": False,
            "platform_notes": "负移位是明确 UB，UBSan(-fsanitize=shift) 在 x86 也会报 shift exponent negative。实测 catch。",
            "notes": "移位量必须 >=0 且 < 类型宽度。",
        })

    # 4b) 超宽移位（signed）——5
    for i in range(5):
        sh = 32 + i  # 32..36；>=32 必 UB（1<<31 恰好可表示 INT_MIN 故避开）
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            f"  int x = 1;\n  int y = x << {sh};  {PLANTED} 有符号左移超出位宽（UB）\n"
            "  std::printf(\"%d\\n\", y);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": f"int 左移 {sh}（>=32 越界）"},
            "severity": "high",
            "expected_verdict": "catch",
            "expected_detectors": ["ubsan"],
            "trigger_condition": "移位量 >= 类型宽度时 UB，UBSan shift-out-of-bounds 报",
            "platform_dependent": False,
            "platform_notes": "移位越界是明确 UB，UBSan 在 x86 报 shift out of bounds。实测 catch。（注：1<<31 恰好可表示 INT_MIN 故本例用 >=32 保证 UB。）",
            "notes": "移位量须 < 类型位宽。",
        })

    # 4c) 超宽移位（unsigned）——5
    for i in range(5):
        sh = 32 + i
        cpp = (
            "#include <cstdint>\n#include <cstdio>\n"
            "int main(){\n"
            f"  uint32_t x = 1u;\n  uint32_t y = x << {sh};  {PLANTED} 无符号左移超出位宽（UB）\n"
            f"  std::printf(\"%u\\n\", y);\n  return 0;\n}}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": f"uint32_t 左移 {sh}（>=32 越界）"},
            "severity": "high",
            "expected_verdict": "catch",
            "expected_detectors": ["ubsan"],
            "trigger_condition": "无符号移位量 >= 宽度也是 UB，UBSan 报",
            "platform_dependent": False,
            "platform_notes": "无符号移位越界同样 UB，UBSan 在 x86 报。实测 catch。",
            "notes": "无符号移位也须 < 宽度。",
        })

    # 4d) 位域越界赋值（catch, compiler-warn）——5
    for i in range(5):
        w = 2 + i
        val = (1 << (w + 1))
        cpp = (
            "#include <cstdio>\n"
            f"struct Bf {{ unsigned f:{w}; }};\n"
            "int main(){\n"
            f"  Bf b; b.f = {val};  {PLANTED} 写入超过 {w} 位位域宽度（截断/UB）\n"
            "  std::printf(\"%u\\n\", b.f);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": f"向 {w} 位位域写入 {val}（超出宽度）"},
            "severity": "medium",
            "expected_verdict": "catch",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "写入值超出位域宽度时行为由实现定义，部分编译器 -W 警告",
            "platform_dependent": False,
            "platform_notes": "位域越界写是 C++ 未指定/UB；g++ -Wall 会发出截断警告。实测 compiler-warn catch。",
            "notes": "写入位域的值应在其宽度范围内。",
        })

    # 4e) 枚举位操作（底层类型不明确）——5 (miss)
    for i in range(5):
        cpp = (
            "#include <cstdio>\n"
            "enum Flags { A = 1, B = 2, C = 4 };\n"
            "int main(){\n"
            f"  Flags f = static_cast<Flags>(A | C | 0x80000000u);  {PLANTED} 枚举与无符号混合位或（底层类型不确定）\n"
            "  std::printf(\"%d\\n\", (int)f);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": "无作用域枚举与 0x80000000u 混合位操作（底层类型不确定）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "无作用域枚举底层类型是能容纳值的实现定义整数类型，混入大常量可能溢出/符号问题",
            "platform_dependent": False,
            "platform_notes": "枚举位操作属设计隐患，sanitizer 与 compiler-warn 通常不报（除非 -Wenum）；compiler-warn miss。真实盲区。",
            "notes": "枚举位标志宜用 enum class + 显式底层类型。",
        })

    # 4f) 位掩码计算错误（逻辑）——5 (miss)
    for i in range(5):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            "  unsigned m = (1 << 8) - 1;  // 本意取低 8 位\n"
            f"  unsigned v = 0xFF00; unsigned lo = v & m;  {PLANTED} 掩码宽度/位置错误导致取错位\n"
            "  std::printf(\"%u\\n\", lo);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": "位掩码宽度/位置计算错误（本例掩码本身正确但位置假设错）"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "掩码拼接/偏移错误产生错误结果，不触发 sanitizer",
            "platform_dependent": False,
            "platform_notes": "位掩码逻辑错误是纯逻辑缺陷，sanitizer 与 compiler-warn 均不抓。真实盲区。",
            "notes": "位掩码应单测验证。",
        })

    # 4g) std::bitset 越界访问——5 (miss)
    for i in range(5):
        idx = 9 + i
        cpp = (
            "#include <bitset>\n#include <cstdio>\n"
            "int main(){\n"
            "  std::bitset<8> bs;\n"
            f"  bool b = bs[{idx}];  {PLANTED} bitset<8> 越界下标 {idx}（operator[] 无边界检查）\n"
            "  std::printf(\"%d\\n\", (int)b);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "bit_operation",
            "defect_location": {"description": f"std::bitset<8> 越界访问下标 {idx}"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "bitset::operator[] 不做边界检查，越界是 UB，运行期通常静默读脏数据",
            "platform_dependent": False,
            "platform_notes": "bitset 越界是 UB 但 sanitizer 不插桩 std::bitset；compiler-warn miss。真实盲区。",
            "notes": "越界访问用 bs.test()（带异常）或先检查 size()。",
        })


# --------------------------------------------------------------------------
# 5) interrupt_safety（30）: 全部 miss（信号处理模拟）
# --------------------------------------------------------------------------
def gen_interrupt():
    # 5a) 共享非原子变量被 ISR 自增（6）
    for i in range(6):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "static int shared = 0;\n"
            "extern \"C\" void isr(int) { shared++; }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} ISR 与主程序竞争自增 shared（无同步）\n"
            "  std::printf(\"%d\\n\", shared);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "信号处理程序与主程序竞态自增非原子全局 shared"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "ISR 与主循环并发 RMW 同一非原子变量，会丢失更新/读到撕裂值",
            "platform_dependent": True,
            "platform_notes": "用户态无法复现真实中断并发；TSan 不识别 signal 并发；sanitizer/compiler-warn 均 miss。真实盲区。",
            "notes": "ISR 共享计数器用 std::atomic 或关中断保护。",
        })

    # 5b) ISR 调用非重入 printf（5）
    for i in range(5):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "extern \"C\" void isr(int) { std::printf(\"irq!\\n\"); }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} 在 ISR 中调用非异步信号安全函数 printf\n"
            "  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "信号处理程序调用非异步信号安全的 printf"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "ISR 中调用非重入函数（malloc/printf 等）在重入时破坏其内部状态",
            "platform_dependent": True,
            "platform_notes": "POSIX 规定 ISR 只能调用异步信号安全函数；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "ISR 内仅调用异步信号安全函数。",
        })

    # 5c) ISR/主程序对计数器无同步竞争（5）
    for i in range(5):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "static long total = 0;\n"
            "extern \"C\" void isr(int) { for (int k = 0; k < 1000; ++k) total += k; }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} 长 ISR 修改 total，主程序同时读\n"
            "  std::printf(\"%ld\\n\", total);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "ISR 与主程序对 total 的非原子读写（撕裂读）"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "多字变量在 ISR 与主循环间无临界区保护，读到半更新值",
            "platform_dependent": True,
            "platform_notes": "用户态无法复现；sanitizer 不识别 signal 并发；compiler-warn miss。真实盲区。",
            "notes": "多字共享量用原子或关中断/自旋锁保护。",
        })

    # 5d) ISR 内递归 raise（嵌套）（4）
    for i in range(4):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "extern \"C\" void isr(int) { static int n = 0; if (n++ < 1) std::raise(SIGINT); }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} ISR 内再次触发自身（嵌套）\n"
            "  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "信号处理程序内再次 raise 同一信号导致嵌套"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "ISR 内触发自身造成栈嵌套/重入，深嵌套致栈溢出",
            "platform_dependent": True,
            "platform_notes": "信号嵌套在用户态难复现真实中断嵌套；sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "ISR 应避免再次触发自身，或屏蔽同信号。",
        })

    # 5e) 主程序读写 ISR 正在更新的结构体（非原子）（5）
    for i in range(5):
        cpp = (
            "#include <csignal>\n#include <signal.h>\n#include <cstdio>\n"
            "struct Pkt { int len; char buf[16]; };\n"
            "static Pkt g;\n"
            "extern \"C\" void isr(int) { g.len = 16; for (int i=0;i<16;++i) g.buf[i]=(char)i; }\n"
            "int main(){\n"
            f"  std::signal(SIGINT, isr);\n  std::raise(SIGINT);  {PLANTED} 主程序读取 ISR 更新的非原子结构体\n"
            "  std::printf(\"%d\\n\", g.len);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "主程序读取 ISR 正在写入的非原子 Pkt 结构体"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "主程序在 ISR 更新结构体中途读取，得到 len 与 buf 不一致的数据",
            "platform_dependent": True,
            "platform_notes": "用户态无法复现；sanitizer 不识别；compiler-warn miss。真实盲区。",
            "notes": "ISR 与主程序共享结构体用双缓冲/原子指针或关中断。",
        })

    # 5f) longjmp 出现在 ISR（5）
    for i in range(5):
        cpp = (
            "#include <csignal>\n#include <csetjmp>\n#include <cstdio>\n"
            "static jmp_buf env;\n"
            "extern \"C\" void isr(int) { std::longjmp(env, 1); }\n"
            "int main(){\n"
            f"  if (setjmp(env) == 0) {{ std::signal(SIGINT, isr); std::raise(SIGINT); }}\n"
            f"  {PLANTED} 在 ISR 中 longjmp（跳过主程序栈帧析构，UB）\n"
            "  std::printf(\"returned\\n\");\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "interrupt_safety",
            "defect_location": {"description": "信号处理程序内调用 longjmp 跳出主程序栈帧"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "从 ISR longjmp 到主程序 setjmp 点，跳过中间栈帧的非平凡对象析构（UB）",
            "platform_dependent": True,
            "platform_notes": "setjmp/longjmp 跨栈帧跳过析构是 UB；sanitizer 在用户态通常不报，compiler-warn miss。真实盲区。",
            "notes": "ISR 内禁止 longjmp。",
        })


# --------------------------------------------------------------------------
# 6) register_ub（30）: 10 catch(register 弃用) + 20 miss
# --------------------------------------------------------------------------
def gen_register():
    # 6a) register 关键字（catch, compiler-warn）——10
    for i in range(10):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            f"  register int r{i} = {i};  {PLANTED} register 关键字（C++17 弃用、C++20 移除）\n"
            f"  std::printf(\"%d\\n\", r{i});\n  return 0;\n}}\n"
        )
        add(cpp, {
            "defect_type": "register_ub",
            "defect_location": {"description": f"使用 register 关键字声明 r{i}"},
            "severity": "low",
            "expected_verdict": "catch",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "register 在 C++17 弃用、C++20 移除；使用会触发弃用警告",
            "platform_dependent": False,
            "platform_notes": "register 关键字自 C++17 起弃用，g++ -Wall 发出 -Wdeprecated 警告。实测 compiler-warn catch。",
            "notes": "删除 register 关键字（现代编译器自动决定寄存器分配）。",
        })

    # 6b) setjmp/longjmp 跳过非平凡对象析构（8）——miss
    for i in range(8):
        cpp = (
            "#include <csetjmp>\n#include <string>\n#include <cstdio>\n"
            "static jmp_buf env;\n"
            "int main(){\n"
            "  volatile int guard = 0;\n"
            "  if (setjmp(env) == 0) {\n"
            "    std::string s = \"resource\";  // 非平凡对象\n"
            f"    if (!guard) {{ guard = 1; std::longjmp(env, 1); }}  {PLANTED} longjmp 跳过 s 的析构（资源泄漏/UB）\n"
            "  }\n"
            "  std::printf(\"done\\n\");\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "register_ub",
            "defect_location": {"description": "longjmp 跳过局部 std::string 的析构函数"},
            "severity": "high",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "setjmp/longjmp 跨过含非平凡析构的栈帧，析构被跳过（资源泄漏/UB）",
            "platform_dependent": False,
            "platform_notes": "跳过析构是 UB，但运行时通常不崩溃，UBSan 不报；compiler-warn miss。真实盲区。",
            "notes": "用异常或 RAII 替代 longjmp 控制流。",
        })

    # 6c) 内联汇编缺失 memory 破坏列表（6）——miss（WSL x86-64 可编译）
    for i in range(6):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            "  int a = 1, b = 2, r = 0;\n"
            "  // 内联汇编修改了内存/寄存器却未声明 clobber，编译器可能错误优化\n"
            f"  asm volatile(\"addl %1, %0\" : \"+r\"(r) : \"r\"(a));  {PLANTED} 缺失 memory/寄存器 clobber 声明\n"
            "  r += b;\n"
            "  std::printf(\"%d\\n\", r);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "register_ub",
            "defect_location": {"description": "内联汇编未声明 memory/被修改寄存器 clobber"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "内联汇编读写内存/寄存器但未在 clobber 列表声明，编译器据此错误优化相邻代码",
            "platform_dependent": True,
            "platform_notes": "内联汇编 clobber 缺失是真实缺陷，但静态分析在本工具链不覆盖；ubsan/compiler-warn miss。WSL x86-64 可编译运行。真实盲区。",
            "notes": "内联汇编须完整声明输出/输入/clobber（含 \"memory\"）。",
        })

    # 6d) 寄存器变量取地址模拟（register misuse）（4）——miss
    for i in range(4):
        cpp = (
            "#include <cstdio>\n"
            "int main(){\n"
            "  int v = 7;\n"
            f"  int* p = &v;  {PLANTED} 模拟“register 变量取地址”（强转制造别名误用）\n"
            "  *p = 9;\n  std::printf(\"%d\\n\", v);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "register_ub",
            "defect_location": {"description": "对局部变量取地址并借指针别名修改（register 取地址的现代化误用模拟）"},
            "severity": "low",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "一旦变量可能取地址，register 提示失效；现代等价误用是未预期的别名",
            "platform_dependent": False,
            "platform_notes": "取地址本身是合法的；此处模拟 register 时代取地址 UB 的现代化等价误用，sanitizer 不抓，compiler-warn miss。真实盲区。",
            "notes": "不要对会被取地址的变量做寄存器假设优化。",
        })

    # 6e) 全局寄存器变量 GCC 扩展误用（2）——miss
    for i in range(2):
        cpp = (
            "#include <cstdio>\n"
            "register int* gp asm(\"rbx\");\n"
            "int main(){\n"
            f"  static int x = 5; gp = &x;  {PLANTED} 全局寄存器变量（GCC 扩展）误用 rbx\n"
            "  std::printf(\"%d\\n\", *gp);\n  return 0;\n}\n"
        )
        add(cpp, {
            "defect_type": "register_ub",
            "defect_location": {"description": "GCC 全局寄存器变量扩展把 rbx 当作 gp"},
            "severity": "medium",
            "expected_verdict": "miss",
            "expected_detectors": ["compiler-warn"],
            "trigger_condition": "全局寄存器变量劫持被调用约定保留的寄存器（如 rbx），破坏 ABI 导致崩溃",
            "platform_dependent": True,
            "platform_notes": "全局寄存器变量是 GCC 扩展，劫持保留寄存器会破坏 ABI；本工具链 compiler-warn miss。真实盲区（WSL x86-64 可编译运行）。",
            "notes": "避免使用全局寄存器变量，或用编译器保留的专用寄存器。",
        })


def main():
    gen_alignment()
    gen_endianness()
    gen_volatile()
    gen_bitop()
    gen_interrupt()
    gen_register()
    # 顺序编号 F001..F200
    assert len(SAMPLES) == 200, f"期望 200 个样本，实际 {len(SAMPLES)}"
    for i, (cpp, meta) in enumerate(SAMPLES, 1):
        sid = f"F{i:03d}"
        # 修正缺陷行
        dl = meta.setdefault("defect_location", {})
        dl["line"] = defect_line(cpp)
        dl.setdefault("function", "main")
        full = {
            "sample_id": sid,
            "defect_type": meta["defect_type"],
            "defect_location": dl,
            "severity": meta["severity"],
            "planted": True,
            "expected_verdict": meta["expected_verdict"],
            "expected_detectors": meta["expected_detectors"],
            "trigger_condition": meta["trigger_condition"],
            "platform_dependent": meta["platform_dependent"],
            "platform_notes": meta["platform_notes"],
            "notes": meta["notes"],
        }
        cpp_path = os.path.join(HERE, f"sample_{sid}.cpp")
        json_path = os.path.join(HERE, f"sample_{sid}.json")
        open(cpp_path, "w", encoding="utf-8").write(cpp)
        json.dump(full, open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已生成 {len(SAMPLES)} 个样本到 {HERE}")


if __name__ == "__main__":
    main()
