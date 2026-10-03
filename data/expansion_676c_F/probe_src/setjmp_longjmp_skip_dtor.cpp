#include <csetjmp>
#include <string>
jmp_buf env;
int main(){ volatile int once=0; if(setjmp(env)==0){ std::string s="hi"; if(!once){once=1; longjmp(env,1);} } return 0; }
