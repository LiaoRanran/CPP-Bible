// RW-031 | CVE-2023-28484 | libxml2 | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-28484
// project_url: https://gitlab.gnome.org/GNOME/libxml2
// year: 2023 | severity: MEDIUM | source_type: cve
// mechanism: XML Schema 解析（xmlSchemaFixupComplexType）对畸形 schema 访问
//   可空返回值导致 NULL 解引用（DoS）。
// notes: 最小重构。UBSan（null）或 ASan（SEGV near null）可命中。
#include <cstdio>
#include <cstring>

struct SchemaType {
    const char* name;
    SchemaType* base;     // may be null for malformed schemas
};

// BUG: no null check on lookup result for malformed schema content.
SchemaType* lookup_type(SchemaType** table, int n, const char* name) {
    for (int i = 0; i < n; ++i) {
        if (std::strcmp(table[i]->name, name) == 0) return table[i];
    }
    return nullptr;       // not found -> null
}

int schema_fixup(SchemaType** table, int n) {
    SchemaType* t = lookup_type(table, n, "xsd:attacker-madeup");
    return static_cast<int>(std::strlen(t->name));  // NULL deref
}

int main() {
    SchemaType a{"xsd:string", nullptr};
    SchemaType* table[1] = {&a};
    int r = schema_fixup(table, 1);
    std::printf("fixup result %d\n", r);
    return 0;
}
