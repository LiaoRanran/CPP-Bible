#include <cstdio>
struct T{T()=default;T(const T&){std::printf("copy");}T(T&&){std::printf("move");}};
int main(){T a; T b(std::move(a));}
