#include <cstddef>
template <typename... Ps> struct PolicySet { static constexpr std::size_t n = sizeof...(Ps); };
struct P1{}; struct P2{};
int main(){ return (int)PolicySet<P1, P2>::n; }
