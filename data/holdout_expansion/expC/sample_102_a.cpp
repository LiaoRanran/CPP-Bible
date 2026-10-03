#include "sample_102_a.h"
int fa(){ return f(); } // <<PLANTED-DEFECT>> 不同 TU 中 inline f 定义不一致（ODR 违例） }

