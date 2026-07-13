#include <cstdio>
[[nodiscard]] int important() { return 7; }
int main(){ important(); std::printf("ignored\n"); }
