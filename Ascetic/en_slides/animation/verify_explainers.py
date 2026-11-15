#!/usr/bin/env python3
"""Validate encoded explainers and save decoded-frame contact sheets."""
from pathlib import Path
import argparse
import json
import math
import subprocess
import wave
import sys

sys.dont_write_bytecode = True

import av
import numpy as np
from PIL import Image
import render_explainers as render


def decoded_frame(container,stream,t):
    container.seek(int(t*av.time_base))
    for frame in container.decode(stream):
        if frame.time>=t:
            return frame.to_image(),frame.time
    raise RuntimeError(f'No frame at {t}')


def verify(n):
    root=render.ROOT;folder=root/f'animation/slide_{n:03d}'
    video=root/f'video/ascetic_en_{n:03d}_explainer_4k.mp4'
    audio=root/f'audio/ascetic_en_{n:03d}_explainer_narration.wav'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    streams=probe['streams'];v=[s for s in streams if s['codec_type']=='video'];a=[s for s in streams if s['codec_type']=='audio']
    assert len(streams)==2 and len(v)==len(a)==1
    v,a=v[0],a[0]
    assert (v['width'],v['height'])==(3840,2160)
    assert v['r_frame_rate']=='30/1' and v['sample_aspect_ratio']=='1:1'
    assert v['codec_name']=='h264' and a['codec_name']=='aac'
    with wave.open(str(audio)) as f:
        duration=f.getnframes()/f.getframerate()
        samples=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.int32)
    assert abs(float(v['duration'])-duration)<.07
    assert abs(float(a['duration'])-duration)<.07
    assert np.max(np.abs(samples))>500
    scenes=render.DATA[n]['scenes'];frames=[];errors=[];bg=render.base(n)
    with av.open(str(video)) as container:
        stream=container.streams.video[0]
        for i,s in enumerate(scenes):
            end=scenes[i+1]['start'] if i+1<len(scenes) else duration
            t=end-.7
            actual,actual_t=decoded_frame(container,stream,t)
            actual_small=actual.resize((480,270),Image.Resampling.LANCZOS)
            expected=render.render(n,actual_t,bg,duration).resize((480,270),Image.Resampling.LANCZOS)
            mse=float(np.mean((np.asarray(actual_small,dtype=np.float32)-np.asarray(expected,dtype=np.float32))**2))
            assert mse<80,(n,t,mse)
            errors.append(mse)
            actual.thumbnail((960,540));frames.append(actual)
        first,_=decoded_frame(container,stream,.1)
        second,_=decoded_frame(container,stream,.8)
        x=np.asarray(first.resize((480,270)),dtype=np.float32)[55:245]
        y=np.asarray(second.resize((480,270)),dtype=np.float32)[55:245]
        motion=float(np.mean(np.abs(x-y)))
        assert motion>.5,(n,motion)
    sheet=Image.new('RGB',(1920,540*math.ceil(len(frames)/2)),'#15100c')
    for i,im in enumerate(frames):sheet.paste(im,((i%2)*960,(i//2)*540))
    sheet.save(folder/'encoded_preview.jpg',quality=94)
    report={'slide':n,'video':str(video),'duration_seconds':duration,'dimensions':[3840,2160],'fps':30,'sample_aspect_ratio':'1:1','streams':['h264','aac'],'subtitle_streams':0,'verified_scenes':len(frames),'decoded_frame_mse':errors,'motion_difference':motion,'bytes':video.stat().st_size}
    (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('slides',nargs='+',type=int)
    for n in parser.parse_args().slides:verify(n)
