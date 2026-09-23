---
name: tw-video-integrate-audio-slide
description: Integrate Taiwan Mandarin audio, Traditional Chinese narration text, and static PNG slides into a YouTube-ready 4K MP4 using reliable slide timings while preserving the complete slide layout.
---

# 整合台灣中文音訊、投影片與字幕稿並輸出 4K

將台灣華語音訊、繁體中文 PNG 投影片及中文字幕稿整合成 3840×2160、30 fps 的靜態投影片影片。`--subtitle` 是旁白與對時文字，預設不燒錄字幕，也不建立字幕軌。

## 輸入與對時

- `--subtitle`：UTF-8（可含 BOM）中文字幕稿。
- `--images-dir`：PNG 投影片資料夾，支援中文及空白路徑。
- `--audio`：既有 M4A、WAV、MP3 等 FFmpeg 可讀取的音訊。
- `--manifest`：可選 JSON，使用 `{"slides":[{"filename":"中文_slide_0001.png","start":0.0}, ...]}`。
- `--output`：可選輸出路徑；預設 `<images-dir>/video/<subtitle-stem>_4k.mp4`。

支援檔名、帶時間編號及 Page 格式：

```text
[霧海上的漫遊者_slide_0001.png]
這是第一張投影片的旁白。

投影片 02｜00:25-00:50
這是第二張投影片的旁白。

[Page 3]
這是第三張投影片的旁白。
```

也接受 `SLIDE 01 | 00:00-00:25`、`幻燈片 01｜00:00-00:25` 及 `[第1頁]`。檔名與 Page 格式必須搭配 manifest；Page 頁碼須從 1 連續並對應全部自然排序的 PNG。

## 工作流程

1. 必要時搜尋 `subtitle/`、`audio/`、`tw_slides/` 及 `tw_slides/update/`。使用者指定 update 時使用該處圖片。
2. 優先使用明確指定的 manifest；否則採用圖片目錄內可唯一判定的 manifest 或帶時間標頭。時間必須來自本次音訊，不得依中文字數、英文音訊比例或平均秒數猜測。
3. 執行：

```text
python scripts/integrate_audio_slides.py --subtitle "中文字幕稿.txt" --images-dir "tw_slides/update" --audio "台灣中文旁白.m4a" --manifest "tw_slides/中文_slide_manifest.json" --output "tw_slides/video/台灣中文版_4k.mp4"
```

## 畫面與輸出規格

- 僅使用提供的 PNG，來源圖片檔保持不變。
- 圖片保持靜止並以硬切換頁，不加動畫或轉場。
- 輸出 3840×2160、30 fps、H.264、yuv420p、AAC 的 MP4。
- 使用高品質 Lanczos 等比例放大完整投影片；不得裁切或拉伸。非 16:9 圖片可加黑邊置於 4K 畫布中央。
- 不平移、重新生成或疊加字幕、浮水印、片頭與額外文字。
- 字幕稿只供旁白及時間核對；預設無字幕軌。

## 驗證與交付

回報 MP4 絕對路徑、檔案大小、片長、投影片數、來源尺寸、3840×2160 輸出尺寸與 30 fps。確認一條 H.264 視訊、一條 AAC 音訊、無字幕軌、音訊非空，且影音與來源音訊長度差不超過 0.1 秒。`expected_hard_cuts` 是投影片數減一；需要時抽查開頭、中間、結尾及換頁附近畫面。

## 相依套件

缺少時才安裝：`python -m pip install av imageio-ffmpeg pillow`。

附帶的 `scripts/integrate_audio_slides.py` 可獨立執行，並透過 `imageio-ffmpeg` 或 PATH 上的 FFmpeg 編碼。
