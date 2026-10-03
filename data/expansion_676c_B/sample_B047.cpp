// sample_B047
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B047.json)

#include <cstdlib>
#include <cstring>
#include <cstdio>
int main(){
  char* s = (char*)std::malloc(8);
  std::strcpy(s, "leak"); /*DEFECT: resource leak: malloc'd buffer not freed */
  std::printf("%s\n", s);
  return 0;
}
