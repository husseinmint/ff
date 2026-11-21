import subprocess
S='/home/claude/eps/maqta3/ep04_beeswax/sfx/'
T_S=6.15
cues=[(0.1,'bm_paper.mp3',0.6),(1.2,'bm_draw.mp3',0.5),(3.6,'bm_ding.mp3',0.6),(4.8,'bm_whoosh.mp3',0.9),(5.6,'bm_hit.mp3',0.9),(3.6,'bm_tick.mp3',0.5),
(T_S+0.0,'bm_swish.mp3',0.6),(T_S+0.5,'bm_pop_small.mp3',0.6),(T_S+1.2,'bm_tick.mp3',0.5),(T_S+1.55,'bm_tick.mp3',0.5),(T_S+1.9,'bm_tick.mp3',0.5),
(T_S+2.6,'bm_hit.mp3',0.7),(T_S+2.65,'bm_count.mp3',0.5),(T_S+8.0,'bm_swish.mp3',0.6),(T_S+10.2,'bm_pop_small.mp3',1.0),(T_S+10.25,'bm_ding.mp3',0.7),(T_S+12.9,'bm_whoosh.mp3',0.5)]
cmd=['ffmpeg','-y','-loglevel','error','-f','lavfi','-t','20','-i','anullsrc=r=48000:cl=stereo']
for _,f,_ in cues: cmd+=['-i',S+f]
fl=[]
for k,(t,f,v) in enumerate(cues):
    fl.append('[%d:a]aresample=48000,volume=%s,adelay=%d|%d[a%d]'%(k+1,v,int(t*1000),int(t*1000),k))
fl.append('[0:a]'+''.join('[a%d]'%k for k in range(len(cues)))+'amix=inputs=%d:normalize=0:duration=first,alimiter=limit=0.9[out]'%(len(cues)+1))
cmd+=['-filter_complex',';'.join(fl),'-map','[out]','-t','20','mix2.wav']
subprocess.run(cmd,check=True)
