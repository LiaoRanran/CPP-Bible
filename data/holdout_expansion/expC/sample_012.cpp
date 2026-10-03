int& f(){ int x = 5; return x; } // <<PLANTED-DEFECT>> 返回局部变量引用（dangling）
int main(){ (void)f(); return 0; }

