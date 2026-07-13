// _ch148_git_object.cpp
// 自包含 SHA-1 实现，复现 Git blob 对象的哈希，验证「内容寻址」模型。
// 编译：g++ -std=c++23 -O2 _ch148_git_object.cpp -o _ch148_git_object
// 期望：sha1("blob 5\0hello") = b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0
#include <cstdio>
#include <cstring>
#include <cstdint>

namespace sha1 {
    struct State { uint32_t h[5]; uint64_t len; unsigned char buf[64]; size_t bufn; };
    static uint32_t rol(uint32_t x, int n){ return (x<<n)|(x>>(32-n)); }
    static void block(State& s, const unsigned char* p){
        uint32_t w[80];
        for(int i=0;i<16;++i) w[i]=(uint32_t(p[i*4])<<24)|(uint32_t(p[i*4+1])<<16)|(uint32_t(p[i*4+2])<<8)|p[i*4+3];
        for(int i=16;i<80;++i) w[i]=rol(w[i-3]^w[i-8]^w[i-14]^w[i-16],1);
        uint32_t a=s.h[0],b=s.h[1],c=s.h[2],d=s.h[3],e=s.h[4];
        for(int i=0;i<80;++i){
            uint32_t f,k;
            if(i<20){f=(b&c)|((~b)&d);k=0x5A827999;}
            else if(i<40){f=b^c^d;k=0x6ED9EBA1;}
            else if(i<60){f=(b&c)|(b&d)|(c&d);k=0x8F1BBCDC;}
            else{f=b^c^d;k=0xCA62C1D6;}
            uint32_t tmp=rol(a,5)+f+e+k+w[i]; e=d;d=c;c=rol(b,30);b=a;a=tmp;
        }
        s.h[0]+=a;s.h[1]+=b;s.h[2]+=c;s.h[3]+=d;s.h[4]+=e;
    }
    static void init(State& s){ s.h[0]=0x67452301;s.h[1]=0xEFCDAB89;s.h[2]=0x98BADCFE;s.h[3]=0x10325476;s.h[4]=0xC3D2E1F0;s.len=0;s.bufn=0; }
    static void update(State& s,const unsigned char* data,size_t n){
        s.len+=n;
        while(n>0){
            size_t take=64-s.bufn; if(take>n) take=n;
            std::memcpy(s.buf+s.bufn,data,take); s.bufn+=take; data+=take; n-=take;
            if(s.bufn==64){ block(s,s.buf); s.bufn=0; }
        }
    }
    static void final(State& s,unsigned char out[20]){
        uint64_t bits=s.len*8;
        unsigned char pad=0x80; update(s,&pad,1);
        unsigned char zero=0;
        while(s.bufn!=56) update(s,&zero,1);
        unsigned char bits_be[8];
        for(int i=0;i<8;++i) bits_be[i]= (bits>>(56-i*8))&0xFF;
        update(s,bits_be,8);
        for(int i=0;i<5;++i){ out[i*4]=(s.h[i]>>24)&0xFF; out[i*4+1]=(s.h[i]>>16)&0xFF; out[i*4+2]=(s.h[i]>>8)&0xFF; out[i*4+3]=s.h[i]&0xFF; }
    }
}

static void to_hex(const unsigned char d[20], char out[41]){
    static const char* hx="0123456789abcdef";
    for(int i=0;i<20;++i){ out[i*2]=hx[d[i]>>4]; out[i*2+1]=hx[d[i]&0xF]; } out[40]='\0';
}

int main(){
    const char* content="hello";
    char buf[64];
    std::memcpy(buf,"blob 5",6); buf[6]='\0'; std::memcpy(buf+7,content,5);
    sha1::State s; sha1::init(s); sha1::update(s,reinterpret_cast<unsigned char*>(buf),12);
    unsigned char dig[20]; sha1::final(s,dig);
    char hex[41]; to_hex(dig,hex);
    std::printf("sha1(blob 5\\0hello) = %s\n",hex);
    std::printf("expect               = b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0\n");
    return std::strcmp(hex,"b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0");
}
