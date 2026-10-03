int* g(){ int a[3] = {1,2,3}; return a; } // <<PLANTED-DEFECT>> 返回局部数组指针
int main(){ (void)g(); return 0; }

