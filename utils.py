

def replace_subsequence(lst, subseq, replacement):
    i = 0
    while i <= len(lst) - len(subseq):
        # Check if the subsequence matches
        if lst[i:i + len(subseq)] == subseq:
            # Replace the subsequence with the replacement
            lst[i:i + len(subseq)] = replacement
            # Adjust index to skip over the replaced subsequence
            i += len(replacement) - 1
        else:
            i += 1
    return lst


def delete_restr(restr,seq):
    for i in restr:
        replace_subsequence(seq,i,i[-1])
    return seq



def split_seq(seq, len_subseq, min_len_subseq,overlap=1):
    len_seq = len(seq)
    seqs = []
    curr_id = 0
    while curr_id < len_seq:
        end_id = min(curr_id + len_subseq, len_seq)
        seqs.append(seq[curr_id:end_id])
        curr_id += len_subseq - overlap
    while len(seqs[-1]) < min_len_subseq:
        needed_elements = min_len_subseq - len(seqs[-1])
        seqs[-1] = seqs[-2][-needed_elements-1:-1] + seqs[-1]

    return seqs

def flatten(xss):
    return [x for xs in xss for x in xs]



def gen_cvcvc_line(c,vs,cons,max_mora,min_mora):
    p=[]
    blob=[c,vs[0]]
    p.append(blob)
    for i in vs:
        blob=[c,i]
        p.append(blob)
    p=split_seq(p,max_mora,min_mora)
    for i in range(len(p)):
        p[i]=flatten(p[i])
    if cons:
        for i in range(len(p)):
            p[i].append(c)
    return p

def gen_cvcvc(c,vs,cons,restr,max_mora,min_mora):
    gl=[]
    for cc in c:
        curr_c=[]
        for vn in range(len(vs)):
            l=vs[vn:]
            l2=vs[:vn]
            l.extend(l2) #new vowel list
            curr_c.extend(gen_cvcvc_line(cc,l,cons,max_mora,min_mora))
        gl.extend(curr_c)
    for i in range(len(gl)):
        gl[i]=delete_restr(restr,gl[i])
    return gl

def gen_vv(vs,restr,max_mora,min_mora):
    gl=[]
    for vn in range(len(vs)):
        l=vs[vn:]
        l2=vs[:vn]
        l.extend(l2) #new vowel list
        p=[l[0]]
        p.append(l[0])
        for i in l[1:]:
            p.append(i)
            p.append(l[0])
        p=split_seq(p,max_mora,min_mora)
        #p=flatten(p)
        gl.append(p)
    gl=flatten(gl)
    for i in range(len(gl)):
        gl[i]=delete_restr(restr,gl[i])
    return(gl)

#print(gen_vv(vw))
#gen_cvcvc(cn,vw,True)
from itertools import *


def count_clusters(seq,vw):
    for i in range(len(seq)):
        if seq[i] in vw:
            seq[i]=vw[0]
    seq=flatten(seq)
    seq=' '.join(seq)
    seq=seq.split(vw[0])
    clusters=[]
    for i in seq:
        i=i.rstrip()
        i=i.rsplit()
        if len(i)>1 and not clusters.__contains__(i):
            clusters.append(i)
    return clusters
from itertools import product

def gen_cc(c:list,vs,restr,len_clusters,cons,max_mora,min_mora):
    a=product(c,repeat=len_clusters)
    a=list(set((a)))
    for i in range(len(a)):
        a[i]=list(a[i])
        #print(a[i])
    #print(a)
    gl=[]
    clusters=[]
    for cluster in a:
        if not clusters.__contains__(cluster):
            ln=[]
            syl0=[cluster[0],vs[0]]
            ccv=1
            #while syl0 in restr:
            while restr.__contains__(syl0):
                if ccv<len(vs):
                    syl0=[cluster[0],vs[ccv]]
                    ccv+=1
                else:
                    syl0=[vs[ccv]]
            #print(syl0)
            syl1=[cluster[-1],vs[0]]
            ccv=1
            #while syl0 in restr:
            while restr.__contains__(syl1):
                if ccv<len(vs):
                    syl1=[cluster[-1],vs[ccv]]
                    ccv+=1
                else:
                    syl1=['Sil',vs[ccv]]
            ln.extend(syl0)
            ln.extend(cluster)
            ln.extend(syl1[1:])
            #print(ln,ln[1:3])
            u=ln[1:3]
            ccv=0
            while restr.__contains__(u):
                if ccv<len(vs):
                    u=[vs[ccv],u[-1]]
                    ccv+=1
                else:
                    u=['Sil']
            l1=ln[:1]
            l2=ln[3:]
            ln=[]
            ln.extend(l1)
            ln.extend(u)
            ln.extend(l2)
            #print(cluster[-1])
            if cons:
                ln.append(cluster[-1])
            #print(ln)
            #ln0=' '.join(ln).split(' '.join(cluster)) #!!!
            #print(ln)
            ln0=[ln[:2],ln[2+len_clusters:]]
            #print(ln0)
            #ln0[0],ln0[1]=ln0[0].rstrip().rsplit(),ln0[1].rstrip().rsplit()
            #print(ln0)
            ln0[0].extend(cluster[:-1])
            ln1=[cluster[-1]]
            ln1.extend(ln0[1])
            ln0[1]=ln1
            if ln0[0]==ln0[1]:
                gl.append(ln0[0])
            else:
                gl.append(ln0[0])
                
                gl.append(ln0[1])
            clusters=count_clusters(gl,vs)
    #gl=flatten(gl)
    #print(gl)
    gl=split_seq(gl,max_mora,min_mora)
    for i in range(len(gl)):
        gl[i]=flatten(gl[i])
    return gl

def append_sil(reclist):
    l=[]
    for i in reclist:
        ln=['Sil']
        ln.extend(i)
        ln.extend(['Sil'])
        l.append(ln)
    return l

def delete_db_list(seq):
    l=[]
    for i in seq:
        if i not in l:
            l.append(i)
    return l

def gen_articulations(reclist,tr,vw,cn):
    di=[]
    for i in reclist:
        for j in range(1,len(i)):
            di.append([i[j-1],i[j]])
    if tr:
        tri=[]
        for i in reclist:
            for j in range(2,len(i)):
                if (((i[j-2] in vw or i[j-2] == 'Sil') and (i[j] in vw or i[j] == 'Sil')) or (i[j-2] in cn and i[j-1] in cn and i[j] in cn)) and (i[j-1] in cn):
                    tri.append([i[j-2],i[j-1],i[j]])
        di.extend(tri)
    di=delete_db_list(di)
    return di
    
def delete_no_exc(reclist,tr,vw,cn):
    reclist.sort(key=len)
    reclist=reclist[::-1]
    used_art=[]
    reclines=[ ]
    for recline in reclist:
        curr_arts=gen_articulations([recline],tr,vw,cn)
        c=0
        for i in curr_arts:
            if not used_art.__contains__(i):
                used_art.append(i)
                c+=1
        if c>0:
            reclines.append(recline)
    reclines=reclines[::-1]
    return reclines

import yaml

def read_yaml(config):
    with open(config,encoding='utf-8') as f:
        data=yaml.safe_load(f)
    #print(data)
    vowels=data['vowels']
    consonants=data['consonants']
    restrictions=data['restrictions']
    generate_cv=data['generate_cv']
    generate_vc=data['generate_vc']
    generate_vv=data['generate_vv']
    generate_cc=data['generate_cc']
    generate_cr=data['generate_cr']
    generate_vcv=data['generate_vcv']
    max_mora=data['max_mora']
    min_mora=data['min_mora']
    max_consonants=data['max_consonants']
    splitter=data['splitter']

    vowels=list(map(str,vowels))
    consonants=list(map(str,consonants))
    #restrictions=data['restrictions']
    rer=[]
    for i in restrictions:
        #print(i)
        o0=list(i.keys())[0]
        oo=i[o0]
        for j in oo:
            rer.append([o0,j])
        #rer.append([i])
    
    for i in range(len(rer)):
        rer[i]=list(map(str,rer[i]))
    #print(rer)
    restrictions=delete_db_list(rer)
    max_mora=int(max_mora)
    min_mora=int(min_mora)
    max_consonants=int(max_consonants)
    splitter=str(splitter)
    return vowels,consonants,restrictions,generate_cv,generate_vc,generate_vv,generate_cc,generate_cr,generate_vcv,max_mora,min_mora,max_consonants,splitter
read_yaml('config.yaml')
def generate_stats(vw):
    l=[]
    for i in vw:
        l.append([i])
    return l

def write_reclist(reclist,out_file,splitter):
    with open(out_file,'w',encoding='utf-8') as f:
        for i in reclist:
            while i[0]=='Sil':
                i=i[1:]
            while i[-1]=='Sil':
                i=i[:-1]
            f.write(splitter.join(i)+'\n')
            