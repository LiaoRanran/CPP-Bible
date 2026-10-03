// sample_B070
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B070.json)

#include <cstdio>
int main(){
  char b[16] = {0};
  double* p = (double*)(b + 7); /*DEFECT: misaligned double access -> UBSan catch */
  *p = 3.14;
  std::printf("%f\n", *p);
  return 0;
}