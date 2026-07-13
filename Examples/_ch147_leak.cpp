#include <cstdio>
int* make() { return new int(1); }       // 调用方需 delete
int main(){ int* p = make(); std::printf("%d\n", *p); /* 漏 delete */ }
