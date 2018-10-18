import os
import sys 
import math
import matplotlib.pyplot as plt
import numpy as np
import atom_data

class data:
    def __init__(self,file):
        self.file=file 
        self.F,self.g,self.cc,self.s,self.E,self.atoms=self.load() 
        self.num=len(self.atoms)
        self.sym = atom_data.data(sys.argv[0])

    def extract_coord(self,line):
        lis=[]
        st=''
        ref=0
        count=0
        line=line.replace('D','E')
        for i in line:
                if i==' ':
                        if len(st)!=0:
                                lis.append(st)
                        st=''
                elif i=='-' and line[count-1]!='E':
                        if len(st)!=0:
                                lis.append(st)
                        st='-'
                else:
                        st+=i
                count+=1
        if len(lis)<3:
                lis.append(st)
        lis=map(float,lis)
        return lis

    def load(self):
        f=open(self.file,'r')
        lines=f.readlines()
        f.close()

        K,g,coord,s,E,atoms=[],[],[],[],[],[]
        var=-1
        ref=0
        for line in lines:
            if 'BL,Alpha,Beta' in line or 'FX_ZMat_Orientation' in line or 'FFX_ZMat_Orientation' in line or 'IPoCou,' in line or 'END' in line:
                ref=2
            if ref==3:
                st=line.strip()
                if var==0:
                    coord+=self.extract_coord(st)
                elif var==1:
                    g+=self.extract_coord(st)
                else:
                    K+=self.extract_coord(st)
            if ref==1 and 'BL,Alpha,Beta' not in line:
                atoms.append(line.strip().split()[0])
            if ref==4:
                line=line.replace('D','E')
                kl=line.strip().split()
                s.append(float(kl[-1]))
                E.append(float(kl[1]))
            if 'CC'==line.strip().split()[0]:
                ref=3
                var=0
            if 'FX_ZMat_Orientation'==line.strip().split()[0]:
                ref=3
                var=1
            if 'FFX_ZMat_Orientation'==line.strip().split()[0]:
                ref=3
                var=2
            if 'XXIRC' in line:
                ref=4
            if 'IAnZ' in line and ref==0:
                ref=1

        # Mass weighting for coord and gradients
        mass_dict=atom_data.data(sys.argv[0])
        for i in range (0,len(coord),len(atoms)*3):
            for j in range (len(atoms)):
                for k in range (3):
                    mi=math.sqrt(float(mass_dict[int(atoms[j])]['atomicMass'][:5]))
                    coord[i+j+k]=mi*coord[i+j+k]
                    g[i+j+k]=mi*g[i+j+k]
        g=np.array(g).reshape((len(s),len(atoms)*3))
        coord=np.array(coord).reshape((len(s),len(atoms)*3))

        #extract hessian from lower triangular form 
        h_dic={}
        ref=0
        for i in range (len(s)):
            for j in range (3*len(atoms)):
                for k in range (j+1):
                    mj=math.sqrt(float(mass_dict[int(atoms[j/3])]['atomicMass'][:5]))
                    mk=math.sqrt(float(mass_dict[int(atoms[k/3])]['atomicMass'][:5]))
                    val=K[ref]/(mj*mk)
                    h_dic[(i,j,k)]=val
                    h_dic[(i,k,j)]=val
                    ref+=1

        # Mass weighting hessian
        F=[]
        for i in range (len(s)):
            F.append([])
            for j in range (3*len(atoms)):
                F[-1].append([])
                for k in range (3*len(atoms)):
                    F[-1][-1].append(h_dic[(i,j,k)])
        
        F=np.array(F)
        
        return F,g,coord,s,E,atoms  
    
    # curvature
    def vector_k(self):
        cc=np.array(self.cc).flatten()
        lis=[]
        for i in range (self.num*3):
            lis.append([]) 
        for i in range (0,len(cc),self.num*3):
            for j in range (self.num*3):
                lis[j].append(cc[i+j])
        k=[]
        for li in lis:
            g1=np.gradient(li,self.s)
            g2=np.gradient(g1,self.s)
            #g2=np.gradient(g2,self.s)
            #g2=np.gradient(g2,self.s)
            k.append(g2)
        return k

    # Scalar curvature
    def scalar_k(self):
        lis=[]
        vk=self.vector_k()
        for i in range (len(self.s)):
            li=[]
            for j in range (self.num*3):
                li.append(vk[j][i])
            lis.append(np.linalg.norm(li))
        return np.array(lis)

    # analytical reaction path vector
    def a_vector_n(self):
        n=[]
        for i in self.g:
            c=np.linalg.norm(i)
            n.append(i) #i/c for unit vector
        return n 

    # scalar from analytical path vector
    def a_scalar_n(self):
        ns=[]
        n_lis=self.a_vector_n() 
        ref=0
        for n in n_lis:
            if self.s[ref]<0:
                ns.append(-np.linalg.norm(n))
            else:
                ns.append(np.linalg.norm(n))
            ref+=1
        return ns 

    #reaction path vector
    def vector_n(self):
        lis=[]
        for i in range (self.num*3):
            lis.append([]) 
        for i in range (0,len(self.cc),self.num*3):
            for j in range (self.num*3):
                lis[j].append(self.cc[i])
        k=[]
        for li in lis:
            g1=np.gradient(li,self.s)
            k.append(g1)
        return k

    def scalar_n(self):
        lis=[]
        vk=self.vector_n()
        for i in range (len(self.s)):
            li=[]
            for j in range (self.num*3):
                li.append(vk[j][i])
            lis.append(np.linalg.norm(li))
        return np.array(lis)

    def make_xyz(self):
        f = open(self.file.split('.')[0]+'.xyz','w')
        for i in range (len(self.cc)):
            f.write(str(len(self.atoms))+'\n')
            f.write(str(self.s[i])+'\n')
            for j in range (0,len(self.cc[i]),3):
                st = self.sym[int(self.atoms[j/3])]['symbol']+' '+' '.join(map(str,self.cc[i][j:j+3]))+'\n'
                f.write(st)
        f.close()

        


if __name__=='__main__':
    d=data(sys.argv[1])
    d.make_xyz()

        
