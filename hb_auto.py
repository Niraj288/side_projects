#automate in directory
import xlwt
import os
import sys
import hbond_out
import make_xl

def make_excel(d):
	bonds={}
	b,f=[],[]
	for i in d:
	 	#b=d[i]
	 	f.append(i)
	 	for j in d[i]:
	 		if j not in b:
	 			b.append(j)
	 		bonds[j,i]=d[i][j]

	wb=xlwt.Workbook() 
	sheet = wb.add_sheet('Version1')

	r=0
	mul=-1
	for i in b:
		mul+=1
		c=0
		r=25*mul
		sheet.write(r,c,i)
		for j in f:
			r=25*mul+1
			sheet.write(r,c,j)
			if (i,j) not in bonds:
				c+=2
				r+=1
				continue
			lis=bonds[i,j]
			r+=1
			for k in lis:
				sheet.write(r,c,float(k[0]))
				sheet.write(r,c+1,float(k[1]))
				r+=1
			c+=2
			
		
	wb.save('test_mode.xls')



def make_output():
	dic={}
	for i in os.listdir(sys.argv[1]):
		if i[-5:]=='.fchk':
			print 'Procession the file '+i
			#hbond_out.job(i)
			dic[i]=make_xl.xl(i.split('/')[-1].split('.')[0]+'.txt')
			print '\n'
	make_excel(dic)



if __name__ == "__main__":
	make_output()

