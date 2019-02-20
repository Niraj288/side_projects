import time
import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
from scipy import interpolate
import os
import sys
from numba import jit

def get_donars(arr_h,refe1,arr):
    point_tree = spatial.cKDTree(arr)
    li_a={}
    for i in range (len(arr_h)):
        li1=(point_tree.query_ball_point(arr_h[i], 1.5))
        if len(li1)==0:
            pass
        else:
            li_a[i]=refe1[li1[0]]
    return li_a

def angle(a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def distance(a,b):
    a = map(float, a)
    b = map(float, b)
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def cartoon(point, li0, d, n = 2):
    #print self.get_backbone()
    if d[point][3] != 'backbone':
        return None 
    
    ind = li0.index(point)
    fli = []

    count = 0
    c1, c2 = 0, 0
    while len(fli) < n+1:
        if d[li0[ind+count]][2] == 'C':
            fli.append(li0[ind+count])
        count += 1
        if ind+count >= len(li0): 
            break
    c1 = count

    count = 1
    while len(fli) < 2*n+1:
        d[li0[ind-count]][2]
        if d[li0[ind-count]][2] == 'C':
            fli.append(li0[ind-count])
        count+=1
        if ind-count <= 0:
            c2 = 2*n+1 - len(fli)
            break

    if c2:
        count = c1
        while len(fli) < 2*n+1:
            if d[li0[ind+count]][2] == 'C':
                fli.append(li0[ind+count])
            count += 1
            if ind+count >= len(li0):
                break




    fli.sort()
    #print fli
    coord = [map(float,d[i][-3:]) for i in fli]
    coord = np.array(coord)
    x,y,z = coord[:,0],coord[:,1],coord[:,2]
    try:
        tck, u = interpolate.splprep([x,y,z], s=3)
    except ValueError:
        return None
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0,1,len(coord)*10)

    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    coord_fine = []

    for i in range (len(x_fine)):
        coord_fine.append([x_fine[i],y_fine[i],z_fine[i]])

    coord_fine = np.array(coord_fine)

    '''
    fig2 = plt.figure(2)
    ax3d = fig2.add_subplot(111, projection='3d')
    ax3d.plot(x, y, z, 'r*')
    #ax3d.plot(x_knots, y_knots, z_knots, 'go')
    ax3d.plot(x_fine, y_fine, z_fine, 'g-')

    fig2.show()
    plt.show()
    '''

    #print fli
    #self.check_cartoon(fli)

    dis = 0
    for i in range (1,len(coord_fine)-1):
        #print self.d[fli[i]][-3:],self.d[fli[i-1]][-3:]
        dis += distance(coord_fine[i],coord_fine[i-1])

    #print dis, distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    res = dis/distance(d[fli[0]][-3:], d[fli[-1]][-3:])

    return res


def check_cartoon(point, li0, d):
    res1 = cartoon(point, li0, d)
    if not res1:
        return None
    res2 = cartoon(point, li0, d, 5)

    #print res1, res2

    if res1 < 1.18 and res2 < 1.2:
        return 'Beta'
    elif res1 < 1.18 and res2 > 1.2:
        return 'Coil' 
    elif res1 < 2.0 and res2 < 2.5:
        return 'Alpha'
    elif res2 > 2.5:
        return 'Sharp Turn' 

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if len(l_)==0 or l_.isdigit() or l_ == 'A':
        chain='backbone'
    else:
        chain='side_chain' 
    return chain

def get_backbone(d):
    li = []
    for i in d:
        if d[i][3] == 'backbone':# and self.d[i][2]!='H':
            li.append(i)
    #print li
    return li

def check_alpha(d, li0):
    
    for i in d:
        if d[i][3] != 'backbone' or d[i][2] == 'H':
            continue
        else:
            ct = check_cartoon(i, li0, d)
            if ct:
                d[i][3] = ct
    return d

@jit
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
        if "END" in line.split()[0]:
            break
        if line.split()[0] in ['ATOM']:
            #print line
            id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
            s=line.strip().split()[-1]
            d[int(id)]=[at,rt,s,chain(s,at),_0, x, y, z]
            l+=1
            if s=='H':
                n_light_pdb+=1
            else:
                n_heavy_pdb+=1

    li0 = get_backbone(d)
    d = check_alpha(d, li0)

    refe_h,refe_d,ref_all={},{},1
    refe1,r1,r2={},0,0
    arr,arr_h,arr_a=[],[],[]
    ref=1
    refe_a,ra={},0
    coord={}
    for line in list2[2:]:
        if len(line.strip().split())<4:
            break
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

@jit(nopython=True, parallel=True)
def query(point_tree, arr_i, l):
    return point_tree.query_ball_point(arr1[i], l)

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
        li1=(query(point_tree, arr1[i], ma))
        li2=(query(point_tree, arr1[i], mi))
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

@jit
def write_o(path1,out,d):
    file=open(path1.split('/')[-1].split('.')[0]+'.txt','w')
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
    file.write("""
Units:
    Hydrogen bond length                Angstron
    Local mode force costant            mDynes/A^2
    H(r)atBCP                           kcal/mol*A^3
    Frequencies                         cm^-1
    LPtoBD*                             kcal/mol
    Charges                             a.u.
    Angles                              Degrees

""")
    file.write('File format : \nDonarResidueId donarResidueType donarChain donarSymbol donarAtomId, HydrogenAtomId, acceptorAtomId acceptorResidueId acceptorResidueType, acceptorChain acceptorSymbol (acceptorAtomId, hydrogenAtomId) D-H...A hydrogenBondLength \n\n')
    st=''
    count=0
    st_d,b_d={},{}
    lm={}
    for item in out[0]:
        a,b=item
        li1=[str(refe_d[a]),'[',str(d[a][4]),']',d[a][1],d[a][3],d[a][2]] 
        li1_test="{:>6} {}{:>6}{} {:>6} {:>15} {:>3}".format(*li1)
        for i in b:
            j,k=i 
            hid=str(j)
            if d[k][2] not in ['O','N','F']:
                continue
            ang = angle(coord[refe_d[k]],coord[int(hid)],coord[refe_d[a]])
            '''
            if ang > 180:
                ang = 360.0 - ang
            if ang < 90.0 :
                continue  
            '''  
            count+=1
            c=d[k][3]+'-'+d[a][3]
            li2=['[',str(d[k][4]),']',d[k][1],d[k][3],d[k][2],str(refe_d[k])]
            li2_test="{}{:>6}{} {:>6} {:>15} {:>3} {:>6}".format(*li2)
            est=[str(refe_d[a]),hid]
            dist=str(round_sig(distance(coord[int(hid)],coord[refe_d[a]]),5))
            lis_test=str(count)+'.',li2_test,hid,li1_test,str(refe_d[a]),hid,d[k][2]+'-H...'+d[a][2],dist+'\n'
            st_test="{:>6}  {:>30} ,{:>6} ,{:>26} ({:>6} ,{:>6}) {:>8}  {:>6}".format(*lis_test)
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
            lm[str(count)+'.']=[d[k][2]+'-H...'+d[a][2],str(refe_d[a])+'-'+hid,dist]
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
    return lm

def make_xyz(path):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    lis=''
    ref=0
    for line in lines:
        if '#p ' in line:
            ref+=1
        if len(line.strip().split())==0:
            ref+=1
        if ref==6:
            break
        if ref==3 or ref==4:
            ref+=1
        if ref==5:
            lis+=line
    g=open(path[:-4]+'.xyz','w')
    g.write(lis)
    g.close()
    return 1

'''
files=os.listdir('.')
path1,path2='',''
for i in files:
    if i[-4:]=='.com':
        make_xyz(i)
files=os.listdir('.')
for i in files:
    if i[-4:]=='.pdb':
        path1=i 
    if i[-4:]=='.xyz':
        path2=i
'''
def job(path1,path2):
    #path1=sys.argv[1]#path1 or raw_input('Enter pdb path : ')
    #path2=sys.argv[2]#path2 or raw_input('Enter xyz path : ')
    t = time.time()
    data=data_extraction(path1,path2)
    out=output(data)
    print 'Time taken is',time.time()-t
    return write_o(path1,out,data[0])





if __name__ == '__main__':
	job(sys.argv[1], sys.argv[2])

