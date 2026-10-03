int main(){
  int* p = new int[16];   // <<PLANTED-DEFECT>> 分配后从未释放 -> 内存泄漏
  (void)p;
  return 0;
}
