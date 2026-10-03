// sample_B065
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B065.json)

#include <cstdio>
int main(){
  char buf[4] = {0};
  int* p = (int*)(buf + 2); /*DEFECT: misaligned int access -> UBSan catch */
  *p = 9;
  std::printf("%d\n", *p);
  return 0;
}