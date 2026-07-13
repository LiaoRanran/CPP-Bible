#include <type_traits>
template <typename T, typename = void> struct HasFoo : std::false_type {};
template <typename T> struct HasFoo<T, std::void_t<decltype(&T::foo)>> : std::true_type {};
struct WithFoo { void foo(){} };
int main(){ static_assert(HasFoo<WithFoo>::value); return 0; }
