# ATOM-MEM-RAII-002（atom_claim）

## 正面

【MEM】ATOM-MEM-RAII-002
以下论断是否成立？依据是什么？
特殊成员函数要不要写，判据是"成员形状"而非记忆口诀：成员全是 RAII 类型（unique_ptr/vector/string） 时一个都不写（Rule of Zero）——编译器隐式生成的特殊成员函数语义全部正确（可拷贝成员拷贝隐式生成 且语义正确、不可拷贝成员如 unique_ptr 的拷贝被删除，移动/析构正确生成；实测 allocs=dtors=frees=1）； 管理裸资源时三件套（析构/拷贝构造/拷贝赋值，Rule of Three）或五件套（+ 移动构造/移动赋值，Rule of Five）必须齐写——只写析构会得到隐式浅拷贝，同一资源两次析构，析构真释放即 double free； 写移动构造必须标 noexcept，否则 vector 扩容搬迁退化为逐个拷贝。 （Rule of Zero 的隐式语义按成员形状各得其所：可拷贝 RAII 成员的拷贝**隐式生成且语义正确**， 不可拷贝成员如 unique_ptr 的拷贝被**删除**——不是一律"删除拷贝"。）

## 背面

论断：特殊成员函数要不要写，判据是"成员形状"而非记忆口诀：成员全是 RAII 类型（unique_ptr/vector/string） 时一个都不写（Rule of Zero）——编译器隐式生成的特殊成员函数语义全部正确（可拷贝成员拷贝隐式生成 且语义正确、不可拷贝成员如 unique_ptr 的拷贝被删除，移动/析构正确生成；实测 allocs=dtors=frees=1）； 管理裸资源时三件套（析构/拷贝构造/拷贝赋值，Rule of Three）或五件套（+ 移动构造/移动赋值，Rule of Five）必须齐写——只写析构会得到隐式浅拷贝，同一资源两次析构，析构真释放即 double free； 写移动构造必须标 noexcept，否则 vector 扩容搬迁退化为逐个拷贝。 （Rule of Zero 的隐式语义按成员形状各得其所：可拷贝 RAII 成员的拷贝**隐式生成且语义正确**， 不可拷贝成员如 unique_ptr 的拷贝被**删除**——不是一律"删除拷贝"。）
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-023: confirm
  - EV-MEM-024: confirm
  - EV-MEM-025: confirm
