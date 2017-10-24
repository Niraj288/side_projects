import os
def search_deep(n_path,func,args=[],ref=1):
        if 'Trash' in n_path:
		return
	try:
        for i in os.listdir(n_path):
            if os.path.isdir(n_path+'/'+i):
                search_deep(n_path+'/'+i,func,args,ref)
            else:
				if ref:
                    for j in args:
                        if j==i[-len(j):]:
                        	func(n_path+'/'+i)
				else:
					for j in args:
                        if j in i:
                            func(n_path+'/'+i)
        except OSError:
                 func(n_path)

def zmatrix(file):
    os.system('module load gaussian/g16a')
    filename=file.split('.')[0]+'.com'
    os.systme('newzmat -ixyz -Ozmat -rebuildzmat '+file+' '+filename)
    f=open(filename,'r')
    lines=f.readlines()
    f.close()
    ref=1
    string=''
    var=0
    count=-1
    for line in lines:
        if 'C'==line.strip().split()[0]:
            ref=0
        if ref==0:
            string+=' '.join(line.strip().split(','))+'\n'
            if 'Variables:' in line:
                var=1
            if var==1:
                count+=1
            if count==6:
                var=0
                count=0
                string+=' Constants:\n'
        if len(line.strip().split())==0:
            break
    return string 



            


