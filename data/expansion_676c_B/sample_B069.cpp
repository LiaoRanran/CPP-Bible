// sample_B069
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B069.json)

#include <cstdio>
int main(){
  char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned read+write punning -> UBSan catch */
  *p = *p + 1;
  std::printf("%d\n", *p);
  return 0;
}