// _bench_d5_ch162_json.cpp
// D5 benchmark: hand-written recursive-descent JSON parser vs nlohmann-like DOM vs SIMD-style scan
#include <cstdio>
#include <chrono>
#include <cstring>

volatile int g_sink = 0;

// --- Mini JSON value (variant-like) ---
struct JsonVal {
    enum Type { Null, Bool, Num, Str, Arr, Obj } type;
    double num;
    char strbuf[64];
};

// Hand-written recursive-descent parser (minimal: numbers + strings + arrays)
struct Parser {
    const char* p;
    const char* end;

    void skip_ws() {
        while (p < end && (*p==' '||*p=='\t'||*p=='\n'||*p=='\r')) p++;
    }

    JsonVal parse_val() {
        skip_ws();
        JsonVal v;
        memset(&v, 0, sizeof(v));
        if (p >= end) { v.type = JsonVal::Null; return v; }
        if (*p == '"') { v.type = JsonVal::Str; p++; int i=0; while (p<end && *p!='"' && i<63) v.strbuf[i++]=*p++; v.strbuf[i]=0; if (p<end) p++; return v; }
        if (*p == '[') { v.type = JsonVal::Arr; p++; int count=0; skip_ws(); if (p<end && *p==']') {p++; v.num=0; return v;} while (p<end && *p != ']') { JsonVal e = parse_val(); count++; skip_ws(); if (p<end && *p==',') p++; skip_ws(); } if (p<end) p++; v.num = count; return v; }
        if (*p >= '0' && *p <= '9' || *p=='-' || *p=='+') {
            v.type = JsonVal::Num;
            double val = 0; double sign = 1;
            if (*p=='-') { sign=-1; p++; }
            while (p<end && *p>='0' && *p<='9') { val = val*10 + (*p-'0'); p++; }
            v.num = sign * val;
            return v;
        }
        v.type = JsonVal::Null; return v;
    }
};

[[gnu::noinline]] int bench_parse(const char* json, int len) {
    Parser parser{json, json+len};
    int count = 0;
    for (int i = 0; i < 1000; i++) {
        parser.p = json;
        JsonVal v = parser.parse_val();
        count += (int)v.num;
    }
    return count;
}

// SAX-style streaming count (no allocation, just scan structure)
[[gnu::noinline]] int bench_sax(const char* json, int len) {
    int depth = 0;
    int elements = 0;
    for (int i = 0; i < 1000; i++) {
        depth = 0; elements = 0;
        for (int j = 0; j < len; j++) {
            char c = json[j];
            if (c == '[' || c == '{') { depth++; elements++; }
            else if (c == ']' || c == '}') { depth--; }
        }
    }
    return elements;
}

// Simple token count (find all value boundaries)
[[gnu::noinline]] int bench_token_count(const char* json, int len) {
    int tokens = 0;
    for (int i = 0; i < 1000; i++) {
        tokens = 0;
        for (int j = 0; j < len; j++) {
            char c = json[j];
            if (c == '"' || c == ':' || c == ',') tokens++;
        }
    }
    return tokens;
}

int main() {
    // Realistic JSON payload: array of 100 numbers
    char buf[8192];
    int pos = 0;
    pos += sprintf(buf+pos, "[");
    for (int i = 0; i < 100; i++) {
        pos += sprintf(buf+pos, "%s%d", i>0?",":"", i * 7 + 3);
    }
    pos += sprintf(buf+pos, "]");
    int len = pos;

    struct { const char* name; int (*fn)(const char*, int); double median; } tests[] = {
        {"recursive-descent", bench_parse,       0},
        {"SAX streaming",     bench_sax,          0},
        {"token scan",        bench_token_count,  0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(buf, len);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch162 json D5 benchmark (1000 iterations x %d bytes, 5-trial median) ===\n", len);
    for (auto& t : tests)
        printf("  %-25s  %8.3f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}
