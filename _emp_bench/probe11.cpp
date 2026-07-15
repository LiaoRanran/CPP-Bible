#include <version>
#define S2(x) #x
#define S(x) S2(x)
#define P(m) _Pragma(S(message("PROBE " #m "=" S(m))))
#define PU(m) _Pragma(S(message("PROBE " #m "=<undef>")))
#ifdef __cpp_impl_three_way_comparison
P(__cpp_impl_three_way_comparison)
#else
_Pragma("message(\"PROBE __cpp_impl_three_way_comparison=<undef>\")")
#endif
int main(){}
