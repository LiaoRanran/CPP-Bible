int main(){ volatile int f=0; (void)f; while(f==0){} return 0; }
