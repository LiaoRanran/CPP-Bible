#include "_ch12_big.h"
int tu_13(int x){ return (int)ch12::tag + chain(x,x,x,x) + (int)sizeof(Blob<int,13>); }
