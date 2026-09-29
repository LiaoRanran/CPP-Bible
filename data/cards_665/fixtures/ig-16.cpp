#include <cstdio>
#include <utility>
struct T{T()=default;T(const T&){std::printf("copy");}};  // 故意不提供移动构造
int main(){T a; T b(std::move(a));}
