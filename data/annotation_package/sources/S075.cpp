#include <cstdio>
void f(double){std::printf("double");}
template<class T>void g(T t){f(t);}
void f(int){std::printf("int");}
int main(){g(1);}
