// sample_B049
// [redacted]
// severity: medium
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B049.json)

#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(sizeof(int));
  *p = 7; /* [redacted]*/
  std::printf("%d\n", *p);
  return 0;
}
