int main(){
  int* p = new int[16];
  try {
    throw 1;
  } catch (int) {
    return 0;   // <<PLANTED-DEFECT>> 异常路径提前返回，p 未释放 -> 内存泄漏
  }
  delete[] p;
  return 0;
}
