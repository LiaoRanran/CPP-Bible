// sample_B064
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B064.json)

#include <cstdio>
int main(){
  alignas(1) char b[16] = {0};
  double* p = (double*)(b + 1); /*DEFECT: misaligned double access -> UBSan catch */
  *p = 1.0;
  std::printf("%f\n", *p);
  return 0;
}