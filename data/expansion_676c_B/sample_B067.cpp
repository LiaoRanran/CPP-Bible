// sample_B067
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B067.json)

#include <cstdio>
int main(){
  char a[8] = {0};
  int* p = (int*)(a + 1);
  *p = 42; /*DEFECT: misaligned int punning write -> UBSan catch */
  std::printf("%d\n", *p);
  return 0;
}