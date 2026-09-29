int f(float*p){*(int*)p=1; return (int)*p;}
int main(){float x=0; return f(&x);}
