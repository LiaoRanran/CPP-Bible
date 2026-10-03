// sample_B051
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B051.json)

#include <cstdio>
int* ignored(){ int* p = new int(5); return p; }
int main(){
  ignored(); /*DEFECT: resource leak: returned allocation discarded */
  std::printf("ok\n");
  return 0;
}