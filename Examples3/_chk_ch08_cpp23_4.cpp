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
#include <format>
#include <version>
#include <string_view>
#include <cwchar>

namespace chk_ch08_cpp23_4 {
// std::print 直接打印（C++23 <print>；本机 GCC13 未实现，用 cout 等价演示）
void p(){ std::cout << 42 << "\n"; }
}
int main(){ return 0; }
