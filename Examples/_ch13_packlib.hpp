// 文件：Examples/_ch13_packlib.hpp
// 行号：1
// 一个「头-only 包」的最小可编译示例，模拟被包管理器（vcpkg/Conan）
// 拉取后的形态：纯头文件 + inline/模板，无需链接 .lib/.a。
// 风格参考 gsl（非拥有视图）+ fmt（格式化），但完全自包含、零外部依赖。
#pragma once
#include <cstddef>
#include <string_view>
#include <format>
#include <iostream>

namespace pkg {

// gsl 风格：非拥有、连续的只读视图（与 std::span 同构，这里自实现以示包边界）
template <class T>
class span_view {
    const T* data_ = nullptr;
    std::size_t size_ = 0;
public:
    constexpr span_view(const T* d, std::size_t n) noexcept : data_(d), size_(n) {}
    constexpr const T* data() const noexcept { return data_; }
    constexpr std::size_t size() const noexcept { return size_; }
    constexpr const T& operator[](std::size_t i) const noexcept { return data_[i]; }
};

// fmt 风格：类型安全的格式化输出（底层复用 std::format，C++20 起可用）
template <class... Args>
inline void println(std::format_string<Args...> fmt, Args&&... args) {
    std::cout << std::format(fmt, static_cast<Args&&>(args)...) << '\n';
}

} // namespace pkg
