import os
import sys
import numpy as np

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 


def get_I(ref,lines):
        li=[]
        for i in range (ref,len(lines)):
                if '***' in lines[i] or 'Entering OneElI..' in lines[i]:
                        break
                if 'D' in lines[i]:
                        st=lines[i].replace('D','E')
                        #print st
                        li+=map(float,st.split()[1:])
        return li

def data(path):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        d={'KE':[],'PE':[],'Ov':[]}
        ref=0
        for line in lines:
                if '*** Overlap ***' in line:
                        d['Ov']=get_I(ref+1,lines)
                if '*** Kinetic Energy ***' in line:
                        d['KE']=get_I(ref+1,lines)
                if '**** Potential Energy ****' in line:
                        d['PE']=get_I(ref+1,lines)
                ref+=1
        return d

if __name__=="__main__":
        final_dict={'FD':[]}
        ref=0
        total=7165
        for i in os.listdir('.'):
                if i[-4:]=='.out':
                        final_dict['FD'].append(data(i))
             	progress(ref, total, status='Doing very long job')
             	ref+=1
        #print final_dict
        np.save('/users/nirajv/data/katja_integrals.npy',final_dict)

