
#include <cstring>
int main(){ char d[8]; const char* s = "012345678901234567890123456789"; memcpy(d, s, 30); return d[0]; }
