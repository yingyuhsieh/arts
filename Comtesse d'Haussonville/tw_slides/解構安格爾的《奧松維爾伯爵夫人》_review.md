# 製作與校對紀錄

- 語言：中文，字幕使用繁體中文與台灣用語。
- 原片：21 頁，1280×720，24 fps，496.094 秒。
- 更新版：24 頁，包含 3 頁補充；每張 PNG 均為 1280×720。
- 完整 AAC 音訊：496.094 秒，已解碼檢查有聲訊號，未加速或變調。
- 字幕：24 個精確 PNG 檔名區塊，順序與 update 一致，不含時間戳記。第 24 頁是原片無旁白末頁。
- 新增頁僅提供畫面與旁白稿，尚未配音。本次交付為 video-to-slides 素材，未輸出延長版 MP4。

## 已閱讀的直接包含 Markdown

- Comtesse d'Haussonville (complete).md
- Comtesse d'Haussonville book.md
- Comtesse d'Haussonville chatgpt.md
- Comtesse d'Haussonville claude.md
- Jean-Auguste-Dominique Ingres 1845 Comtesse d’Haussonville.md
- comtesse_dhaussonville_youtube_en.md
- comtesse_dhaussonville_youtube_tw.md

## 修正與保留

字幕共記錄 54 組辨識或正字修正，另依語境處理代名詞與標點。例如：協議→斜倚、閉爐臺→壁爐台、斷面場群→緞面長裙、政治家體驗→政治家提耶、路伊斯→路易絲、佛裡克→弗里克。完整逐項紀錄見同名前綴 corrections.json。

原片口述的「光學不可能」等肯定語氣，保留為原音所述，並在補充第 23 頁明確區分視覺評論與光學驗證。原片的「書中」及「披扇／散落一角」等既有點陣文字依技能的原文保留要求未改寫；字幕使用畫中、披肩與折角的正確語境，補充頁亦採披肩。

第 1、20 頁重新整理標題斷行；第 4、12、14、17 頁改善文字襯底與邊距；第 10 頁放大時間線說明；第 17 頁放大原有英文標籤，保留原圖邏輯與文字。移除右下角 NotebookLM 殘留標記。全部 24 頁已逐張以實際輸出解析度檢視。

## 補充內容與來源

1. 第 21 頁：路易絲的 1858、1872 年著作；依 complete 文章「她是誰」及中文內容計畫第 6 段。
2. 第 22 頁：1882 年家族繼承、1927 年購藏與 1986 年兩畫重聚；依 complete 文章收藏章及[弗里克 1986 年展覽紀錄](https://www.frick.org/exhibitions/past/1986/ingres_portraits)。
3. 第 23 頁：歌劇歸來的情境、鏡像評論、早期草稿與三年跨度的證據界線；依 complete 文章與中文計畫查證備註。[弗里克提供的作品解說](https://artsandculture.google.com/asset/comtesse-d-haussonville-jean-auguste-dominique-ingres/gQGTMTaShUJNKA?hl=en)另核對了創作起點與畫面情境。

作者目錄直接包含的候選圖片數為 0；依技能不遞迴進入 images 子目錄，補充頁採文字與年份資訊設計。未引入與內容無關的圖片。

## 排序、背景與對時

原始第 21 頁已移至第 24 頁，移動後與貼紙前的 SHA-256 一致：`177434272fa60af20d643c886633d4ba22df6c3b098a2f33f53d1c3d5165a60e`。最後置中加入 468×468 的完整片尾貼紙。

共用背景由內建 image_gen 依使用者完整藝術方向生成，另加 16:9、中央留白、無人物與無文字限制。已保留 background.png 與 background_prompt.txt。

原始 slide_manifest.json 記錄原片 21 個場景的時間，不能直接當作新增 24 頁的配音時間表。補充旁白完成後，應依實際音訊重建換頁時間並自然延長片長。
