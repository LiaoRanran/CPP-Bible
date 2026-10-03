int main(){
  int input = 9;
  int* p = new int[2];
  if (input == 9) { delete[] p; } // <<PLANTED-DEFECT>> 特定输入时重复释放
  delete[] p;
  return 0;
}

