// sample_B068
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B068.json)

#include <cstdio>
int main(){
  alignas(1) char s[12] = {0};
  int* p = (int*)(s + 5); /*DEFECT: misaligned int access -> UBSan catch */
  *p = 7;
  std::printf("%d\n", *p);
  return 0;
}