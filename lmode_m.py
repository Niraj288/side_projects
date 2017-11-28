import subprocess
import os
try:
	import xlwt
	import xlrd
	from xlutils.copy import copy as xl_copy
except ImportError:
	import os
	os.system('sudo pip install xlwt')
	os.system('sudo pip install xlrd')
	os.system('sudo pip install xlutils')
	import xlwt
	import xlrd
	from xlutils.copy import copy as xl_copy
d={}
def lmode_m(path,d):
	#print 'performing step 3 ...'
	#proc = subprocess.Popen('/usr/local/octave/3.8.0/bin/octave '+path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	data = subprocess.check_output('/usr/local/octave/3.8.0/bin/octave '+path, shell=True)
	#tmp = proc.stdout.read()
	data=data.split('\n')
	print data,'data'
	ref=0
	st='\n'
	for i in data:
		if len(i.strip().split())==0:
			continue
		if 'adia' in i:
			ref=1
		if ref==1 or ref==2:
			ref+=1
		if ref==3:
			d[path].append(i.strip().split()[0])

def recr(path,d):
	for i in os.listdir(path):
		if '.m'==i[-2:]:
			d[i]=[]
			lmode_m(i,d)

path=raw_input('Enter path : ')
recr(path,d)

if 'Data.xls' in os.listdir(path):

	rb=xlrd.open_workbook('Data.xls', formatting_info=True)
	workbook = xl_copy(rb)
else:
	workbook = xlwt.Workbook()
filename=path.split('/')[-1]
name=raw_input('Enter sheet name : ') or filename.split('/')[-1]
sheet = workbook.add_sheet(name)

sheet.write(0,0,'Name')
sheet.write(0,1,'Force constants')
ref=0
for i in d:
	ref+=1
	sheet.write(ref,0,i)
	for j in d[i]:
		ref+=1
		sheet.write(ref,1,j)

workbook.save('Data.xls')



