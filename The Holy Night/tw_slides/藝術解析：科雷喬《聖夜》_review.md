# 《聖夜》影片轉投影片：核對與交付紀錄

## 輸出

- 語言：中文；字幕及補充頁採繁體中文與臺灣用語。
- 原始投影片：20張，依場景擷取清單；包含片末無旁白頁。
- 補充投影片：3張；最終update內共23張，均為1280 × 720。
- 最終順序：原始0001–0019、補充0020–0022、移至0023的原始末頁。
- 原始末頁於貼圖前已核對SHA-256與reorder紀錄一致：725c47eda6373f1910072a76eb3dfa512b626aa956ce8b8c8135284bb19f67ec。
- 末頁置入完整結尾貼圖；已逐張開啟所有23張PNG檢查，並清除右下NotebookLM文字標記。
- 完整音訊：615.189秒，約10分15秒，保留原始旁白速率。補充頁旁白已加入文字稿，尚未合成補充配音或新影片；原始manifest僅記錄原影片20頁時點，不作23頁的配音時序。
- 字幕：23個精確檔名區塊，與update順序一致，無時間戳記。

## 查閱的Markdown

- Correggio 1522-1530 The Holy Night chatgpt.md
- Correggio 1522-1530 The Holy Night claude.md
- The Holy Night (complete).md
- the_holy_night_youtube_en.md
- the_holy_night_youtube_tw.md

## 修正與補充依據

以《The Holy Night (complete).md》整合稿為主要比對依據；其餘四份檔案提供不同版本及雙語影片內容參照。直接層級沒有候選圖片，因此三張補充頁採文字版，未遞迴取用images子資料夾。

字幕修正包括科雷喬的多種誤辨、La Notte、聖嬰、馬槽、路加福音、帕爾馬、費茲威廉博物館、聖女彼濟達、雷焦艾米利亞、普拉托內里、埃斯特、奧古斯特三世、門格斯、牧人來拜及巴洛克等人名、地名、作品名和術語；也清除不完整字元，修正明顯的同音字及上下文可辨的語句。

補充0020：區分1522年10月14日委託、約1528–1530年成畫斷代，及原作楊木板油彩、256.5 × 188公分；整合稿作品辨識、年代與媒材附錄支持。

補充0021：聖嬰、雲端、遠景三個亮度區域，以及強烈明暗與柔和輪廓可並存；整合稿「夜色、色彩與柔化輪廓」支持。

補充0022：相關素描的推定性、與成畫的差異及不能認定為合約圖稿；整合稿「準備素描與創作過程」支持。

原始旁白中「畫布」等史實或詮釋說法保留其實際敘述，另以明確補充說明媒材差異，沒有把新增說明冒充原始音訊。各來源對精確安置年、原框、替代摹本及個別二戰路線的說法有差異；未新增這些不確定細節。

## 背景生成

使用內建imagegen工具。保留使用者完整風格方向，以無人物、無前景畫作、無文字標記的空背景呈現。適配投影片時增加中央80%為明亮低對比象牙白、深色限於裝飾邊角的條件，以便原有深色文字可讀。背景永久保留。

使用者原始方向：

Use a luminous High Renaissance style inspired by Correggio’s The Holy Night (La Notte), with radiant ivory white, warm golden amber, soft rose, muted ultramarine, earthy ochre, and deep velvety browns, delicate oil-glaze textures, soft sfumato transitions, and dramatic chiaroscuro centered on the Christ Child as the miraculous source of divine light, gently illuminating the Virgin Mary’s tender face, surrounding shepherds, and softly modeled angelic figures, with graceful flowing drapery, dynamic diagonal compositions, ethereal clouds, and shadowy rustic architectural details creating an intimate yet transcendent atmosphere of sacred wonder, while preserving expansive dark negative space and subtle luminous gradients so the artwork, titles, and subtitles remain visually dominant.

新增背景限制：Create one reusable clean 16:9 slide BACKGROUND, landscape. EMPTY BACKGROUND ONLY: NO people or figures whatsoever, no Christ Child, Mary, shepherds or angels, no foreground paintings, no text, letters, logos or watermarks. Convey sacred light through abstract warm luminous gradients, sfumato clouds, faint drapery-like brushwork and rustic architectural shadows at outer edges only. Center 80% must be luminous pale ivory, extremely quiet, low contrast, with high legibility for dark presentation text; reserve velvety dark tones for very narrow decorative outer corners. Subtle oil-glaze texture. Exact 16:9 composition.

## 檢查

- 所有PNG可開啟，尺寸一致；標題對比與流程箭頭已局部改善。
- 背景16:9，無人物、文字或標記。
- 編號連續，字幕一對一，補充頁位於原始末頁之前。
- 原音訊與原影片長度差小於0.001秒。
- git diff --check通過；檢查命令暫時停用LFS過濾器以避免唯讀.git限制，未變更Git設定。
