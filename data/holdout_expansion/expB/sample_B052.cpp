// sample_B052
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B052.json)

#include <cstdio>
int main(){
  int* a = new int(1);
  int* b = new int(2);
  delete a;
  std::printf("%d\n", *b);
  /*DEFECT: resource leak: b never deleted */
  return 0;
}