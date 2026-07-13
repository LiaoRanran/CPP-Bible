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

namespace chk_ch05_cpp14_25 {
// 变量模板作常量
template<class T> constexpr bool is_int_v = std::is_same_v<T,int>; static_assert(is_int_v<int>, "");
}
int main(){ return 0; }
