import os
import sys
import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import math
from sklearn import metrics
from sklearn import svm
import sklearn.preprocessing as ps 
from sklearn.kernel_ridge import KernelRidge
from sklearn import cross_validation

def get_ids(path,suffix='_ah'):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        i=-1
        i2=0
        ref=0
        lmtr={}
        lmte={}
        fk = {}
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
                        if 'N-H...O' not in line:
                                continue
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        st=[n1+l[0].strip(),'H'+l[1].strip()]
                        fk[str(i2+1)+'.'] = line.strip().split()[-3]
                        if i2==0:
                                length=len(line)
                        if 'I(5)' in line:
                                lmte[str(i2+1)+'.']=st
                        else:
                                lmtr[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        tr,te = [],[]
        ka_tr, ka_te = [], []
        for i in lmtr:

                st1 = '-'.join(lmtr[i])
                a, b = lmtr[i]

                st2 = '-'.join([b,a])
                tr.append(st1)
                tr.append(st2)
                ka_tr.append(fk[i])

        for i in lmte:
                st1 = '-'.join(lmte[i])
                a, b = lmte[i]

                st2 = '-'.join([b,a])
                te.append(st1)
                te.append(st2)
                ka_te.append(fk[i])
        #print ka_te
        return  tr, te, ka_tr, ka_te

def get_data(file):
        df = pd.read_excel(file)
        tr,te,ka_tr,ka_te = get_ids(file.split('.')[0]+'.txt')
        li_tr = []
        for i in df.Bond:
                if i in tr:
                        li_tr.append(True)
                else:
                        li_tr.append(False)
        li_te = []
        for i in df.Bond:
                if i in te:
                        li_te.append(True)
                else:
                        li_te.append(False)
        #'Bond Ellipticity','HessianEigenValue0','HessianEigenValue1','HessianEigenValue2', 'G'
        df.drop(columns = ['Bond', 'Comments', 'V', 'K', 'L'], inplace = True)
        df_tr = df[li_tr]
        df_te = df[li_te]
        X_train = df_tr.values
        y_train = np.array(map(float,ka_tr))

        X_test = df_te.values
        y_test = np.array(map(float,ka_te))

        return X_train, X_test, y_train, y_test

def prin(X,y,X_test, y_test):
        #clf = LinearRegression() #(n_jobs=processors)
        clf = svm.SVR()
        #clf=KernelRidge(alpha=0.01,kernel='laplacian',degree=18)

        clf.fit(X, y)
        print 'Training size',len(X)
        accuracy = clf.score(X,y)
        print 'Accuracy on train',accuracy,'\n'
        RMSE=math.sqrt(metrics.mean_squared_error(y,clf.predict(X)))
        print 'RMSE',RMSE
        MAE=metrics.mean_absolute_error(y,clf.predict(X))
        print 'MAE',MAE

        accuracy = clf.score(X_test,y_test)
        print 'Accuracy on test',accuracy,'\n'


X_train, X_test, y_train, y_test = [], [], [], []
for i in os.listdir('.'):
        if i[-4:] == '.xls':
                x_tr, x_te, ytr, yte = get_data(i)
                X_train+= list(x_tr) 
                X_test += list(x_te) 
                y_train += list(ytr) 
                y_test += list(yte) 


X_train, X_test, y_train, y_test = map(np.array,[X_train, X_test, y_train, y_test ])

X_train = ps.scale(X_train)

print X_train.shape, y_train.shape, X_test.shape, y_test.shape

X_train, X_test, y_train, y_test= cross_validation.train_test_split(X_train,y_train,test_size=0.20)

prin(X_train, y_train, X_test, y_test)























