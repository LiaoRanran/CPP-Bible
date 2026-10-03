#include <cstdio>
int main(){ unsigned char raw[4]={0x12,0x34,0x56,0x78}; unsigned v=*(unsigned*)raw; (void)v; std::printf("%u\n",v); return 0; }
