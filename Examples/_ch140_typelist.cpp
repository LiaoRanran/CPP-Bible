template <typename... Ts> struct TypeList {};
template <typename L> struct Front;
template <typename H, typename... T> struct Front<TypeList<H, T...>> { using type = H; };
struct A; struct B;
using L = TypeList<A, B>;
int main(){ using T = Front<L>::type; (void)sizeof(T*); return 0; }
