#include <cstdio>
struct T{T(){}T(const T&){std::printf("copy");}T(T&&){std::printf("move");}};
void g(T x){}
void h(T&& x){g(x);}
int main(){h(T{});}
