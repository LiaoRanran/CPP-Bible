int main(){ volatile int v=0; int* p=const_cast<int*>((volatile int*)&v); (void)*p; return 0; }
