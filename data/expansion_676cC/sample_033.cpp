int main(){
  try {
    int* p = new int[16];
    if (1) throw 1;
    delete[] p;
  } catch (int) {}
  return 0;
} // <<PLANTED-DEFECT>> 异常路径下 new[] 未释放 -> 泄漏

