struct S{int v;};
S& h(){ S s{7}; return s; } // <<PLANTED-DEFECT>> 返回局部对象引用
int main(){ (void)h(); return 0; }

