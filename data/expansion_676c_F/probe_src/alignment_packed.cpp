#pragma pack(push,1)
struct S{char c; int i;};#pragma pack(pop)
int main(){ S s; s.i=42; (void)s.i; return 0; }
