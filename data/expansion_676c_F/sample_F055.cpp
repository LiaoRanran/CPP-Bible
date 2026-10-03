#include <cstdint>
#include <cstdio>
int main(){
  uint32_t magic = 0x12345678;
  // 直接把内存表示当作文件格式写入，假设所有机器小端
  std::printf("%08X\n", magic);  // <<PLANTED-DEFECT>> 文件格式硬编码主机端序
  return 0;
}
