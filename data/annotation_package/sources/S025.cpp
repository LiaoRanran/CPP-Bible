#include <cstring>
#include <cstdio>
int main(){ char* p = new char[4]; std::memcpy(p, "abcd", 5); std::printf("%c\n", p[0]); delete[] p; return 0; }
