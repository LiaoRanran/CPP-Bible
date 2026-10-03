#include <csetjmp>
#include <string>
#include <cstdio>
static jmp_buf env;
int main(){
  volatile int guard = 0;
  if (setjmp(env) == 0) {
    std::string s = "resource";  // 非平凡对象
    if (!guard) { guard = 1; std::longjmp(env, 1); }  // <<PLANTED-DEFECT>> longjmp 跳过 s 的析构（资源泄漏/UB）
  }
  std::printf("done\n");
  return 0;
}
