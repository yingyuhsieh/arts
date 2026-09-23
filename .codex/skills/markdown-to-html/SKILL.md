---
name: markdown-to-html
description: 將單一 Markdown 檔案轉換為 HTML 格式，儲存至 ./summary/htm。使用 /markdown-to-html 加上 Markdown 檔案路徑啟動。當需要「轉換 md 為 html」、「markdown 轉 html」、「convert markdown to html」時使用此技能。
metadata:
  version: "1.0.0"
  category: Documentation
---

## Overview

將指定的 Markdown 檔案轉換為格式美觀的 HTML 檔案，保留原始檔名但改為 `.html` 副檔名，儲存至 `./summary/htm` 目錄。

## Input Format

```
/markdown-to-html <path-to-markdown-file>
```

例如：
- `/markdown-to-html ./summary/Edward Hopper (complete).md`
- `/markdown-to-html summary/Egon Schiele (complete).md`

## Instructions

當此技能被觸發時，請依照以下步驟執行：

### Step 1: 讀取 Markdown 檔案

使用 Read 工具讀取使用者指定的 Markdown 檔案。如果檔案不存在，通知使用者並停止。

### Step 2: 確保輸出目錄存在

檢查 `./summary/htm` 目錄是否存在，若不存在則建立。

### Step 3: 轉換 Markdown 為 HTML

將 Markdown 內容轉換為完整的 HTML5 文件，遵循以下規則：

#### HTML 結構

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>從 H1 標題提取</title>
    <style>/* 見下方樣式定義 */</style>
</head>
<body>
    <!-- 轉換後的內容 -->
</body>
</html>
```

#### CSS 樣式

使用以下內嵌樣式（與專案既有 HTM 檔案風格一致）：

```css
body {
    font-family: "Microsoft JhengHei", "PMingLiU", serif;
    line-height: 1.8;
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
}
h1, h2, h3 {
    margin-top: 30px;
    margin-bottom: 15px;
}
h1 {
    font-size: 28px;
    border-bottom: 2px solid;
    padding-bottom: 10px;
}
h2 {
    font-size: 22px;
}
h3 {
    font-size: 18px;
}
ul, ol {
    margin-left: 20px;
}
li {
    margin-bottom: 15px;
}
p {
    text-indent: 2em;
    margin-bottom: 15px;
}
.quote {
    border-left: 4px solid #ccc;
    margin: 20px 0;
    padding: 10px 20px;
    color: #555;
    background: #f9f9f9;
}
.quote p {
    text-indent: 0;
}
strong {
    font-weight: bold;
}
em {
    font-style: italic;
}
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 30px 0;
}
```

#### Markdown 轉換規則

逐行解析 Markdown 內容，進行以下轉換：

1. **標題**: `# H1` → `<h1>`, `## H2` → `<h2>`, `### H3` → `<h3>`
2. **段落**: 連續非空白行組成段落，包裹在 `<p>` 標籤中
3. **粗體**: `**text**` → `<strong>text</strong>`
4. **斜體**: `*text*` → `<em>text</em>`
5. **無序列表**: `- item` 或 `* item` → `<ul><li>item</li></ul>`
6. **有序列表**: `1. item` → `<ol><li>item</li></ol>`
7. **引用**: `> text` → `<div class="quote"><p>text</p></div>`；連續的引用行應合併在同一個 `.quote` 容器中
8. **分隔線**: `---` 或 `***` → `<hr>`
9. **行內代碼**: `` `code` `` → `<code>code</code>`
10. **連結**: `[text](url)` → `<a href="url">text</a>`

注意事項：
- 生成的 HTML 不得使用 `blockquote` 元素。Markdown 引用與來源中的原始 `blockquote` 元素都必須轉換為 `<div class="quote">...</div>`；不得在輸出中留下其開始或結束標籤
- 段落中的換行應視為同一段落的延續（Markdown 軟換行）
- 空行分隔不同段落
- 列表項目可能包含多行文字
- 確保巢狀標記正確轉換（例如粗體內含斜體）

### Step 4: 儲存 HTML 檔案

將生成的 HTML 寫入 `./summary/htm/<原始檔名>.html`。

檔名規則：
- 保留原始 Markdown 檔案的名稱（不含副檔名）
- 副檔名改為 `.html`
- 例如：`Edward Hopper (complete).md` → `Edward Hopper (complete).html`

### Step 5: 驗證輸出

重新讀取生成的 HTML，確認文件可解析、標題與內容完整，並以不分大小寫搜尋 `blockquote`。若找到任何 `blockquote` 元素或 CSS 選擇器，先改成 `.quote` 容器與樣式，再進行回報。

### Step 6: 回報結果

告知使用者轉換完成，顯示輸出檔案路徑。

## Output

生成的 HTML 檔案儲存至 `./summary/htm/` 目錄。

## Best Practices

- 確保 HTML 輸出在瀏覽器中正確渲染繁體中文。
- `<title>` 標籤應使用 Markdown 檔案中的第一個 H1 標題，若無 H1 則使用檔名。
- 保持與專案既有 `articles/htm/` 目錄下 HTM 檔案一致的視覺風格。

## Common Pitfalls

- Markdown 檔案中若包含 HTML 原始碼，原則上應原樣保留；唯一例外是 `blockquote` 元素，必須轉換成 `<div class="quote">`，確保輸出完全不使用該元素。
- 注意檔名中的特殊字元（括號、空格、中文字）在檔案系統中的處理。
- 確保列表前後有正確的空行以避免轉換錯誤。
