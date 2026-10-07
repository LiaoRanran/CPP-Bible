#include <thread>
int g=0;
int main(){std::thread a([]{for(int i=0;i<100000;i++)g++;});std::thread b([]{for(int i=0;i<100000;i++)g++;});a.join();b.join();}
