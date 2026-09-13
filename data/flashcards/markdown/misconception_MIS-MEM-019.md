# MIS-MEM-019（misconception）

## 正面

【误解】MIS-MEM-019 写了析构函数就够了（违反 Rule of 3/5：漏写拷贝/移动）
触发说法：类里有指针就要写析构函数，写完析构就安全了

## 背面

为什么错：实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attempting double-free in ~Buggy）
反例 1：隐式拷贝/移动的生成规则由'用户声明了什么'驱动（[class.copy.ctor]）：声明析构函数 → 隐式拷贝仍生成但已废弃语义（浅拷贝）；正确的做法是三件套（析构/拷贝构造/拷贝赋值）或五件套（+ 移动）齐写，或直接 Rule of Zero 用 RAII 成员（见 ATOM-MEM-RAII-002 / EV-MEM-023 对照组）
关联原子：ATOM-MEM-RAII-002 ATOM-MEM-MOVE-002
