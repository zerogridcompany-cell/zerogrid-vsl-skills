"""間を詰める＋全体の倍率。tighten.py in out tempo  → out と out.keep.json（[元の始め,元の終わり,新しい始め]）"""
import sys,re,json,subprocess
inp,out,tempo=sys.argv[1],sys.argv[2],float(sys.argv[3])
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',inp],capture_output=True,text=True).stdout)
log=subprocess.run(['ffmpeg','-hide_banner','-i',inp,'-af','silencedetect=n=-38dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
def want(d): return 0.55 if d>=0.9 else (0.32 if d>=0.5 else min(d,0.2))
keep=[];cur=0.0
for s,e in zip(st,en):
    d=e-s
    if s<=0.01: cur=max(0,e-0.08); continue
    if e>=dur-0.01: keep.append([cur,s+0.25]); cur=None; break
    g=want(d)
    if d-g<0.02: continue
    keep.append([cur,s+g/2]); cur=e-g/2
if cur is not None: keep.append([cur,dur])
fc=';'.join(f"[0:a]atrim={x:.4f}:{y:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={y-x-0.01:.4f}:d=0.01[k{i}]" for i,(x,y) in enumerate(keep))
fc+=';'+''.join(f'[k{i}]' for i in range(len(keep)))+f'concat=n={len(keep)}:v=0:a=1,atempo={tempo}[o]'
subprocess.run(['ffmpeg','-y','-v','error','-i',inp,'-filter_complex',fc,'-map','[o]','-ar','48000',out],check=True)
m=[];t=0
for x,y in keep: m.append([round(x,4),round(y,4),round(t/tempo,4)]); t+=y-x
json.dump({"tempo":tempo,"keep":m},open(out.rsplit('.',1)[0]+'.keep.json','w'))
print('out',round(t/tempo,2),'s', len(keep),'区間')
