"""Animate local gestures in the original painting, preserving its composition."""
from pathlib import Path
import subprocess
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageFilter, ImageOps


def main():
    root = Path(__file__).resolve().parent
    source = root / 'images/The Raft of the Medusa 梅杜莎之筏.jpg'
    output = root / 'The Raft of the Medusa_people_animation_8s_1280x720.mp4'
    if output.exists():
        raise FileExistsError(output)
    painting = Image.open(source).convert('RGB')
    height = 716
    width = round(painting.width * height / painting.height)
    art = np.asarray(painting.resize((width, height), Image.Resampling.LANCZOS))
    backdrop = ImageOps.fit(painting, (1280, 720)).filter(ImageFilter.GaussianBlur(30))
    backdrop = (np.asarray(backdrop) * 0.36).astype(np.uint8)
    yy, xx = np.mgrid[:height, :width].astype(np.float32)
    # Work in coordinates of the 1920 x 1310 reference for readable landmarks.
    x, y = xx * 1920 / width, yy * 1310 / height
    # cx, cy, support radius x/y, horizontal/vertical amplitude, phase, cycles.
    # Separate the signalling gestures, heads, and upper bodies from the raft.
    gestures = [
        (1328, 354, 105, 190, 6, 3, 0.0, 2),
        (1350, 270, 85, 90, 11, 3, 0.0, 2),
        (1336, 220, 72, 95, 17, 3, 0.0, 2),
        (1370, 166, 85, 85, 26, 7, 0.0, 2),
        (1340, 127, 170, 80, 32, 12, 0.25, 2),
        (1260, 143, 100, 65, 28, 16, 0.65, 2),
        (1505, 420, 85, 98, -15, -9, 0.8, 2),
        (1440, 388, 100, 65, -22, 12, 1.15, 2),
        (1450, 480, 80, 82, -5, -3, 0.8, 2),
        (1163, 423, 75, 85, 14, -15, 0.4, 2),
        (1107, 470, 85, 65, 8, -8, 0.4, 2),
        (1010, 478, 76, 100, 5, -3, 0.4, 2),
        (1268, 489, 80, 100, -7, -4, 1.2, 2),
        (1272, 550, 118, 100, -4, -4, 1.2, 2),
        (1315, 568, 70, 82, -8, -7, 1.2, 2),
        (1161, 663, 100, 100, 4, -4, 0.7, 2),
        (1043, 646, 80, 95, 4, -5, 0.7, 2),
        (564, 749, 100, 125, 2, 3, 1.5, 2),
    ]
    fields = []
    for cx, cy, rx, ry, ax, ay, phase, cycles in gestures:
        radius = ((x-cx)/rx)**2 + ((y-cy)/ry)**2
        weight = np.maximum(1-radius, 0)**2
        fields.append((weight, ax*width/1920, ay*height/1310, phase, cycles))
    water = np.maximum(
        np.clip((0.17-x/1920)/0.12, 0, 1)*np.clip((y/1310-0.4)/0.2, 0, 1),
        np.clip((x/1920-0.93)/0.07, 0, 1)*np.clip((y/1310-0.4)/0.2, 0, 1),
    )
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-r', '30',
               '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
               '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-n', str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    previews = []
    try:
        for i in range(240):
            time = i/240
            dx = np.zeros_like(xx)
            dy = np.zeros_like(yy)
            for weight, ax, ay, phase, cycles in fields:
                amount = np.sin(2*np.pi*cycles*time+phase)-np.sin(phase)
                dx += weight*ax*amount
                dy += weight*ay*amount
            dx += water*1.6*np.sin(y/1310*44-4*np.pi*time)
            dy += water*0.8*np.sin(x/1920*34-4*np.pi*time)
            animated = cv2.remap(art, xx-dx, yy-dy, cv2.INTER_CUBIC,
                                  borderMode=cv2.BORDER_REFLECT_101)
            frame = backdrop.copy()
            left, top = (1280-width)//2, (720-height)//2
            frame[top:top+height, left:left+width] = animated
            process.stdin.write(frame.tobytes())
            if i in (0, 30, 90, 150):
                previews.append(Image.fromarray(frame).resize((640, 360)))
    finally:
        process.stdin.close()
    if process.wait():
        raise RuntimeError('Video encoding failed')
    contact = Image.new('RGB', (1280, 720))
    for index, preview in enumerate(previews):
        contact.paste(preview, ((index % 2)*640, (index//2)*360))
    preview_path = Path(tempfile.gettempdir()) / 'medusa_people_preview.jpg'
    contact.save(preview_path)
    capture = cv2.VideoCapture(str(output))
    assert int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) == 240
    assert capture.get(cv2.CAP_PROP_FPS) == 30
    assert capture.get(cv2.CAP_PROP_FRAME_WIDTH) == 1280
    assert capture.get(cv2.CAP_PROP_FRAME_HEIGHT) == 720
    count = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        count += 1
    capture.release()
    assert count == 240
    print(f'Validated {count} frames: 8 seconds, 1280x720, 30 fps.\n{output}')
    print(f'Preview: {preview_path}')


if __name__ == '__main__':
    main()
