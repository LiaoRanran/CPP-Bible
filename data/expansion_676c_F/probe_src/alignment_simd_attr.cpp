#include <cstddef>
struct alignas(16) A{ double a[2]; };
int main(){ char buf[8]; A* p=(A*)(void*)buf; (void)p; return 0; }
