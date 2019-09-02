import csv
import shutil
import index
import lookup
import math
import entropy
reload(index)


def combined(filepath,nrange,syllables='all'):
    ldict={}
    for n in range(nrange[0],nrange[1]):
        ldict[n]=[]
    string=index.get_data_string(filepath)
    data_list=string.split('/')
    if syllables=='all':
        syllables=[]
        for item in data_list:
            for char in item:
                if char not in syllables:
                    syllables.append(char)
    #print(data_list)
    #print(len(data_list))
    metadict={}
    for i in range(0,len(data_list)):
        #print(i)
        result=[] 
        held_out_list=[]
        for item in data_list:
            held_out_list.append(item)
        held_out_list.remove(held_out_list[i])
        print('calculating entropy for song '+str(i+1)+' of '+str(len(data_list)))
        held_out_string='/'.join(held_out_list)
        for n in range(nrange[0],nrange[1]):
            dct=entropy.p_to_ent(held_out_string,[nrange[0],n+1])
            look=lookup.lookup(dct,data_list[i])
            for ktem in look:
                #print('ktem='+str(ktem))
                if ktem[0][-2] in syllables:
                    ldict[len(ktem[0])].append(ktem[1][0])
        i+=1
    avdict={}
    for key,value in ldict.items():
        probs=[]
        #print(len(value))
        for item in value:
            if type(item)==float:
                probs.append(item)
        if len(probs)>0:
            avdict[key]=sum(probs)/len(probs)
        else:
            avdict[key]=0
    with open("./output/p.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in avdict.items():
            row=[]
            row.append(key)
            row.append(value)
            writer.writerow(row)
    return avdict     

def separate(filepath,nrange,syllables='all'):
    result={}
    string=index.get_data_string(filepath)
    data_list=string.split('/')
    if syllables=='all':
        syllables=[]
        for item in data_list:
            for char in item:
                if char not in syllables:
                    syllables.append(char)
    for syllable in syllables:
        print('syllable: '+syllable)
        avdict=p(filepath,nrange,[syllable])
        result[syllable]=avdict
    with open("./output/p.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in result.items():
            row=[]
            row.append(key)
            for jey,ualue in value.items():
                row.append(ualue)
            writer.writerow(row)
    return result

'''for item,value in ldict:
        avg_dict[item]=sum(ldict[item])'''

''' for item in lookup_list:
            result.append(item[1][0])
        metametadict[i]=metadict

    for i in range(0,len(data_list)):
        lookup_list_i=result.append(lookup.lookup(metametadict[i],held_out_list[i]))
        for item in lookup_list:
            result.append(item[1][0])
    return sum(result)/len(result)'''

def avg_p(filepath,nrange):
    avgdict={}
    idct={}
    pr=p(filepath,nrange)
    #print(pr)
    for i in range(nrange[0],nrange[1]):
        ilist=[]
        for key,value in pr.items():
            if key==i:
                #print('value:'+str(value))
                for jey,ualue in value.items():
                    for iey,talue in ualue.items():
                        ilist.append(talue[0])
        idct[i]=sum(ilist)/len(ilist)
    return idct