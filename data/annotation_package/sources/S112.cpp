#include <cstdio>
int bump(int& x){ return ++x; }
int show(int a, int b){ return a * 10 + b; }
int main(){ int i = 0; std::printf("%d\n", show(bump(i), bump(i))); return 0; }
