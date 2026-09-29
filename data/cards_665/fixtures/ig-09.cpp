int f(int*p){*p=1; return *p;}
int main(){int x=0; return f(&x);}
