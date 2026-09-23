#!/bin/zsh
set -euo pipefail

background='./Wanderer above the Sea of Fog/images/slide_backgrounds/demystifying_wanderer_background.png'
input_dir='.build/video-slides/raw-scenes'
output_dir='./Wanderer above the Sea of Fog/en_slides/update'
mkdir -p "$output_dir"

for index in {1..18}; do
  source_number=$(printf '%02d' "$index")
  target_number=$(printf '%03d' "$index")
  ffmpeg -hide_banner -loglevel error \
    -i "$background" \
    -i "$input_dir/scene-${source_number}.png" \
    -filter_complex "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[bg];[1:v]scale=1136:639,format=rgba,colorchannelmixer=aa=0.965[content];[bg][content]overlay=72:40:format=auto,format=rgb24" \
    -frames:v 1 "$output_dir/slide_${target_number}.png"
done
