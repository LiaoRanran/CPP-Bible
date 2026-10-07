#include <cstdio>
int main(){ int i = 0; int a[2] = { i++, i++ }; std::printf("%d %d\n", a[0], a[1]); return 0; }
