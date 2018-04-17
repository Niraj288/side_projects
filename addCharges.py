#!/usr/bin/python
import xlwt
import module
import sys
#import xlrd
#from xlutils.copy import copy as xl_copy

#metals=['Co','Rh','Ni','Pd','Pt','Ir','I']

def func(path,keyword,ref,d,n):
        filename=path
        file =open(filename,'r')
        lines=file.readlines()
        file.close()

        for line in lines:
                if 'Total' in line:
                        continue
                li=line.strip().split()
                try:
                        int(li[0][-1])
                        j=0
                        while j<len(li):
                                try:
                                        int(li[0][j])
                                        nam,id,charge =li[0][:j],li[0][j:].strip(),li[1]
                                        break
                                except ValueError:
                                        j+=1
                except ValueError:
                        nam,id,charge=li[0],li[1],li[2]
                d[id]=charge

def get_ids(path,suffix,d):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lm={}
        length=0
        for line in lines:
                i+=1
                if ref==5:
                        break
                if 'File format' in line:
                        ref+=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2:
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', DensityCriticalPointAcceptor \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        st=[d[l[0].strip()],d[l[1].strip()]]

                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm 

def addC(path,p_id):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lm={}
        length=0
        for line in lines:
                i+=1
                if ref==5:
                        break
                if 'File format' in line:
                        ref+=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2:
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', AcceptorCharge, H_Charge \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        try:
                                float(p_id[str(i2+1)+'.'][0])
                                lm[str(i2+1)+'.']=' '.join(p_id[str(i2+1)+'.'])
                        except ValueError:
                                lm[str(i2+1)+'.']='None'
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        j=0
        length+=1
        for line in lines:
                if len(line.strip().split())==0:
                        j+=1
                        continue
                if line.strip().split()[0] in lm:
                        string=lm[line.strip().split()[0]]
                        lines[j]=lines[j][:-1]+' '*(length-len(lines[j])+2)+string+'\n' 
                j+=1
        g=open(path,'w')
        g.write(''.join(lines))
        g.close()


def job(filename):
        ref=0
        d={}
        n=0
        
        path=filename+'.nbo'#raw_input("Enter .sum path : ")
        func(path,'BCP',ref,d,n)
        txt_path=filename+'.txt'#raw_input("Enter .txt path : ")
        p_id=get_ids(txt_path,'_ah',d)     
        #print p_id	
        addC(txt_path,p_id)

if __name__=='__main__':
        job(sys.argv[1].split('.')[0])






