// ch35 ABI 与结构体 padding —— 真实反汇编证据源
// 展示 System V AMD64 ABI 的 padding 规则如何在机器码层面落地：
//   成员按对齐要求放置，char 之后插入 3 字节 padding，int 落在 offset 4。
struct alignas(8) Packet {
    char   tag;     // offset 0
    int    id;      // offset 4  (tag 后插入 3 字节 padding)
    double value;   // offset 8
};  // sizeof = 16, align = 8

int read_id(const Packet* p) __attribute__((used));
int read_id(const Packet* p) { return p->id; }

double read_value(const Packet* p) __attribute__((used));
double read_value(const Packet* p) { return p->value; }

void set_tag(Packet* p, char t) __attribute__((used));
void set_tag(Packet* p, char t) { p->tag = t; }
