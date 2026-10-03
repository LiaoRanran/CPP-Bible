int main(){
  int* p = new int[16];
  if (true) return 0;   // <<PLANTED-DEFECT>> 提前返回，p 未释放 -> 内存泄漏
  delete[] p;
  return 0;
}
