int main(){
  int* p = new int[10];
  delete p; // <<PLANTED-DEFECT>> new[] / delete 不匹配
  return 0;
}

