// sample_B088
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B088.json)

#include <cstdio>
int main(){
  void (*fp)() = nullptr;
  fp(); /*DEFECT: call through null function pointer (UB) -> ASan */
  return 0;
}