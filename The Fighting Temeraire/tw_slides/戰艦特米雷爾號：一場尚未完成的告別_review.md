# 投影片轉換與校對紀錄

- 語言：中文，字幕使用繁體中文與台灣用語。
- 來源影片：557.859410 秒，1280×720，24 fps。
- 完整音訊：557.859002 秒；保留原片語速及音高。
- 原始投影片：22 張；補充：3 張；更新版合計：25 張。
- 逐張開啟更新版 PNG 檢查，全部為 1280×720；字幕含 25 個相同順序、精確檔名的區塊，無時間戳記。
- 原第 22 頁移至第 25 頁，重排前後 SHA-256 相符，再置入 468×468 結尾貼圖。
- 已移除右下角 NotebookLM 字樣；第 2、4、7、12、18、21 頁調整文字對比、分行或版面。
- 本次交付為投影片、背景、原片完整音訊及逐頁文字。補充頁旁白是新增文字，尚未錄製或合成音訊；沒有輸出重製 MP4。

## 檢閱資料

只檢閱作者目錄直接包含的六份 Markdown；未遞迴讀取子目錄。作者目錄直接包含的候選圖片數為零，補充頁採文字版面。

1. Joseph Mallord William Turner 1839 The Fighting Temeraire.md
2. The Fighting Temeraire (complete).md
3. The Fighting Temeraire chatgpt.md
4. The Fighting Temeraire claude.md
5. the_fighting_temeraire_youtube_en.md
6. the_fighting_temeraire_youtube_tw.md

較早的簡介有入藏年代、目擊傳說及固定月牙象徵等不精確說法；補充內容依較完整整理稿及雙語企劃中對證據限制的說明。

## 字幕校對

以 small CPU/int8 模型取得 334 個語音片段，再依場景時間分組。校正人名、船名、地名、技術詞及明顯同音辨識錯字，例如 Tona／痛那→透納、特米雷二號／特名雷爾號→特米雷爾號、太霧四河→泰晤士河、圍桿／尾竿→桅杆、二等戰略艦→二等戰列艦、奈爾遜→納爾遜、透明照染→透明罩染、史詩級輓歌與橡樹等。另重轉錄拖船、火車與船隻對比片段，修正「畫面裡那輛狂飆的火車」等字句。

原旁白的「正中午」及「幹掉兩艘法國敵艦」保留在原對應段落；資料中的下午抵達時間、俘獲經過另置於第 24 頁，避免把新增史實冒充原片語音。

## 補充頁與依據

| 最終頁碼 | 主題 | 作者目錄內依據 |
|---|---|---|
| 22 | 厚塗、透明罩染、X 光提示舊畫布再利用；不能據此斷定趕工 | complete 整理稿；雙語企劃 Segment 5 |
| 23 | 月牙與衰老解讀的限制；軍艦報廢不等於海權或全部風帆終結 | complete 整理稿；雙語企劃 Segments 5、6、8 |
| 24 | 兩艘法艦被俘後於風暴沉沒；兩艘拖船；下午抵達與靠岸時間 | complete 整理稿的海戰與拖航段落 |

## 背景生成

使用內建 imagegen，生成後正規化為 1280×720 並永久保留。最終提示如下：

> Use case: productivity-visual
> Asset type: reusable 16:9 presentation background, 1280x720 or larger exact 16:9.
> Primary request: Use a luminous Romantic maritime style inspired by J. M. W. Turner’s The Fighting Temeraire, with blazing sunset gold, amber, crimson, soft rose, smoky blue-gray, and silvery white, atmospheric oil-painted textures and loose translucent brushwork, glowing light dissolving forms into mist and water, a majestic pale sailing ship contrasted with a small dark steam tug, shimmering reflections across the Thames, distant industrial silhouettes, and a poetic melancholic mood of transition from the age of sail to the modern industrial world, while preserving expansive luminous sky and misty negative space so the artwork, titles, and subtitles remain visually dominant.
> Composition: quiet, pale ivory/silvery mist low-contrast center occupying 80% of canvas, delicate decorative maritime brushwork at edges, ship and tug as small indistinct distant silhouettes along lower edge. A subtle background rather than a foreground painting. High legibility for dark slide text.
> Constraints: no people, no text, letters, logos, watermark, or framed paintings. Exact 16:9.

## 輸出位置

- 背景：`/Users/yingyuhsieh/Desktop/mcp/arts/The Fighting Temeraire/tw_slides/戰艦特米雷爾號：一場尚未完成的告別_background.png`
- 更新投影片：`/Users/yingyuhsieh/Desktop/mcp/arts/The Fighting Temeraire/tw_slides/update/`
- 完整音訊：`/Users/yingyuhsieh/Desktop/mcp/arts/The Fighting Temeraire/tw_slides/audio/戰艦特米雷爾號：一場尚未完成的告別_audio.m4a`
- 字幕稿：`/Users/yingyuhsieh/Desktop/mcp/arts/The Fighting Temeraire/tw_slides/subtitle/戰艦特米雷爾號：一場尚未完成的告別.txt`

`git diff --check` 通過。來源影片及既有研究資料未修改。
