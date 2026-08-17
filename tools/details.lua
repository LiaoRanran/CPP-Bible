-- details.lua — 让 <details><summary>…</summary> 练习答案块在 pandoc LaTeX/PDF 下保留「答案与解析」标签。
--
-- 背景：
--   site(mkdocs-material) 与 EPUB(HTML 输出) 原生渲染 <details> 折叠块，无需处理。
--   但 PDF 走 --pdf-engine=xelatex，LaTeX writer 会丢弃 RawBlock(html)。
--   仓库中 <details><summary>答案与解析</summary> 多数后跟空行，故答案正文是「普通 markdown」
--   （正常渲染），仅 <details>/</details>/<summary> 标签被丢弃 → PDF 丢失「答案与解析」标签与折叠。
--   本过滤器在遇到开头为 <details 的 RawBlock(html) 时，输出一个加粗标签段落；
--   若该标签内联包含答案正文（无空行分隔），则一并用 pandoc.read 解析补回。
--
-- 用途：仅用于 PDF（generate_pdf.sh）。EPUB 保留原生 <details>，切勿对本过滤器接入 EPUB。

function RawBlock(raw)
  if raw.format ~= 'html' then return nil end
  local s = raw.text
  local rest = s:match('^%s*<details[^>]*>(.*)$')
  if not rest then return nil end

  local summary, body = rest:match('^%s*<summary>(.-)</summary>(.*)$')
  if not summary or summary == '' then
    summary = '答案与解析'
    body = rest
  end
  body = body:gsub('%s*</details>%s*$', '')

  local out = { pandoc.Para({ pandoc.Strong({ pandoc.Str(summary) }) }) }
  if body and body:match('%S') then
    for _, b in ipairs(pandoc.read(body, 'markdown').blocks) do
      table.insert(out, b)
    end
  end
  return out
end
