#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# 676c-D: 扩样数据生成——C++ 标准库缺陷（迭代器/容器/字符串/算法/智能指针/lambda 捕获）
# 生成 200 个候选样本（sample_D001..D200.cpp + .json）到本目录。
# 每个样本都是可独立编译运行的真实植入缺陷；缺陷行带 // <<PLANTED-DEFECT>> 标记。
# 初始 expected_verdict 为基于推理的猜测，任务C验证阶段会用真实 detect() 结果覆盖。
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- 标记行约定：缺陷所在行包含 <<PLANTED-DEFECT>> ----
MARK = "// <<PLANTED-DEFECT>>"

def wrap(code_lines):
    """包成完整可编译的 cpp 源码（含头部与 main 框架的由模板自行给出）。"""
    return "\n".join(code_lines) + "\n"

# 每个生成函数返回 list[dict]，dict 字段：
#   defect_type, code(list[str]), func, desc, sev,
#   exp_verdict, exp_detectors(list), trigger, notes
# 缺陷行需含 MARK。

# ============================ 1. iterator_invalidation ============================
def gen_iterator(n=35):
    out = []
    # T1: vector push_back 触发重新分配 -> it 失效 (catch, asan)
    for i in range(1, 8):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3};",
            "  auto it = v.begin();",
            f"  for (int k = 0; k < {i}; ++k) v.push_back(k);",
            "  *it = 42; " + MARK + " 使用重新分配后失效的迭代器",
            "  std::printf(\"%d\\n\", *it);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="vector push_back 重新分配后使用失效迭代器", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="push_back 触发 realloc，it 指向已释放/搬迁的旧缓冲区，asan 报 heap-use-after-free。"))
    # T2: vector insert 头部 -> 之后迭代器失效 (catch)
    for i in range(1, 6):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v(5, 1);",
            "  auto it = v.begin() + 3;",
            f"  v.insert(v.begin(), {i});",
            "  *it = 9; " + MARK + " insert 后使用失效迭代器",
            "  std::printf(\"%d\\n\", *it);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="vector insert 后使用失效迭代器", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="insert 使插入点之后的迭代器失效，写入越界/悬垂，asan 报 heap-buffer-overflow/use-after-free。"))
    # T3: vector erase 后使用失效迭代器(无 realloc, 逻辑失效) -> miss
    for i in range(1, 6):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {10, 20, 30, 40};",
            f"  auto it = v.begin() + {i};",
            "  v.erase(v.begin());",
            "  std::printf(\"%d\\n\", *it); " + MARK + " erase 后使用失效迭代器(无 realloc)",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="vector erase 后使用失效迭代器（逻辑缺陷，无 realloc）", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="erase 使插入点之后迭代器失效但不一定 realloc，内存仍分配，asan 通常检测不到——检测器盲区。"))
    # T4: deque push_front 使迭代器失效 (catch)
    for i in range(1, 4):
        code = [
            "#include <deque>",
            "#include <cstdio>",
            "int main() {",
            "  std::deque<int> d = {1, 2, 3};",
            "  auto it = d.begin() + 1;",
            f"  for (int k = 0; k < {i}; ++k) d.push_front(0);",
            "  std::printf(\"%d\\n\", *it); " + MARK + " deque push_front 后使用失效迭代器",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="deque push_front 后使用失效迭代器", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="deque 在两端增删会使全部迭代器失效，访问悬垂，asan 报 heap-use-after-free/invalid。"))
    # T5: unordered_map insert rehash 使迭代器失效 (catch)
    for i in range(1, 4):
        code = [
            "#include <unordered_map>",
            "#include <cstdio>",
            "int main() {",
            "  std::unordered_map<int, int> m;",
            "  m[1] = 10;",
            "  auto it = m.find(1);",
            f"  for (int k = 2; k < 2 + {i} * 50; ++k) m[k] = k;",
            "  std::printf(\"%d\\n\", it->second); " + MARK + " rehash 后使用失效迭代器",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="unordered_map rehash 后使用失效迭代器", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="insert 触发 rehash，旧迭代器悬垂，asan 报 heap-use-after-free。"))
    # T6: map erase 被擦迭代器后使用 (catch/miss)
    for i in range(1, 4):
        code = [
            "#include <map>",
            "#include <cstdio>",
            "int main() {",
            "  std::map<int, int> m;",
            "  m[1] = 10; m[2] = 20; m[3] = 30;",
            "  auto it = m.find(2);",
            "  m.erase(it);",
            f"  std::printf(\"%d\\n\", it->second); " + MARK + f" 使用已被 erase 的迭代器({i})",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="map erase 后使用被擦除的迭代器", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="map 节点被删除后，迭代器悬垂，解引用为 use-after-free，asan 可能捕获。"))
    # T7: range-for 循环内修改容器 (catch)
    for i in range(1, 4):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3};",
            f"  for (int x : v) {{ (void)x; v.push_back({i}); }} " + MARK + " range-for 内 push_back 使迭代器失效",
            "  std::printf(\"%zu\\n\", v.size());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="range-for 循环内修改容器触发迭代器失效", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="range-for 隐式使用迭代器，循环内 push_back 致 realloc，后续迭代 UB，asan 报 heap-use-after-free/infinite-loop。"))
    # T8: 保存 end() 后插入，比较失效 end() (miss)
    for i in range(1, 4):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3};",
            "  auto e = v.end();",
            f"  v.insert(v.begin(), {i});",
            "  std::printf(\"%d\\n\", (int)(v.end() == e)); " + MARK + " 比较失效的 end() 迭代器",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="容器修改后使用失效的 end() 迭代器", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="保存的 end() 在插入后失效，比较结果是未定义行为但通常不崩溃，asan 检测不到——盲区。"))
    # T9: 类成员 vector 迭代器失效（复杂/嵌套）
    code = [
        "#include <vector>",
        "#include <cstdio>",
        "struct Holder {",
        "  std::vector<int> v = {1, 2, 3};",
        "  int read_bad() {",
        "    auto it = v.begin();",
        "    v.push_back(4);",
        "    return *it; " + MARK + " 成员函数内 push_back 后使用失效迭代器",
        "  }",
        "};",
        "int main() {",
        "  Holder h;",
        "  std::printf(\"%d\\n\", h.read_bad());",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="iterator_invalidation", code=code, func="Holder::read_bad",
                    desc="类成员 vector 在成员函数内 push_back 后使用失效迭代器", sev="high",
                    exp_verdict="catch", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="类成员容器修改导致成员函数内迭代器失效，asan 报 heap-use-after-free。"))
    # 补足到 n
    while len(out) < n:
        i = len(out) % 5 + 1
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3, 4, 5};",
            f"  auto it = v.begin() + {i};",
            "  v.erase(v.begin());",
            "  std::printf(\"%d\\n\", *it); " + MARK + " erase 后使用失效迭代器(补充变体)",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="iterator_invalidation", code=code, func="main",
                        desc="vector erase 后使用失效迭代器（补充变体）", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="无 realloc 的逻辑失效，asan 盲区。"))
    return out[:n]

# ============================ 2. stl_container_ub ============================
def gen_container(n=35):
    out = []
    # T1: 空容器 front() (miss, 真实盲区)
    for i in range(1, 7):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v;" + ("" if i % 2 else "  // 空容器"),
            "  if (v.empty()) { int x = v.front(); " + MARK + " 空容器调用 front()",
            "    std::printf(\"%d\\n\", x); }",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="空 vector 调用 front()", sev="high",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="空容器 front() 是 UB，但 asan/ubsan 通常不报（读未初始化/越界不一定触发），属于检测器盲区。"))
    # T2: operator[] 越界 (catch, asan)
    for i in range(1, 7):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3};",
            f"  int x = v[{3 + i}]; " + MARK + " operator[] 越界访问",
            "  std::printf(\"%d\\n\", x);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="vector operator[] 越界访问", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="operator[] 不做边界检查，越界访问堆内存，asan 报 heap-buffer-overflow。"))
    # T3: std::array 越界 (catch/miss 取决于实现)
    for i in range(1, 5):
        code = [
            "#include <array>",
            "#include <cstdio>",
            "int main() {",
            "  std::array<int, 3> a = {1, 2, 3};",
            f"  int x = a[{3 + i}]; " + MARK + " std::array 越界访问",
            "  std::printf(\"%d\\n\", x);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="std::array operator[] 越界访问", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="std::array 越界访问栈上内存，asan 报 stack-buffer-overflow。"))
    # T4: vector<bool> 代理引用在必然重分配后悬垂
    for i in range(1, 4):
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<bool> vb(3, false);",
            "  auto bit = vb[1];  // 代理对象持有指向位字的指针",
            f"  for (int k = 0; k < {64 + i * 8}; ++k) vb.push_back(true);  // 位数超过一机器字，必然重分配",
            "  bool b = bit; " + MARK + " vector<bool> 代理引用在重分配后悬垂",
            "  std::printf(\"%d\\n\", (int)b);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="vector<bool> 代理引用在重分配后悬垂", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="vector<bool> 的 operator[] 返回代理对象，持有指向位字的指针；位数超过一机器字后 push_back 必然重分配，代理悬垂，读取为 use-after-free。"))
    # T5: 从空 optional 取值 (miss, UB)
    for i in range(1, 5):
        code = [
            "#include <optional>",
            "#include <cstdio>",
            "int main() {",
            "  std::optional<int> o;" + ("" if i % 2 else "  // 未赋值"),
            "  int x = *o; " + MARK + " 从空 optional 解引用",
            "  std::printf(\"%d\\n\", x);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="从空 std::optional 解引用取值", sev="high",
                        exp_verdict="miss", exp_detectors=["asan", "ubsan"],
                        trigger="直接运行即触发",
                        notes="对空 optional 解引用是 UB，但 sanitizer 一般无专门检查，编译器警告也通常没有——检测器盲区。"))
    # T6: 从空 variant 取 wrong alternative (miss)
    for i in range(1, 4):
        code = [
            "#include <variant>",
            "#include <cstdio>",
            "int main() {",
            "  std::variant<int, double> v = 3;",
            "  double d = std::get<double>(v); " + MARK + " 从持有 int 的 variant 取 double",
            "  std::printf(\"%f\\n\", d);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="std::variant 取错误 alternative（抛异常）", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="std::get 错误类型抛 bad_variant_access，属异常而非 sanitizer 可检——盲区。"))
    # T7: list splice 后迭代器归属错误 (miss/逻辑)
    code = [
        "#include <list>",
        "#include <cstdio>",
        "int main() {",
        "  std::list<int> a = {1, 2, 3};",
        "  auto it = a.begin();",
        "  a.erase(a.begin());  // 节点被删除，it 悬垂",
        "  std::printf(\"%d\\n\", *it); " + MARK + " list erase 后使用已删除节点的迭代器",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                    desc="std::list erase 后使用已删除节点的迭代器", sev="high",
                    exp_verdict="catch", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="erase 释放节点内存，it 悬垂，解引用为 heap-use-after-free，asan 捕获。"))
    # T8: deque 越界 operator[] (catch)
    code = [
        "#include <deque>",
        "#include <cstdio>",
        "int main() {",
        "  std::deque<int> d = {1, 2, 3};",
        "  int x = d[10]; " + MARK + " deque operator[] 越界",
        "  std::printf(\"%d\\n\", x);",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                    desc="std::deque operator[] 越界访问", sev="high",
                    exp_verdict="catch", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="deque 越界访问，asan 报 heap/container-buffer-overflow。"))
    # 补足到 n
    while len(out) < n:
        code = [
            "#include <vector>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v;",
            "  int x = v.back(); " + MARK + " 空容器调用 back()",
            "  std::printf(\"%d\\n\", x);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="stl_container_ub", code=code, func="main",
                        desc="空 vector 调用 back()（补充）", sev="high",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="空容器 back() 是 UB，asan/ubsan 盲区。"))
    return out[:n]

# ============================ 3. string_ub ============================
def gen_string(n=35):
    out = []
    # T1: c_str() 失效（长串强制 realloc -> catch）
    for i in range(1, 8):
        init = '"' + ("a" * (24 + i * 3)) + '"'
        code = [
            "#include <string>",
            "#include <cstdio>",
            "int main() {",
            f"  std::string s = {init};",
            "  const char* p = s.c_str();",
            "  s += \" world\";",
            "  std::printf(\"%s\\n\", p); " + MARK + " 修改后使用失效的 c_str() 指针",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="std::string 修改后使用失效的 c_str() 指针", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="初始串超 SSO，+= 触发 realloc，p 悬垂，asan 报 heap-use-after-free。"))
    # T2: 通过 data() 指针越界写（真实 OOB）-> catch
    for i in range(1, 4):
        code = [
            "#include <string>",
            "#include <cstdio>",
            "int main() {",
            "  std::string s(200, 'a');  // 堆分配",
            "  char* p = s.data();",
            f"  p[{300 + i * 40}] = 'X'; " + MARK + " 通过 data() 指针越界写（超出缓冲）",
            "  std::printf(\"%zu\\n\", s.size());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="通过 data() 指针越界写 std::string 堆缓冲", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="data() 仅保证 [data(), data()+size()) 可写；越过 size 写入为越界，asan 报 heap-buffer-overflow。"))
    # T3: string_view 悬垂（临时 string）-> catch
    for i in range(1, 6):
        code = [
            "#include <string>",
            "#include <string_view>",
            "#include <cstdio>",
            "int main() {",
            "  std::string_view sv = std::string(\"temp" + str(i) + "\");",
            "  std::printf(\"%.*s\\n\", (int)sv.size(), sv.data()); " + MARK + " 使用悬垂的 string_view（临时串已析构）",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="从临时 std::string 构造的 string_view 悬垂", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="临时 string 在语句结束析构，sv 悬垂，访问触发 use-after-scope/heap，asan 捕获。"))
    # T4: substr 越界（抛异常）-> miss
    for i in range(1, 5):
        code = [
            "#include <string>",
            "#include <cstdio>",
            "int main() {",
            "  std::string s = \"abc\";",
            f"  std::string t = s.substr(5, {i}); " + MARK + " substr(pos>size) 抛 out_of_range",
            "  std::printf(\"%s\\n\", t.c_str());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="std::string::substr 越界（抛异常）", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="substr(pos>size) 抛 out_of_range（良定义异常），sanitizer 不报——盲区。"))
    # T5: 字符串字面量修改（const char* 转 char*）-> miss/catch
    for i in range(1, 4):
        code = [
            "#include <cstdio>",
            "int main() {",
            "  char* p = (char*)\"hello\";",
            f"  p[{i}] = 'X'; " + MARK + " 修改字符串字面量（只读段）",
            "  std::printf(\"%s\\n\", p);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="修改字符串字面量（const 转非 const）", sev="high",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="写只读段是 UB，是否崩溃取决于段保护，asan 通常报 SEGV/公交车——多为盲区（可能直接段错误而非 sanitizer 报告）。"))
    # T6: string_view 指向已析构的局部 string（复杂）
    code = [
        "#include <string>",
        "#include <string_view>",
        "#include <cstdio>",
        "std::string_view leak() {",
        "  std::string s = \"local content\";",
        "  return std::string_view(s); " + MARK + " 返回指向局部 string 的 string_view",
        "}",
        "int main() {",
        "  auto sv = leak();",
        "  std::printf(\"%.*s\\n\", (int)sv.size(), sv.data());",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="string_ub", code=code, func="leak",
                    desc="函数返回指向局部 string 的 string_view（悬垂）", sev="high",
                    exp_verdict="catch", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="局部 string 析构后 string_view 悬垂，访问触发 use-after-scope，asan 捕获。"))
    # 补足到 n
    while len(out) < n:
        k = len(out)
        base = 40 + (k % 5) * 4
        code = [
            "#include <string>",
            "#include <string_view>",
            "#include <cstdio>",
            "int main() {",
            f"  std::string s = \"" + ("z" * base) + "\";",
            "  std::string_view sv(s.data(), s.size());",
            f"  s.append(\"" + ("w" * 100) + "\");  // 必然触发 realloc，旧缓冲被释放",
            "  unsigned long sum = 0;",
            "  for (char ch : sv) sum += (unsigned char)ch; " + MARK + " 遍历悬垂的 string_view（读取已释放缓冲）",
            "  std::printf(\"%lu\\n\", sum);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="string_ub", code=code, func="main",
                        desc="原 string 扩容后遍历悬垂的 string_view（读取已释放缓冲）", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="长串字面量构造时 capacity==size，append 后必然 realloc，sv 指向已释放缓冲；在插桩代码中遍历读取，asan 报 heap-use-after-free。"))
    return out[:n]

# ============================ 4. algorithm_misuse ============================
def gen_algorithm(n=35):
    out = []
    # T1: sort 比较器非严格弱序（始终返回 true）-> miss/崩溃
    for i in range(1, 6):
        code = [
            "#include <vector>",
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};",
            "  std::sort(v.begin(), v.end(), [](int a, int b) { return (a % 2) < (b % 2); }); " + MARK + f" 比较器违反严格弱序(非传递,{i})",
            "  std::printf(\"%d\\n\", (int)v.size());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::sort 比较器违反严格弱序（非传递）", sev="high",
                        exp_verdict="miss", exp_detectors=["asan", "ubsan"],
                        trigger="直接运行即触发",
                        notes="比较器 (a%2)<(b%2) 破坏传递性（偶<奇、奇<偶，但非偶<偶），不满足严格弱序，sort 行为未定义；实测可终止但结果无序，sanitizer 不报——盲区。"))
    # T2: remove 不 erase (逻辑错误) -> miss
    for i in range(1, 7):
        code = [
            "#include <vector>",
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3, 2, 1};",
            "  std::remove(v.begin(), v.end(), 2); " + MARK + f" 忘记 erase（remove-erase 惯用法缺失,{i}）",
            "  std::printf(\"%zu\\n\", v.size());  // 仍为 5，含残留元素",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::remove 后未调用 erase", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="remove 只移动元素不删除，size 不变，属逻辑错误，sanitizer 不报——盲区。"))
    # T3: copy 源与目标重叠 (catch/miss)
    for i in range(1, 6):
        code = [
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  int a[6] = {1, 2, 3, 4, 5, 6};",
            f"  std::copy(a, a + 3, a + {i}); " + MARK + " 源与目标区间重叠",
            "  std::printf(\"%d\\n\", a[5]);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::copy 源与目标区间重叠（UB）", sev="high",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="重叠 copy 是 UB，行为依实现；asan 通常无重叠检测——盲区（部分实现可用 memmove 掩盖）。"))
    # T4: transform 目标区间不足 (catch, asan)
    for i in range(1, 6):
        code = [
            "#include <vector>",
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> in(5, 1);",
            f"  std::vector<int> out({i});",
            "  std::transform(in.begin(), in.end(), out.begin(), [](int x){ return x + 1; }); " + MARK + " 目标区间过小，越界写入",
            "  std::printf(\"%zu\\n\", out.size());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::transform 目标区间容量不足（越界写入）", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="out 容量小于 in，写入越界堆内存，asan 报 heap-buffer-overflow。"))
    # T5: accumulate 初始值类型错误（精度/截断）-> miss
    for i in range(1, 5):
        code = [
            "#include <vector>",
            "#include <numeric>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<double> v = {0.1, 0.2, 0.3};",
            f"  int sum = std::accumulate(v.begin(), v.end(), 0); " + MARK + f" 以 int 为初始值累加 double（截断,{i}）",
            "  std::printf(\"%d\\n\", sum);  // 应为 0 而非 0.6",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::accumulate 初始值类型错误导致截断", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="以 int 0 为初值使 double 累加被截断，是逻辑错误，sanitizer 不报——盲区。"))
    # T6: lower_bound 用于未排序区间 (miss/逻辑)
    for i in range(1, 4):
        code = [
            "#include <vector>",
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {5, 3, 1, 4, 2};",  # 未排序
            f"  auto it = std::lower_bound(v.begin(), v.end(), 3); " + MARK + f" 在未排序区间使用 lower_bound({i})",
            "  std::printf(\"%d\\n\", (int)(it - v.begin()));",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::lower_bound 用于未排序区间", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="lower_bound 要求有序，未排序时结果无意义，属逻辑错误——盲区。"))
    # T7: unique 不 erase (miss)
    code = [
        "#include <vector>",
        "#include <algorithm>",
        "#include <cstdio>",
        "int main() {",
        "  std::vector<int> v = {1, 1, 2, 2, 3, 3};",
        "  std::unique(v.begin(), v.end()); " + MARK + " unique 后未 erase",
        "  std::printf(\"%zu\\n\", v.size());",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                    desc="std::unique 后未调用 erase", sev="medium",
                    exp_verdict="miss", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="unique 只把重复元素移到尾部，size 不变，逻辑错误——盲区。"))
    # T8: merge 输入未排序 (miss)
    code = [
        "#include <vector>",
        "#include <algorithm>",
        "#include <cstdio>",
        "int main() {",
        "  std::vector<int> a = {3, 1, 2}, b = {6, 4, 5}, out(6);",
        "  std::merge(a.begin(), a.end(), b.begin(), b.end(), out.begin()); " + MARK + " merge 输入区间未排序",
        "  std::printf(\"%zu\\n\", out.size());",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                    desc="std::merge 输入区间未排序", sev="medium",
                    exp_verdict="miss", exp_detectors=["asan"],
                    trigger="直接运行即触发",
                    notes="merge 要求两区间有序，未排序结果错误，逻辑错误——盲区。"))
    # 补足到 n
    while len(out) < n:
        code = [
            "#include <vector>",
            "#include <algorithm>",
            "#include <cstdio>",
            "int main() {",
            "  std::vector<int> v = {1, 2, 3, 2, 1};",
            "  std::remove_if(v.begin(), v.end(), [](int x){ return x == 2; }); " + MARK + " remove_if 后未 erase（补充）",
            "  std::printf(\"%zu\\n\", v.size());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="algorithm_misuse", code=code, func="main",
                        desc="std::remove_if 后未 erase（补充）", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="逻辑错误，sanitizer 盲区。"))
    return out[:n]

# ============================ 5. smart_pointer ============================
def gen_smart(n=30):
    out = []
    # T1: unique_ptr 管理数组却用默认 delete (catch, asan mismatch)
    for i in range(1, 7):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "int main() {",
            f"  std::unique_ptr<int> p(new int[{i + 1}]); " + MARK + " 用默认 delete 管理数组（应为 delete[]）",
            f"  int* raw = p.get(); raw[0] = 1;",
            "  std::printf(\"%d\\n\", raw[0]);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="unique_ptr 用默认 delete 管理 new[] 数组", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="析构时触发",
                        notes="数组需用 delete[]，默认 delete 导致 mismatched-free，asan 报 new-delete-type-mismatch。"))
    # T2: 从同一裸指针构造多个 shared_ptr (catch, 双重释放)
    for i in range(1, 5):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "int main() {",
            "  int* raw = new int(42);",
            f"  std::shared_ptr<int> a(raw);",
            f"  std::shared_ptr<int> b(raw); " + MARK + f" 两个独立 shared_ptr 指向同一裸指针({i})",
            "  std::printf(\"%d %d\\n\", *a, *b);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="从同一裸指针构造多个独立 shared_ptr（双重释放）", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="析构时触发",
                        notes="a、b 各自持有控制块，析构时两次 delete 同一指针，asan 报 double-free。"))
    # T3: get() 后手动 delete (catch, 双重释放)
    for i in range(1, 4):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "int main() {",
            "  auto p = std::make_shared<int>(7);",
            f"  int* raw = p.get();",
            f"  delete raw; " + MARK + f" 手动 delete 智能指针管理的裸指针({i})",
            "  std::printf(\"%d\\n\", *p);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="对 shared_ptr::get() 返回指针手动 delete", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="析构时触发",
                        notes="shared_ptr 仍管理该指针，手动 delete 后析构再 delete，asan 报 double-free。"))
    # T4: 循环引用 (miss, 内存泄漏 asan 默认不报)
    for i in range(1, 5):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "struct Node {",
            "  std::shared_ptr<Node> next;",
            "};",
            "int main() {",
            "  auto a = std::make_shared<Node>();",
            "  auto b = std::make_shared<Node>();",
            f"  a->next = b; b->next = a; " + MARK + f" shared_ptr 循环引用导致泄漏({i})",
            "  std::printf(\"leak\\n\");",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="std::shared_ptr 循环引用导致内存泄漏", sev="medium",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="析构后泄漏",
                        notes="循环引用使引用计数不归零，对象永不释放；asan 默认不报告泄漏（需 detect_leaks=1）——检测器盲区。"))
    # T5: shared_from_this 在构造函数中调用 (miss, UB)
    for i in range(1, 4):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "struct Bad : std::enable_shared_from_this<Bad> {",
            "  Bad() {",
            f"    auto self = shared_from_this(); " + MARK + f" 构造函数中调用 shared_from_this（对象尚未被 shared_ptr 管理,{i}）",
            "    (void)self;",
            "  }",
            "};",
            "int main() {",
            "  auto p = std::make_shared<Bad>();",
            "  std::printf(\"ok\\n\");",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="Bad::Bad",
                        desc="在构造函数中调用 shared_from_this", sev="high",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="构造时触发",
                        notes="构造期间对象尚未被任何 shared_ptr 拥有，shared_from_this 抛 bad_weak_ptr（异常）或 UB——sanitizer 盲区。"))
    # T6: weak_ptr 未检查 expired 就 lock 后解引用 (catch/miss)
    for i in range(1, 4):
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "int main() {",
            "  auto sp = std::make_shared<int>(5);",
            "  std::weak_ptr<int> wp(sp);",
            "  sp.reset();",
            f"  auto lp = wp.lock();",
            f"  std::printf(\"%d\\n\", *lp); " + MARK + f" 未检查 expired 直接解引用 lock() 结果({i})",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="weak_ptr 未检查 expired 直接解引用 lock() 结果", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="运行时空指针解引用",
                        notes="lock() 返回空指针，解引用为空指针解引用，asan 报 SEGV/nullptr-deref。")) 
    # T7: release() 后丢失裸指针导致泄漏 (miss)
    code = [
        "#include <memory>",
        "#include <cstdio>",
        "int main() {",
        "  auto p = std::make_unique<int>(9);",
        "  p.release(); " + MARK + " release() 后未接管返回裸指针，内存泄漏",
        "  std::printf(\"leaked\\n\");",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="smart_pointer", code=code, func="main",
                    desc="unique_ptr::release() 后未接管裸指针", sev="low",
                    exp_verdict="miss", exp_detectors=["asan"],
                    trigger="析构后泄漏",
                    notes="release() 放弃所有权但不释放，返回的裸指针未被接管即泄漏；asan 默认不报泄漏——盲区。"))
    # 补足到 n
    while len(out) < n:
        code = [
            "#include <memory>",
            "#include <cstdio>",
            "int main() {",
            "  int* raw = new int(1);",
            f"  std::shared_ptr<int> a(raw);",
            f"  std::shared_ptr<int> b(raw); " + MARK + " 多 shared_ptr 共享裸指针（补充）",
            "  std::printf(\"%d\\n\", *a);",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="smart_pointer", code=code, func="main",
                        desc="多 shared_ptr 共享同一裸指针（补充）", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="析构时触发",
                        notes="双重释放，asan 报 double-free。"))
    return out[:n]

# ============================ 6. lambda_capture ============================
def gen_lambda(n=30):
    out = []
    # T1: 引用捕获局部变量，返回后悬垂 (catch, asan stack-use-after-return)
    for i in range(1, 7):
        code = [
            "#include <functional>",
            "#include <cstdio>",
            "std::function<int()> make() {",
            "  int x = 42;",
            f"  return [&x]() {{ return x + {i}; }}; " + MARK + f" 引用捕获局部变量，返回后悬垂({i})",
            "}",
            "int main() {",
            "  auto f = make();",
            "  std::printf(\"%d\\n\", f());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="make",
                        desc="lambda 引用捕获局部变量并在作用域外调用", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="调用返回的 lambda 时触发",
                        notes="返回的 lambda 引用已销毁的局部变量，调用时 use-after-scope，asan 报 stack-use-after-return。"))
    # T2: 捕获 this 后对象销毁 (catch, heap-use-after-free)
    for i in range(1, 5):
        code = [
            "#include <functional>",
            "#include <memory>",
            "#include <cstdio>",
            "struct Widget {",
            "  int v = 7;",
            "  std::function<int()> bind() { return [this]() { return v; }; } " + MARK + f" 捕获 this({i})",
            "};",
            "int main() {",
            "  std::function<int()> f;",
            "  { auto w = std::make_unique<Widget>(); f = w->bind(); }",
            "  std::printf(\"%d\\n\", f());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="Widget::bind",
                        desc="lambda 捕获 this，对象销毁后仍调用", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="对象析构后调用 lambda 触发",
                        notes="捕获的 this 指向已释放对象，调用时 heap-use-after-free，asan 捕获。"))
    # T3: [=] 捕获副本误以为修改原变量 (miss, 逻辑)
    for i in range(1, 5):
        code = [
            "#include <cstdio>",
            "int main() {",
            "  int x = 1;",
            f"  auto f = [=]() mutable {{ x = 99; }}; " + MARK + f" 按值捕获后修改副本({i})",
            "  f();",
            "  std::printf(\"%d\\n\", x);  // 仍为 1",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="main",
                        desc="按值捕获 lambda 修改副本，原变量不变", sev="low",
                        exp_verdict="miss", exp_detectors=["asan"],
                        trigger="直接运行即触发",
                        notes="按值捕获得到副本，修改不影响原变量，属逻辑错误，sanitizer 不报——盲区。"))
    # T4: 默认捕获 [&] 意外捕获悬垂引用 (catch/miss)
    for i in range(1, 4):
        code = [
            "#include <functional>",
            "#include <cstdio>",
            "std::function<int()> mk() {",
            "  int y = 5;",
            f"  auto f = [&]() {{ return y + {i}; }}; " + MARK + f" 默认引用捕获局部变量({i})",
            "  return f;",
            "}",
            "int main() {",
            "  auto g = mk();",
            "  std::printf(\"%d\\n\", g());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="mk",
                        desc="默认 [&] 捕获导致悬垂引用", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="调用返回的 lambda 触发",
                        notes="默认引用捕获局部变量，返回后悬垂，asan 报 stack-use-after-return。"))
    # T5: 按值捕获指针，指向对象已销毁 (catch, 悬垂)
    for i in range(1, 4):
        code = [
            "#include <functional>",
            "#include <cstdio>",
            "std::function<int()> mk() {",
            "  int* p = new int(3);",
            f"  auto f = [p]() {{ return *p; }}; " + MARK + f" 按值捕获指针，但指针所指对象稍后释放({i})",
            "  delete p;",
            "  return f;",
            "}",
            "int main() {",
            "  auto g = mk();",
            "  std::printf(\"%d\\n\", g());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="mk",
                        desc="lambda 按值捕获指针，所指对象已释放", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="调用 lambda 时触发",
                        notes="捕获的指针所指对象在 lambda 返回前被 delete，调用时 use-after-free，asan 捕获。"))
    # T6: 递归 lambda 捕获自身未初始化 (miss/逻辑)
    code = [
        "#include <functional>",
        "#include <cstdio>",
        "int main() {",
        "  std::function<int(int)> fact;",
        "  fact = [fact](int n) { return n <= 1 ? 1 : n * fact(n - 1); }; " + MARK + " 递归 lambda 按值捕获尚未初始化的自身",
        "  try { std::printf(\"%d\\n\", fact(5)); } catch (const std::exception& e) { std::printf(\"threw\\n\"); }",
        "  return 0;",
        "}",
    ]
    out.append(dict(defect_type="lambda_capture", code=code, func="main",
                    desc="递归 lambda 按值捕获尚未初始化的自身（空副本）", sev="medium",
                    exp_verdict="miss", exp_detectors=["asan"],
                    trigger="递归调用时触发",
                    notes="按值捕获时复制的是仍为空的 std::function，递归调用抛 bad_function_call；应以 [&] 捕获。是真实缺陷但非 sanitizer 可检——盲区。"))
    # 补足到 n
    while len(out) < n:
        code = [
            "#include <functional>",
            "#include <cstdio>",
            "std::function<int()> mk() {",
            "  int z = 8;",
            "  return [&z]() { return z; }; " + MARK + " 引用捕获局部变量（补充）",
            "}",
            "int main() {",
            "  auto g = mk();",
            "  std::printf(\"%d\\n\", g());",
            "  return 0;",
            "}",
        ]
        out.append(dict(defect_type="lambda_capture", code=code, func="mk",
                        desc="lambda 引用捕获局部变量（补充）", sev="high",
                        exp_verdict="catch", exp_detectors=["asan"],
                        trigger="调用返回的 lambda 触发",
                        notes="悬垂引用，asan 报 stack-use-after-return。"))
    return out[:n]

# ============================ 主流程 ============================
def main():
    specs = []
    specs += gen_iterator(35)
    specs += gen_container(35)
    specs += gen_string(35)
    specs += gen_algorithm(35)
    specs += gen_smart(30)
    specs += gen_lambda(30)
    assert len(specs) == 200, f"期望 200 个，实际 {len(specs)}"

    for idx, sp in enumerate(specs, start=1):
        sid = f"D{idx:03d}"
        code_lines = sp["code"]
        # 计算缺陷行（1-based）
        dline = None
        for li, ln in enumerate(code_lines, start=1):
            if MARK in ln:
                dline = li
                break
        assert dline is not None, f"{sid} 缺少缺陷标记行"
        sp["defect_line"] = dline

        cpp = "\n".join(code_lines) + "\n"
        cpp = ("// 676c-D: planted C++ standard-library defect candidate (generated)\n"
               "// SPDX-License-Identifier: Apache-2.0\n" + cpp)
        # 重新对齐行号：头部加了 2 行注释，缺陷行 +2
        dline += 2

        json_obj = {
            "sample_id": sid,
            "defect_type": sp["defect_type"],
            "defect_location": {
                "line": dline,
                "function": sp["func"],
                "description": sp["desc"],
            },
            "severity": sp["sev"],
            "planted": True,
            "expected_verdict": sp["exp_verdict"],
            "expected_detectors": sp["exp_detectors"],
            "trigger_condition": sp["trigger"],
            "notes": sp["notes"],
            "generator": "676c-expD-generate_D",
        }
        cpp_path = os.path.join(OUT, f"sample_{sid}.cpp")
        json_path = os.path.join(OUT, f"sample_{sid}.json")
        with open(cpp_path, "w", encoding="utf-8") as f:
            f.write(cpp)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=2)
    print(f"生成完成：{len(specs)} 个样本（cpp+json）于 {OUT}")


if __name__ == "__main__":
    main()
