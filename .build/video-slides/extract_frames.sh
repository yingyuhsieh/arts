#!/bin/zsh
set -euo pipefail

video='./Wanderer above the Sea of Fog/Demystifying_the_Wanderer.mp4'
out='.build/video-slides/raw-scenes'
mkdir -p "$out"

times=(
  26.70 57.70 85.60 117.10 147.00 176.30
  202.00 232.00 261.80 280.10 312.40 345.70
  376.50 410.00 443.30 472.50 503.10 506.20
)

index=1
for timecode in "${times[@]}"; do
  number=$(printf '%02d' "$index")
  ffmpeg -hide_banner -loglevel error -ss "$timecode" -i "$video" -frames:v 1 -q:v 2 "$out/scene-${number}.png"
  index=$((index + 1))
done
