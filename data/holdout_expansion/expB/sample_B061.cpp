// sample_B061
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B061.json)

#include <cstdio>
int main(){
  alignas(1) char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned int access (UB) -> UBSan alignment catch */
  *p = 5;
  std::printf("%d\n", *p);
  return 0;
}