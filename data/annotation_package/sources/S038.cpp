#include <vector>
#include <cstdio>
int main(){ int* p=nullptr; { std::vector<int> v{1,2,3}; p = &v[1]; } std::printf("%d\n", *p); return 0; }
