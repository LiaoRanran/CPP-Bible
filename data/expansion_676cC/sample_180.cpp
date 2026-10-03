int main(){
  int input = 5;
  int* p = new int[2];
  if (input == 5) { delete[] p; } // <<PLANTED-DEFECT>> 特定输入时重复释放
  delete[] p;
  return 0;
}

