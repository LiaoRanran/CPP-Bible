// RW-039 | CVE-2020-15999 | FreeType | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-15999
// project_url: https://freetype.org/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: Pwn2Own 2020 —— 内嵌 PNG 位图的位图字体（sbix/CBDT）加载中，
//   face->glyph->bitmap 分配按小尺寸、渲染按大尺寸，堆越界写。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct GlyphBitmap {
    unsigned char* buffer;
    unsigned rows, width_bytes;
};

// BUG: allocation uses the *header-declared* small metrics; the blit loop uses
// the crafted larger metrics from the PNG payload.
void load_bitmap_glyph(GlyphBitmap* g, unsigned hdr_rows, unsigned hdr_wb,
                       unsigned png_rows, unsigned png_wb) {
    g->rows = png_rows;               // rendered size (large)
    g->width_bytes = png_wb;
    g->buffer = static_cast<unsigned char*>(std::malloc(hdr_rows * hdr_wb)); // small!
    for (unsigned y = 0; y < png_rows; ++y) {
        std::memset(g->buffer + (size_t)y * png_wb, 0xFF, png_wb); // overflow
    }
}

int main() {
    GlyphBitmap g{};
    load_bitmap_glyph(&g, /*hdr*/ 4, 4, /*png*/ 64, 64);  // 16 bytes alloc, 4096 written
    std::printf("glyph loaded %ux%u\n", g.rows, g.width_bytes);
    std::free(g.buffer);
    return 0;
}
