long long g_nofence(){ long long s=0; for(int i=0;i<100;++i) s+=i; return s; }
long long g_fence(){ long long s=0; for(int i=0;i<100;++i){ s+=i; asm volatile("" : "+r"(s)); } return s; }
