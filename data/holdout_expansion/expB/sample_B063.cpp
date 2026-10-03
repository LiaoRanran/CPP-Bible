// sample_B063
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B063.json)

#include <cstdio>
int main(){
  char buf[8] = {0};
  short* p = (short*)(buf + 1); /*DEFECT: misaligned short access -> UBSan catch */
  *p = 1;
  std::printf("%d\n", (int)*p);
  return 0;
}