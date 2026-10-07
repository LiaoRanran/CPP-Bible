#include <cstdio>
struct alignas(8) L{long long v;};
int main(){alignas(2) char buf[sizeof(L)+8];L* p=reinterpret_cast<L*>(buf);p->v=1;std::printf("%lld\n",p->v);}
