// RW-040 | CVE-2022-27404 | FreeType | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-27404
// project_url: https://freetype.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: sfnt_init_face 对畸形 SFNT（TrueType）字体的表目录解析越界写。
// notes: 最小重构。ASan 应报 heap-buffer-overflow。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: the table directory count from the font header drives copies past the
// provided font data buffer.
void parse_sfnt_directory(const uint8_t* font, size_t font_len) {
    uint16_t num_tables = 0;
    std::memcpy(&num_tables, font + 4, 2);          // attacker-controlled count
    std::vector<char> names(num_tables);            // sized by the count
    for (uint16_t i = 0; i < num_tables; ++i) {
        // reads 16-byte entries far past font_len for a crafted count
        size_t off = 12 + (size_t)i * 16;
        names[i] = static_cast<char>(font[off]);    // OOB read when off >= font_len
    }
    std::printf("parsed %u table entries\n", num_tables);
}

int main() {
    // crafted font: header claims 0xFFFF tables but file is 32 bytes
    std::vector<uint8_t> font(32, 0);
    font[4] = 0xFF;
    font[5] = 0xFF;                                  // num_tables = 65535
    parse_sfnt_directory(font.data(), font.size());
    return 0;
}
