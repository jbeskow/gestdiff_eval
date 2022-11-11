import subprocess
import os
def make_black_video(vin,vout):
    subprocess.call(['ffmpeg','-y','-i',vin,'-vf','eq=brightness=-1:contrast=-1:saturation=-1',vout])

def concatenate_video(vid1,vid2,vout):
    subprocess.call(['ffmpeg','-y','-i',vid1,'-i',vid2,'-filter_complex',
        '[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]',
        '-map','[v]','-map','[a]',vout])

def crop_video(vin,vout):
    subprocess.call(['ffmpeg','-y','-i',vin,'-filter:v','crop=in_w/2:in_h',vout])
    return vout

def downscale(vin,vout):
    subprocess.call(['ffmpeg','-y','-i',vin,'-vf','scale=iw/2:ih/2',vout])
    return vout


def sequential_side_by_side(vid1,vid2,vout):
    vid1 = downscale(vid1,'/tmp/vid1.mp4')
    vid2 = downscale(vid2,'/tmp/vid2.mp4')

    #vid1 = crop_video(vid1,'/tmp/vid1.mp4')
    #vid2 = crop_video(vid2,'/tmp/vid2.mp4')


    make_black_video(vid1,'/tmp/black1.mp4')
    make_black_video(vid2,'/tmp/black2.mp4')
    concatenate_video(vid1,'/tmp/black2.mp4','/tmp/left.mp4')
    concatenate_video('/tmp/black1.mp4',vid2,'/tmp/right.mp4')
    subprocess.call(['ffmpeg','-y','-i','/tmp/left.mp4','-i','/tmp/right.mp4','-filter_complex','hstack',vout])
   
# first play 1+2, then 2+3
def seq_triplet(vid1,vid2,vid3,vout):
    
    vid1 = crop_video(vid1,'/tmp/vid1.mp4')
    vid2 = crop_video(vid2,'/tmp/vid2.mp4')
    vid3 = crop_video(vid2,'/tmp/vid3.mp4')

    make_black_video(vid1,'/tmp/black1.mp4')
    make_black_video(vid3,'/tmp/black3.mp4')

    concatenate_video(vid1,'/tmp/black3.mp4','/tmp/left.mp4')
    concatenate_video(vid2,vid2,'/tmp/mid.mp4')
    concatenate_video('/tmp/black1.mp4',vid3,'/tmp/right.mp4')

    subprocess.call(['ffmpeg','-y','-i','/tmp/left.mp4','-i',
        '/tmp/mid.mp4','-i','/tmp/right.mp4','-filter_complex','hstack=inputs=3',vout])



def get_pairs(audios,systems):
    out = []
    pairs3 = [[0,1],[0,2],[1,2]] 
    pairs4 = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]] 

    if len(systems)==3:
        pairs = [[0,1],[0,2],[1,2]] 
    elif len(systems)==4:
        pairs = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    else:
        raise Exception('troubles')

    pairlist = []
    for audio in audios:
        for pair in pairs:
            sys1 = systems[pair[0]]
            sys2 = systems[pair[1]]
            f1 = '{}_{}.mp4'.format(audio,sys1)
            f2 = '{}_{}.mp4'.format(audio,sys2)
            comb1 = '{}_{}_{}_A.mp4'.format(audio,sys1,sys2)
            comb2 = '{}_{}_{}_B.mp4'.format(audio,sys1,sys2)
            out.append([f1,f2,comb1]) 
            out.append([f2,f1,comb2]) 
            pairlist.append('{}_{}'.format(sys1,sys2))
    return out,pairlist

indir='tsg'
outdir='tsg_comb'
audios = open('tsg/audios.txt').read().strip().split('\n')[0:36]
systems = open('tsg/systems.txt').read().strip().split('\n')
#import pdb;pdb.set_trace()
combos,pairlist = get_pairs(audios,systems)

import json
print(len(pairlist))
print(json.dumps(pairlist))
print(len(audios))
print(json.dumps(audios))

#xit()
for f1,f2,comb in combos:
    print(f1,f2,comb)
    sequential_side_by_side(os.path.join(indir,f1),os.path.join(indir,f2),os.path.join(outdir,comb))


#sequential_side_by_side('test1c.mp4','test3c.mp4','h1_3.mp4')
#seq_triplet('test1c.mp4','test3c.mp4','test2c.mp4','triplet.mp4')