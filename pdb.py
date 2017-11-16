import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor

def get_donars(arr_h,refe1,arr):
    point_tree = spatial.cKDTree(arr)
    li_a={}
    for i in range (len(arr_h)):
        li1=(point_tree.query_ball_point(arr_h[i], 1.5))
        li_a[i]=refe1[li1[0]]
    return li_a

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if len(l_)==0 or l_.isdigit():
        chain='backbone'
    else:
        chain='side_chain' 
    return chain

def data_extraction(path1,path2):
    file1,file2=open(path1,'r'),open(path2,'r')
    list1,list2=file1.readlines(),file2.readlines()
    file1.close()
    file2.close()
    l=0
    d={}
    d['file_xyz']=path2.split('/')[-1]
    d['file_pdb']=path1.split('/')[-1]
    n_heavy_pdb,n_light_pdb=0,0
    for line in list1:
        if "TER" in line.split()[0]:
            break
        if 'ATOM' in line.split()[0]:
            #print line
            id,at,rt,_,_0,x,y,z,_2,_3,s=line.strip().split()[1:]
            d[int(id)]=[at,rt,s,chain(s,at),_0]
            l+=1
            if s=='H':
                n_light_pdb+=1
            else:
                n_heavy_pdb+=1

    refe_h,refe_d,ref_all={},{},1
    refe1,r1,r2={},0,0
    arr,arr_h,arr_a=[],[],[]
    ref=1
    refe_a,ra={},0
    coord={}
    for line in list2:
        if len(line.strip().split())==0:
            continue
        s,x,y,z=line.strip().split()
        if s!='H':
            #print 'hd'
            ref_ad=ref 
            while ref_ad<l:
                if d[ref_ad][2]==s:
                    break
                ref_ad+=1
            if s in ['O','N','F']:
                #print d[ref_ad][2],s,ref_ad
                refe_a[ra]=ref_ad 
                refe_d[ref_ad]=ref_all
                ra+=1
                arr_a.append([float(x),float(y),float(z)])
            refe1[r1]=ref_ad 
            r1+=1
            arr.append([float(x),float(y),float(z)])
            ref=ref_ad+1
        elif s=='H':
            refe_h[r2]=ref_all
            r2+=1
            arr_h.append([float(x),float(y),float(z)])  
        coord[ref_all]=[float(x),float(y),float(z)]
        ref_all+=1
    
    donars=get_donars(arr_h,refe1,arr)

    return d,donars,arr_a,arr_h,refe_a,refe_h,n_heavy_pdb,n_light_pdb,r1,r2,refe_d,coord

#return [index from array donars,[index for hydrogens,...]]
def result(arr1,arr2,mi,ma):
    points = arr2
    if len(arr2)==0:
        raise Exception("There are no hydrogen atoms !!")
    point_tree = spatial.cKDTree(points)
    li1,li2=[],[]
    res=[]
    for i in range (len(arr1)):
        #print i
        li1=(point_tree.query_ball_point(arr1[i], ma))
        li2=(point_tree.query_ball_point(arr1[i], mi))
        res.append([i,list(set(li1)-set(li2))])
    return res

#returns [donar id,[(hydrogen id,acceptor id),....]]
def output(data):
    d,donars,arr_a,arr_h,refe_a,refe_h,n_heavy_pdb,n_light_pdb,n_heavy,n_light,refe_d,coord=data 
    res=result(arr_a,arr_h,1.6,2.4)
    lis=[]
    h_count=0
    for i in res:
        a=i[0]
        a_id=refe_a[a]
        li=[]
        for j in i[1]:
            h_id=refe_h[j]
            d_id=donars[j]
            if d[d_id][2] in ['O','N','F']:
                h_count+=1
            li.append((h_id,d_id))
        lis.append([a_id,li]) 
    return [lis,[n_heavy_pdb,n_light_pdb,n_heavy,n_light,h_count,refe_d,coord]]

def write_o(out,d):
    file=open('output.txt','w')
    file.write('\n\n          ======================================================================\n')
    file.write('          ==                Possible number of hydrogen bonds :               ==\n')
    file.write('          ==                        Program H_BondCalc                        ==\n')
    file.write('          ==                                                                  ==\n')
    file.write('          ==                         Code version 1.0                         ==\n')
    file.write('          ==                            Niraj Verma                           ==\n')
    file.write('          ==    Computational and Theoretical Chemistry Group (CATCO), SMU    ==\n')
    file.write('          ==                     Dallas, Texas 75275 USA                      ==\n')
    file.write('          ======================================================================\n')
    file.write('\n'*2)
    n_heavy_pdb,n_light_pdb,n_heavy,n_light,h_count,refe_d,coord=out[1]
    file.write("Filename : "+d['file_xyz']+'\n')
    file.write("Total number of heavy atoms : "+str(n_heavy)+'\n')
    file.write("Total number of light atoms : "+str(n_light)+'\n\n')
    file.write("Filename : "+d['file_pdb']+'\n')
    file.write("Total number of heavy atoms : "+str(n_heavy_pdb)+'\n')
    file.write("Total number of light atoms : "+str(n_light_pdb)+'\n\n')
    file.write("Number of hydrogen bonds possible : "+str(h_count)+'\n\n')
    file.write('File format : \nDonarResidueId donarResidueType donarChain donarSymbol donarAtomId, HydrogenAtomId, acceptorAtomId acceptorResidueId acceptorResidueType, acceptorChain acceptorSymbol (acceptorAtomId, hydrogenAtomId) D-H...A hydrogenBondLength \n\n')
    st=''
    count=0
    st_d,b_d={},{}
    for item in out[0]:
        a,b=item
        li1=[str(refe_d[a]),'[',str(d[a][4]),']',d[a][1],d[a][3],d[a][2]] 
        li1_test="{:>4} {}{:>3}{} {:>4} {:>13} {:>2}".format(*li1)
        for i in b:
            j,k=i 
            hid=str(j)
            if d[k][2] not in ['O','N','F']:
                continue
            count+=1
            c=d[k][3]+'-'+d[a][3]
            li2=['[',str(d[k][4]),']',d[k][1],d[k][3],d[k][2],str(refe_d[k])]
            li2_test="{}{:>3}{} {:>4} {:>13} {:>2} {:>4}".format(*li2)
            est=[str(refe_d[a]),hid]
            dist=str(round_sig(distance(coord[int(hid)],coord[refe_d[a]]),5))
            lis_test=str(count)+'.',li2_test,hid,li1_test,str(refe_d[a]),hid,d[k][2]+'-H...'+d[a][2],dist+'\n'
            st_test="{:>4}  {:>30} ,{:>4} ,{:>24} ({:>4} ,{:>4}) {:>8}  {:>6}".format(*lis_test)
            st0=st_test
            db=d[k][2]+'-H...'+d[a][2]
            if c not in st_d:
                st_d[c]=[st0]
            else:
                st_d[c].append(st0)
            if db not in b_d:
                b_d[db]=[st0]
            else:
                b_d[db].append(st0)
            file.write(st0)
            #st+=str(count)+'.'+' '*(5-(len(str(count))))+d[k][2]+'-H...'+d[a][2]+'   '+d[k][3]+'...'+d[a][3]+'\n'
    
    file.write('\n')
    file.write("Additional : \n\n")
    for string in st_d:
        file.write(string+' N = '+str(len(st_d[string]))+'\n'+''.join(st_d[string])+'\n\n')
    for string in b_d:
        file.write(string+'    N = '+str(len(b_d[string]))+'\n'+''.join(b_d[string])+'\n\n')
    #file.write(st+'\n\n')
    file.write("...Termination of the program ....")
    file.close()


data=data_extraction('/Users/47510753/Downloads/for-niraj/1l2y.pdb','/Users/47510753/Downloads/for-niraj/for-script.com')
out=output(data)
write_o(out,data[0])





