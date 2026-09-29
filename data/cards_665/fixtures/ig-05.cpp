#include <memory>
#include <cstdio>
int main(){std::printf("%zu %zu\n", sizeof(void*), sizeof(std::unique_ptr<int>));}
