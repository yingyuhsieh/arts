$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$srcTw = Join-Path $root 'The Fighting Temeraire\YouTube\一艘戰艦的最後航程：威廉·透納《特米雷爾號》.png'
$dstTw = Join-Path $root 'The Fighting Temeraire\tw_slides\update\戰艦特米雷爾號：一場尚未完成的告別_slide_0001.png'
$srcEn = Join-Path $root 'The Fighting Temeraire\YouTube\William Turner's The Fighting Temeraire- A Warship’s Last Voyage.png'
$dstEn = Join-Path $root 'The Fighting Temeraire\en_slides\update\The_Fighting_Temeraire_slide_0001.png'
Copy-Item -LiteralPath $srcTw -Destination $dstTw -Force
Copy-Item -LiteralPath $srcEn -Destination $dstEn -Force
Write-Output $dstTw
Write-Output $dstEn
