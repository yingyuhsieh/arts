"""Verify batch outputs and produce a compact delivery manifest."""
from pathlib import Path
import json,importlib.util,math,sys
import av,numpy as np
from PIL import Image,ImageDraw
spec=importlib.util.spec_from_file_location('renderer',Path(__file__).with_name('render_explainers.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
for n in m.NUMS:
    work=m.WORK/f'slide_{n:03d}';manifest=json.loads((work/'manifest.json').read_text());video=Path(manifest['video']);report=work/'verification.json'
    if report.exists():results.append(json.loads(report.read_text()));continue
    if not video.exists():continue
    try:c=av.open(str(video))
    except av.error.InvalidDataError:continue
    expected=manifest['duration_seconds']
    with c:
        assert len(c.streams.video)==1 and len(c.streams.audio)==1 and len(c.streams.subtitles)==0
        v=c.streams.video[0];a=c.streams.audio[0];v.thread_type='AUTO';v.codec_context.thread_count=4
        vd=float(v.duration*v.time_base);ad=float(a.duration*a.time_base)
        assert (v.width,v.height)==(3840,2160) and float(v.average_rate)==30
        assert v.codec_context.name=='h264' and a.codec_context.name=='aac' and v.codec_context.format.name=='yuv420p'
        assert abs(vd-expected)<.1 and abs(ad-expected)<.1 and abs(vd-ad)<.1
        prepared=m.prepare(n);samples=[];scenes=m.CONFIG[n][1]
        sheet=Image.new('RGB',(1920,540*math.ceil(len(scenes)/2)),'#eee8d8')
        for i,s in enumerate(scenes):
            end=scenes[i+1][0] if i+1<len(scenes) else expected
            t=22 if n==21 and i==0 else min(expected-.1,s[0]+min(3,(end-s[0])/2))
            c.seek(int(t/v.time_base),stream=v,backward=True)
            for frame in c.decode(v):
                if frame.time>=t:break
            im=frame.to_image();small=im.resize((480,270),Image.Resampling.LANCZOS)
            ref=m.render_frame(n,float(frame.time),prepared,expected).resize((480,270),Image.Resampling.LANCZOS)
            error=float(np.abs(np.asarray(small,dtype=np.float32)-np.asarray(ref,dtype=np.float32)).mean())
            assert error<4,(n,t,error)
            im.thumbnail((960,540));sheet.paste(im,(i%2*960,i//2*540))
            samples.append({'time':round(float(frame.time),3),'scene':i+1,'mean_pixel_error':round(error,4)})
        sheet.save(work/'encoded_preview.jpg',quality=93)
    with av.open(str(video)) as c:
        peak=0.;energy=0.;count=0
        for f in c.decode(audio=0):
            arr=f.to_ndarray().astype(np.float64);peak=max(peak,float(np.abs(arr).max()));energy+=float((arr*arr).sum());count+=arr.size
        rms=(energy/count)**.5
    assert peak>.01 and rms>.001
    result={'page':n,'video':str(video),'bytes':video.stat().st_size,'dimensions':[3840,2160],'fps':30,'video_codec':'h264','pixel_format':'yuv420p','audio_codec':'aac','video_duration_seconds':round(vd,4),'audio_duration_seconds':round(ad,4),'expected_duration_seconds':expected,'subtitle_streams':0,'audio_peak':round(peak,6),'audio_rms':round(rms,6),'scene_samples':samples,'verification_passed':True}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');results.append(result)
    print(f'VERIFIED page {n}: {vd:.3f}s, {len(samples)} scenes, {video.stat().st_size/1e6:.2f} MB',flush=True)
(m.WORK/'explainer_batch_manifest.json').write_text(json.dumps({'pages_requested':m.NUMS,'completed_pages':[r['page'] for r in results],'all_complete':len(results)==len(m.NUMS),'videos':results},ensure_ascii=False,indent=2)+'\n')
print(f'{len(results)}/{len(m.NUMS)} verified',flush=True)
