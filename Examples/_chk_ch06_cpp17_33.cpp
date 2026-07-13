#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <map>
#include <set>
#include <functional>
#include <thread>
#include <future>
#include <atomic>
#include <tuple>
#include <utility>
#include <initializer_list>
#include <array>
#include <stdexcept>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <limits>
#include <ciso646>
#include <iomanip>
#include <iterator>
#include <filesystem>
#include <variant>
#include <any>
#include <optional>
#include <ranges>
#include <bit>
#include <chrono>
#include <execution>
#include <type_traits>
#include <concepts>
#include <span>
#include <expected>
#include <print>
#include <mdspan>
#include <flat_map>
#include <flat_set>

namespace chk_ch06_cpp17_33 {
// 结构化绑定到数组
std::array<int,2> arr{1,2}; auto [x,y]=arr; (void)x;(void)y;
}
int main(){ return 0; }
