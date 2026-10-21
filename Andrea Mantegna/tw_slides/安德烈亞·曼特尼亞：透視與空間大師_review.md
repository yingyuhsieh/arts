# 處理與校對紀錄

- 語言：中文，字幕採繁體中文與臺灣用語。
- 原始影片：1280 × 720、24 fps、350.133696 秒，未修改。
- 擷取 22 頁、補充 2 頁，更新目錄共 24 頁。
- 原片尾由 0022 移至 0024 並加上完整結尾貼紙；貼紙前 SHA-256 已重建核對相符。
- 音訊為原片完整 AAC，350.132993 秒，完整解碼通過，未加速或變調。
- 本次交付分頁圖片、音訊及字幕稿，未另行合成影片；補充頁旁白已寫入字幕，尚未錄音。
- 原始時序見根目錄 manifest；加入補充後請依 update 重排紀錄安排。

## 審閱資料

- Andrea Mantegna (complete).md
- Andrea Mantegna chatgpt.md
- Andrea Mantegna 最重要的的作品.md
- Andrea_Mantegna_complete.md
- andrea_mantegna_youtube_en.md
- andrea_mantegna_youtube_tw.md

作者目錄直接包含的候選圖片為 0 張。依技能範圍未遞迴使用 images 子目錄，兩頁補充採文字頁。

## 補充依據

- 0022：奧韋塔里工程的多人合作、1944 年戰損，以及倖存原作、歷史照片、戰後拼復的區別。依據兩份 complete 文章的奧韋塔里段落及中文 YouTube 計畫段落 2。
- 0023：凱撒的凱旋以九幅大型畫布形成連續隊列；古典重建是文藝復興想像。依據 chatgpt 文章第十節及 complete 文章的凱旋段落。
- 來源對部分精確年代及作品回運年份有分歧，補充頁未使用有爭議的細節。
- 原始口播的誇飾與概括敘述保留，不以研究文章取代說話者的論點。

## 字幕校正

共修正 51 處辨識錯字及專名，包含：

- 芒特尼亞／滿特尼亞／滿天涯 → 曼特尼亞。
- 斯龐爾橋內 → 斯夸爾喬內；共渣家 → 貢扎加。
- 多納泰勞 → 多納太羅；伊薩貝拉德斯特 → 伊莎貝拉・德斯特。
- 極度 → 基督（僅作品名稱及基督頭部等誤辨處）。
- 丁合／丁恆 → 釘痕；透視縮短髮 → 透視縮短法。
- 圓中祈禱 → 園中祈禱；涼狼 → 涼廊。
- Dissorto因素 → di sotto in sù。
- 曾經是體驗 → 沉浸式體驗；空間措施 → 空間錯視。
- 石膏翻膜 → 石膏翻模；阿爾貝斯山 → 阿爾卑斯山。
- 帕納賽斯山 → 帕納塞斯山；妙思女神 → 繆斯女神。
- 其餘依語句修正同音錯字，保持原有內容與精確檔名區塊。

## 驗證與視覺檢查

- 24 張更新圖片均逐頁以原始解析度開啟檢查，皆為 1280 × 720。
- 可重用背景保存為 1920 × 1080，16:9，無人物、文字或標記。
- 原頁的背景裝飾已淡化，避免干擾文字。
- 0002 加明亮文字底板；0006、0020 改善標題層級與圖文重疊；0015 放大時間線說明、分行並加底板，保留年份、文字意義及順序。
- 已移除右下角 NotebookLM 字樣，0024 完整顯示結尾貼紙。
- 原影片部分微小外文示意標籤本身拼寫或線稿不明，保留原圖，未猜測重繪；主要中文標題與說明可讀。
- 字幕 24 個檔名區塊與更新圖片一一對應，順序正確、無時間戳。
- 原片尾貼紙前 SHA-256：797ea6fb624b6159c3c8f1ba7a6aff3047f7163592fe48beecd5767688f02324。
- git diff --check 通過；臨時音訊、聯絡表與補充 JSON 已清理，背景保留。

## 背景生成提示

使用內建 imagegen，提示如下：

```text
Use case: productivity-visual. Asset type: one reusable clean 16:9 presentation background, landscape. Art direction verbatim: Use a monumental Italian Renaissance style inspired by Andrea Mantegna, with warm terracotta, antique marble white, muted ochre, deep crimson, bronze green, cool slate blue, and weathered stone gray, combining finely detailed egg-tempera textures with sculptural figures resembling ancient Roman reliefs, sharply defined anatomical forms, intricate classical architecture, triumphal arches, carved columns, and archaeological ornament, dramatic di sotto in sù foreshortening, rigorous linear perspective, crisp directional lighting, angular drapery, and rugged rocky landscapes, creating a solemn, intellectually refined atmosphere of classical grandeur and archaeological realism, while preserving spacious architectural negative space, subdued fresco-like textures, and restrained decorative details so the artwork, titles, and subtitles remain visually dominant. Adaptation constraints for reusable background: no people or human figures (including relief people), no foreground paintings, no text, letters, logos or watermark. Very pale warm marble white center occupying 85% with extremely subtle fresco texture, quiet low contrast. Restrained classical carved architectural edge details only, very narrow borders, high legibility for dark text. Exact 16:9 composition.
```

