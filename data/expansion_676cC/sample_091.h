#ifndef sample_091_H
#define sample_091_H
int f0(){ return 1; } // <<PLANTED-DEFECT>> 头文件定义非 inline 函数，被多 TU 包含 -> 强多重定义
#endif

