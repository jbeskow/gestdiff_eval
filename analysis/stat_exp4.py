import sys
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison


csvf = sys.argv[1]
df0 = pd.read_csv(csvf)
systems = ['GDSg1p5','ZE','GDS']
skiprows = 53
studyid = '636e70d289a9acb4399c636e'
skipusers = ['608718e0a8520f7baac735e7']+['60fd0572a7b7e6b6bea8e79b', '5ddc37fc0605ebbb311ced36', '62b05696557fb90078fe57ff', '5c3d48955fd1050001a99364', '60855f538b53f54054804748']+['5da3502604be3d0011caf90f', '600463555dafb42a777cf5a3', '6303809730ba6f53288a4f85', '6163f8a826c9b98b20139416', '5ca53042aa2c820001fef20a']+['5b6f312393405d000159e471', '5ef5f74fb4a08f2676fb3aba']

datadir = 'zeg_style_silent'
#print(skipusers)

def parse_filename(fn):
    x,A,B,order = fn.split('/')[1].split('.')[0].split('-')
    if order =='A':
        return A,B
    else:
        return B,A

subjects = {}
failed = {}
data = {'system':[],'score':[]}
for idx,row in df0.iterrows():
    if idx<skiprows:
        continue

    if row['study_id'] != studyid:
        continue

    if row['subject_id'] in skipusers:
        #print('skipping user')
        continue

    #print('start')
    stim = row['stimulus']
    resp = row['response']
    subj = row['subject_id']
    #print(stim,resp,row['experiment'])

    if not isinstance(stim,str):
        continue

    if 'attention' in stim:
        if int(resp) != 4:
            #print('attention fail:',stim,resp,subj)
            if subj not in failed:
                failed[subj] = 1
            else:
                failed[subj] += 1

    if datadir in stim:
        subjects[subj] = True
        resp = int(resp)
        #print(idx,stim,resp)
        L,R = parse_filename(stim)
        Lscore = 2-resp
        Rscore = resp-2
        #print(L,Lscore)
        #print(R,Rscore)
        data['system'].append(L)    
        data['score'].append(Lscore)    
        data['system'].append(R)    
        data['score'].append(Rscore)    
    #        print(parse_filename1(row['stimulus']))
    #    print(row['stimulus'],row['response'])
df = pd.DataFrame.from_dict(data)
print('subjects:',len(subjects.keys()))
print('responses:',df.shape[0]/2)
print('failed:')
ff = [id for id in failed.keys() if failed[id]>=2]
print(ff)


# MEANS & STD

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h, m-h, m+h

print ('Mean and confidence interval')
print ('============================')
print('model\tmean\t95%int')
for system in systems:
    data = df[df['system']==system]['score'].tolist()
    m,h,c0,c1 = mean_confidence_interval(data)

    #print('{}\t{:.3f} +/-{:.3f}'.format(system, m, h))
    print('{}\t& {:.3f} \pm {:.3f}\t'.format(system, m, h))


# ANOVA

def anova_and_tukey(df,depvar,indepvar,catlist):
    
    dd = []
    for type in catlist:
        vals = df[df[indepvar]==type][depvar].tolist()
        dd.append(vals)
        #print(type,len(vals),len(dd))

    f,p = stats.f_oneway(*dd)


    print ('One-way ANOVA')
    print ('=============')
 
    print ('F value:', f)
    print ('P value:', p, '\n')

    data = df[df[indepvar].isin(catlist)][depvar].to_numpy()
    groups = df[df[indepvar].isin(catlist)][indepvar].to_numpy()
    
    mc = MultiComparison(data,groups,catlist)
    result = mc.tukeyhsd()
    print(result)

    
anova_and_tukey(df,'score','system',systems)

