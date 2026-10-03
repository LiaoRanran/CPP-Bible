#include "sample_117_a.h"
int ga(){ return g; } // <<PLANTED-DEFECT>> 不同 TU 中 inline 变量 g 初值不一致（ODR 违例） }

