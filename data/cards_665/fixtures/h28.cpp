int* f(){int x=7; return &x;}
int main(){int* p=f(); return *p;}
