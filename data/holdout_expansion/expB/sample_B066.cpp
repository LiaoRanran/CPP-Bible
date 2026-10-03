// sample_B066
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B066.json)

#include <cstdio>
int main(){
  char buf[16] = {0};
  float* p = (float*)(buf + 1); /*DEFECT: misaligned float access -> UBSan catch */
  *p = 1.0f;
  std::printf("%f\n", *p);
  return 0;
}