// sample_B090
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B090.json)

#include <cstdio>
struct S { void f(){ std::printf("ok\n"); } };
int main(){
  S* s = nullptr;
  s->f(); /*DEFECT: call member function through null pointer (UB) -> ASan */
  return 0;
}