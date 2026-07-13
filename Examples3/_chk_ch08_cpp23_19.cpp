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

namespace chk_ch08_cpp23_19 {
// std::mdspan 多维视图访问（本机用 span 等价演示）
int d2[4]; std::span<int> m2(d2); void use_md(){ m2[0]=1; }
}
int main(){ return 0; }
