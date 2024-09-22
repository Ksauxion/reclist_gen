from utils import *


def main(config):
    #config='config.yaml'
    vowels,consonants,restrictions,generate_cv,generate_vc,generate_vv,generate_cc,generate_cr,generate_vcv,max_mora,min_mora,max_consonants,splitter=read_yaml(config)
    reclist=[]

    if generate_vv:
        reclist.extend(gen_vv(vowels,restrictions,max_mora,min_mora))

    if generate_cv and generate_vc and not generate_vcv:
        reclist.extend(gen_cvcvc(consonants,vowels,generate_cr,restrictions,2,1))
    elif generate_cv and generate_vc and generate_vcv:
        reclist.extend(gen_cvcvc(consonants,vowels,generate_cr,restrictions,max_mora,min_mora))
    elif generate_cv and not generate_vc:
        reclist.extend(gen_cvcvc(consonants,vowels,False,restrictions,1,1))
    elif not generate_cv and generate_vc:
        reclist.extend(gen_cvcvc(consonants,vowels,False,restrictions,1,1)[::-1])
    if generate_cc:
        reclist.extend(gen_cc(consonants,vowels,restrictions,max_consonants,generate_cr,max_mora,min_mora))
    
    reclist=append_sil(reclist)
    reclist=delete_no_exc(reclist,generate_vcv,vowels,consonants)
    #reclist.sort()

    filename=config.replace('.yaml','_reclist.txt')
    write_reclist(reclist,filename,splitter)

if __name__=='__main__':
    main()