#ifndef sample_098_H
#define sample_098_H
int f7(){ return 1; } // <<PLANTED-DEFECT>> 头文件定义非 inline 函数，被多 TU 包含 -> 强多重定义
#endif

