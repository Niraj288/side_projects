import os
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import xlwt
from sklearn import metrics
import math
from sklearn.model_selection import KFold
from sklearn.kernel_ridge import KernelRidge
from sklearn.neural_network import MLPRegressor
from sklearn import preprocessing, cross_validation, neighbors, svm
import random
import sklearn.preprocessing as ps 

def add_data(data):
	pka=np.load('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy').item()
	ne=np.load(data).item()
	lis=[]
	for i in ne:
		pk=float(raw_input("Enter pka for "+i+' : '))
		pka[i.split('/')[-1].split('.')[0]]=pk
		lis.append([pka[i.split('/')[-1].split('.')[0]],pk])
	for k in lis:
		print ' '.join(map(str,k)) 
	if raw_input('save : ')=='y':
		np.save('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy',pka)


def make_excel(data,name,func):
	pr=func(data)
	wb=xlwt.Workbook() 
	sheet = wb.add_sheet('Version1') 
	sheet.write(0,0,'Filename')
	sheet.write(0,1,'Qa1')
	sheet.write(0,2,'Qa2')
	#sheet.write(0,3,'Qw')
	sheet.write(0,4,'pKa')
	sheet.write(0,5,'pKa (predicted)')
	sheet.write(0,6,'Diff')
	row=1
	for i in data:
		col=0
		a,b,d=data[i]
		sheet.write(row,col,i.split('/')[-1])
		sheet.write(row,col+1,float(a[-1]))
		sheet.write(row,col+2,float(b[-1]))
		#sheet.write(row,col+3,float(c[-1]))
		sheet.write(row,col+4,float(d))
		sheet.write(row,col+5,float(pr[row-1][0]))
		sheet.write(row,col+6,float(pr[row-1][0]-float(d)))
		row+=1
	wb.save(name)

def mad(data, axis=None):
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)

def prin2(X_train, y_train, X_test, y_test, file):
	t=100
	#clf = MLPRegressor()#solver=dic['solver'],activation=dic['activation'],hidden_layer_sizes=eval(dic['hls']), batch_size = dic['batch_size'], max_iter=dic['max_iter'])
	clf = LinearRegression()
	#clf=svm.SVR()
	#clf=KernelRidge(alpha=0.01,kernel='laplacian')
	clf.fit(X_train, y_train)
	
	print 'Training size',len(X_train)
	print 'Testing size',len(X_test)
	#scores = cross_val_score(clf, X, y, cv=5)
	#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

	accuracy = clf.score(X_train,y_train)
	print 'accuracy',accuracy,'\n'
	print 'RMSE',math.sqrt(metrics.mean_squared_error(y_test,clf.predict(X_test)))
	MAE=metrics.mean_absolute_error(y_test,clf.predict(X_test))
	print 'MAE',MAE 
	#X_test,y_test=X[-t:],y[-t:]
	#file=file[-t:]
	pr=clf.predict(X_test)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y_test)):
		if y_test[i]==0.0:
			y_test[i]=0.0000001
		predi=str(round(((pr[i]-y_test[i])/y_test[i])*100,2))+' %'
		print file[i]+' '*(20-len(file[i]))+' '*(20-len(predi))+ predi, ' '*(20-len(str(y_test[i])))+str(y_test[i]) , ' '*(20-len(str(round(pr[i],2))))+str(round(pr[i],2)),' '*(20-len(str(round((y_test[i]-pr[i]),4))))+str(round((y_test[i]-pr[i]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	return MAE

def validate(X,y,file):
        kf = KFold(n_splits=3, random_state=True, shuffle=True )
        ref=0
        for train,test in kf.split(y):
                a=np.array([X[i] for i in train])
                b=np.array([y[i] for i in train])
                c=np.array([X[i] for i in test])
                d=np.array([y[i] for i in test])
                file_t=[file[i] for i in test]
                ref+=prin2(a,b,c,d,file_t)
        print 'cross validation MAE',ref/5
        return ref/5

def prin(X,y,file):
	clf = LinearRegression() #(n_jobs=processors)

	clf.fit(X, y)
	print 'Training size',len(X)
	accuracy = clf.score(X,y)
	print 'accuracy',accuracy,'\n'
	RMSE=math.sqrt(metrics.mean_squared_error(y,clf.predict(X)))
	print 'RMSE',RMSE
	MAE=metrics.mean_absolute_error(y,clf.predict(X))
	print 'MAE',MAE
	MAD=mad(y)
	print 'MAD', MAD
	eqn='pka = '
	for i in range (len(X[0])):
		eqn+=str(clf.coef_[0][i])+'*Q'+str(i+1)+' + '
	eqn+=str(clf.intercept_[0])
	print eqn,'\n'
	pr=clf.predict(X)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y)):
		predi=str(round(((pr[i][0]-y[i][0])/y[i][0])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y[i][0])))+str(y[i][0]) , ' '*(20-len(str(round(pr[i][0],2))))+str(round(pr[i][0],2)),' '*(20-len(str(round((y[i][0]-pr[i][0]),4))))+str(round((y[i][0]-pr[i][0]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	print RMSE,MAE,MAD,clf.coef_[0][3],clf.coef_[0][4],clf.coef_[0][0],clf.coef_[0][1],clf.coef_[0][2],clf.intercept_[0],accuracy
	#return clf 
	return pr



def make_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		#print i,data[i]
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		a1=(float(a[-1])+float(b[-1]))/2
		b1=float(c[-1]) 
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(d)]]
	#validate(X,y,file)
	return prin(X,y,file)
	
def test(data):
	X,y=[],[]
        file=[]
        for i in data:
                file.append(i.split('/')[-1])
                a,b,f=data[i]
                a1,b1=a[-1],b[-1]
                X+=[[b1**2,b1]]
                y+=[[float(f)]]
        prin(X,y,file)

def amide_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		if 0 and i in ['./mol1H.out','./mol2H.out','./mol3H.out','./mol4H.out','./mol15H.out','./mol16H.out','./mol17H.out','./mol18H.out','./mol19H.out']:
			continue
		file.append(i.split('/')[-1])
		a,b,c,d,e,f=data[i]
		a1,b1=b[-1],e[-1]
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(f)]]
	prin(X,y,file)

def get_rand(X,y,t):
	if t==-1:
		return X,y
	random.seed(1286)
	inde= random.sample(range(len(X)),t)
	x1,y1=[],[]
	for i in inde:
		x1.append(X[i])
		y1.append(y[i])
	return x1,y1

def amide_fit2(data):
	X,y=[],[]
	file=[]
	t=70
	for i in data:
		if 0 :#'N24' in i.split('/')[-1] or  'N28' in i.split('/')[-1] or 'N37' in i.split('/')[-1] or 'N58' in i.split('/')[-1]:
			continue
		if data[i][3]>7.8 or data[i][3]<5.0:
			continue
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		a1,b1,c1=a[2],b[2],c[2]
		X+=[[a1**3,b1**3,c1**3,a1**2*b1,b1**2*c1,c1**2*a1,a1*b1**2,b1*c1**2,c1*a1**2,a1*b1,b1*c1,c1*a1,a1,b1,c1]]
		y+=[[float(d)]]
		#y+=[float(d)]
	#X,y=get_rand(X,y,86)
	X=np.array(X)
	y=np.array(y)
	X=ps.scale(X)
	#X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.15)
	#return prin2(X_train, y_train, X_test, y_test, file)
	#return prin2(X[:t],y[:t],X[t:],y[t:],file)
	#return validate(X,y,file)
	return prin(X,y,file)

def phenol_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		if 'N24' in i.split('/')[-1] or  'N28' in i.split('/')[-1] or 'N37' in i.split('/')[-1] or 'N38' in i.split('/')[-1] or 'N25' in i.split('/')[-1]:
			continue
		file.append(i.split('/')[-1])
		a,b,f=data[i]
		a1,b1=a[-1],b[-1]
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(f)]]
	#return prin2(X[:91],y[:91],X[91:],y[91:],file)
	#return validate(X,y,file)
	return prin(X,y,file)

def symm_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		file.append(i.split('/')[-1])
		a,b,c,d,e=data[i]
		a1,b1=(a[-1]+c[-1])/2,(b[-1]+d[-1])/2
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(e)]]
	prin(X,y,file)

def predict(func,data,pred,t):
        print 'Predicting ...\n'
        
        X,y=[],[]
        file=[] 

        known={'mol10H.out':8.32,'mol11H.out':7.25,'mol12H.out':7.19,'mol13H.out':7.55,'mol14H.out':7.65,'mol15H.out':5.62,'mol16H.out':5.69,'mol26H.out':0.0,'mol27H.out':0.0,'mol28H.out':0.0,'mol32H.out':0.0}
                
        for i in data:
                if 'N24' in i.split('/')[-1] or  'N28' in i.split('/')[-1]:# or 'N58_10' in i.split('/')[-1] or 'N58' in i.split('/')[-1]:
                        continue
                if data[i][3]>7.0 or data[i][3]<4.0:
                        continue
                file.append(i.split('/')[-1])
                a,b,c,d=data[i]
                a1,b1,c1=a[2],b[2],c[2]
                X+=[[a1**3,b1**3,c1**3,a1**2*b1,b1**2*c1,c1**2*a1,a1*b1**2,b1*c1**2,c1*a1**2,a1*b1,b1*c1,c1*a1,a1,b1,c1]]
                y+=[[float(d)]]
                #y+=[float(d)]
        file2=[]
        for i in pred:
                file2.append(i.split('/')[-1])
                a,b,c=pred[i]
                a1,b1,c1=a[2],b[2],c[2]
                X+=[[a1**3,b1**3,c1**3,a1**2*b1,b1**2*c1,c1**2*a1,a1*b1**2,b1*c1**2,c1*a1**2,a1*b1,b1*c1,c1*a1,a1,b1,c1]]
                #X,y=get_rand(X,y,86)
        X=np.array(X)
        y=np.array(y)
        #X=ps.scale(X)
        clf=prin(X[:-t],y,file)
        pr=clf.predict(X[-t:])
        for i in range (len(file2)):
                print file2[i]+' '*(20-len(file2)),"{:>15} {:>15} {:>15}".format(*[str(pr[i][0])[:4],known[file2[i]],str(pr[i][0]-known[file2[i]])[:5]])
                #X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.15)
                #return prin2(X_train, y_train, X_test, y_test, file)
                #return prin2(X[:t],y[:t],X[t:],y[t:],file)
                #return validate(X,y,file)
                #return prin(X,y,file)

def calc(data):
        name_c={'-a2':amide_fit2,'-r':phenol_fit,'-a':amide_fit,'-p':phenol_fit,'-m':make_fit,'-s':symm_fit,'-t':test}
        pka=np.load('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy').item()
        d=np.load(data).item()
        rm_lis=[]
        ref=0
        #print d
        tu=[]
        pred={}
        for i in pka:
        	if 'mol' in i:
        		tu.append(i)
        for i in tu:
        	del pka[i]
        for i in d:
                if len(d[i])==4:
                        break
                name=i.split('/')[-1].split('.')[0]
                try:
                        d[i]=d[i]+[pka[name]]
                except KeyError:
                        ref=1
                        pk='p' or raw_input('Enter pka for '+i+' : ')

                        if len(pk)==0:
                                rm_lis.append(i)
                        elif pk=='p':
                                rm_lis.append(i)
                                pred[i]=d[i]
                        else:
                                pka[name]=float(pk)
                                d[i]=d[i]+[pka[name]]
        for i in rm_lis:
                del d[i]
        if ref:
                if 0:#raw_input('Save data : ')=='y':
                        np.save('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy',pka)
        if len(pred)!=0:
	        t=len(pred)
	        predict(name_c[sys.argv[2]],d,pred,t)
	        return
        if len(sys.argv)>2:
                name_c[sys.argv[2]](d)
        else:
                make_fit(d)

                #amide_fit(d)
                #make_fit(d)
                #phenol_fit(d)
                #test(d)
                #symm_fit(d)
        make_excel(d,data.split('/')[-1].split('.')[0]+'.xls',name_c[sys.argv[2]])#make_fit)

calc(sys.argv[1])
#add_data(sys.argv[1])









