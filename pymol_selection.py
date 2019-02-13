#pymol code

from pymol import cmd
import os
import sys

def func(filename):
        
        file =open(filename,'r')
        lines=file.readlines()
        file.close()

        data = []
        for i in range (2,len(lines)):
                data+=[map(float,lines[i].strip().split()[1:])]

        
        return data

def get_avg(a,b):
	x1, y1, z1 = map(float,a) 
	x2, y2, z2 = map(float,b)
	return (x1+x2)/2, (y1+y2)/2, (z1+z2)/2

# name your bond here
def get_label_from_excel():
	path = '/Users/47510753/Documents/HB-I/excel_files/pymol_raw.txt'
	f = open(path, 'r')
	lines = f.readlines()
	f.close()

	sn, fi, co = [], [], []
	for line in lines:
		l = line.strip().split()
		sn.append(l[2])
		fi.append(l[-3])
		co.append(l[-1])

	d = {}
	for i in range (len(sn)):
		print str(sn[i])+fi[i][:4]
		d[str(sn[i])+fi[i][:4]] = co[i]

	#print d
	return d



def get_ids(path,suffix):
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	ref=0
	st=[]
	data = func(path.split('.')[0]+'.xyz')

	ex_d = get_label_from_excel()

	for line in lines:
		if ref==5:
			break
		if 'File format' in line:
			ref=1
		if len(line.strip().split())==0 and ref>0:
			ref+=1
		if ref==2 or ref==3:
			ref+=1
		if ref==4:
			if suffix=='_dh':
				
				if '[' in line:
					l=line.strip().split()
					st+=[[line.strip().split()[0],l[6],l[8]]]
				else:
					l=line.strip().split()
					st+=[[line.strip().split()[0],l[2],l[4]]]
			else:
				#for acceptor-hydrogen calculation

				s,e=line.index('('),line.index(')')
				l=line[s+1:e].split(',')
				#st+=[[line.strip().split()[0],l[0],l[1],get_avg(data[int(l[0])-1], data[int(l[1])-1])]]   #1

				try:
					print '-'.join([l[0].strip(), l[1].strip()])+path.split('/')[-1].split('.')[0].split('-')[0]
					st_temp = ex_d['-'.join([l[0].strip(), l[1].strip()])+path.split('/')[-1].split('.')[0].split('-')[0]]

					st+=[[line.strip().split()[0],l[0],l[1],get_avg(data[int(l[0])-1], data[int(l[1])-1]),st_temp]]   #2
				except KeyError:
					continue
					st+=[[line.strip().split()[0],l[0],l[1],get_avg(data[int(l[0])-1], data[int(l[1])-1]),'-1']]   #2

			
	return st

#send .txt path
def selection_(path):
	ids=get_ids(path,'_ah')
	#for [h,i,j,k] in ids:   #1
	for [h,i,j,k,l] in ids:    #2
		print h,'id '+i.strip()+','+j.strip()
		#cmd.select(h,'id '+i.strip()+','+j.strip())
		cmd.distance(h, 'id '+i.strip(), 'id '+j.strip())
		cmd.hide('labels', h)
		cmd.pseudoatom(h+'_ps', pos = k, label = l)
		#cmd.label(h+'_ps', h)
		


selection_('/Users/47510753/Desktop/To-Niraj/test2/5e61-qm4.txt')

if __name__=='__main__':
	selection_('/Users/47510753/Desktop/To-Niraj/test2/1r4g-qm5.txt')
	#selection_(sys.argv[1])
