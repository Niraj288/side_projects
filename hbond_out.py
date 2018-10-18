import os
import sys
import pdb
import pdb1
import pdb_c
import module
import make_lmode_file
import addKaTopdb
import xtb_lmode
import time
import addC
import addBCP
import addFreq
import addLPCont
import addCharges
import addRing
import xlwt

def make_excel(d,filename):
    workbook = xlwt.Workbook()
    #workbook = xl_copy(rb)
    name='sheet1'
    sheet = workbook.add_sheet(name)

    sheet.write(0,0,'S/No')
    sheet.write(0,1,'Bond')
    sheet.write(0,2,'atomIDs')
    sheet.write(0,3,'HB length')

    for i in d['hb']:
        sheet.write(int(i[:-1]),0,i[:-1])
        sheet.write(int(i[:-1]),1,d['hb'][i][0]) 
        sheet.write(int(i[:-1]),2,d['hb'][i][1])
        sheet.write(int(i[:-1]),3,float(d['hb'][i][2]))

    ref=3
    for i in d:
    	if i=='hb':
    		continue
    	if i=='l':
    		ref+=1
    		sheet.write(0,ref,'Ka(Acceptor)')
    		sheet.write(0,ref+1,'Ka(Donor)')
    		a,b=d[i]
    		for j in a:
			if '?' in a[j]:
				sheet.write(int(j[:-1]),ref,a[j][:-3])
			else:
    				sheet.write(int(j[:-1]),ref,a[j])
    		for j in b:
			if '?' in b[j]:
                                sheet.write(int(j[:-1]),ref,b[j][:-3])
                        else:
    				sheet.write(int(j[:-1]),ref+1,b[j])
    		ref+=1
    	if i=='lf':
    		ref+=1
    		sheet.write(0,ref,'freq(Acceptor)')
    		sheet.write(0,ref+1,'freq(Donor)')
    		a,b=d[i]
    		for j in a:
    			sheet.write(int(j[:-1]),ref,a[j])
    		for j in b:
    			sheet.write(int(j[:-1]),ref+1,b[j])
    		ref+=1
    	if i=='bcp':
    		ref+=1
    		sheet.write(0,ref,'H(r)atBCP')
    		for j in d[i]:
    			sheet.write(int(j[:-1]),ref,d[i][j])
    	if i=='charg':
    		ref+=1
    		sheet.write(0,ref,'AcceptorCharge(Mulliken)')
    		sheet.write(0,ref+1,'DonarCharge(Mulliken)')
    		sheet.write(0,ref+2,'Chargediff(Mulliken)')
    		for j in d[i]:
    			a,b=d[i][j].strip().split()
    			sheet.write(int(j[:-1]),ref,a)
    			sheet.write(int(j[:-1]),ref+1,b)
    			sheet.write(int(j[:-1]),ref+2,float(b)-float(a))
    		ref+=2
    	if i=='C':
    		ref+=1
    		sheet.write(0,ref,'AcceptorCharge(NBO)')
    		sheet.write(0,ref+1,'DonarCharge(NBO)')
    		sheet.write(0,ref+2,'Chargediff(NBO)')
    		for j in d[i]:
			#print d[j][i]
    			a,b=d[i][j].strip().split()
    			sheet.write(int(j[:-1]),ref,a)
    			sheet.write(int(j[:-1]),ref+1,b)
    			sheet.write(int(j[:-1]),ref+2,float(b)-float(a))
    		ref+=2
    	if i=='R':
    		ref+=1
    		sheet.write(0,ref,'Intra-HB')
    		for j in d[i]:
    			sheet.write(int(j[:-1]),ref,d[i][j])
	
	if i=='lp':
                ref+=1
                sheet.write(0,ref,'LPtoBD*')
                for j in d[i]:
                        sheet.write(int(j[:-1]),ref,d[i][j])

    workbook.save(filename+'.xls')

#give com file
def xyz(filename,end):
	if end==xyz:
		return
	print 'Making xyz ...'
	print 'Exit status :',module.make_xyz(filename+'.'+end)

def hbonds(filename):
	if '-c' in sys.argv:
		print 'Using xyz file ...'
		print 'Considering C-H...O bonds ...'
		p=pdb_c.job(filename+'.xyz')
		print 'Success using xyz.'
		return p
	try:
		print 'Using pdb ...' 
		f=open(filename+'.pdb','r')
		f.close()
		try:
			p=pdb.job(filename+'.pdb',filename+'.xyz')
			print 'Success using pdb .'
			return p
		except KeyError:
			print 'Mismatch of heavy atoms in pdb and com or fchk file !!'
			print 'Using xyz file ...'
			p=pdb1.job(filename+'.xyz')
			return p
	except IOError:
		print 'No pdb file found !'
		print 'Using xyz file ...'
		p=pdb1.job(filename+'.xyz')
		print 'Success using xyz.'
		return p 

def lmode(filename,software='gaussian'):
	if software=='xtb':
		print 'Using xtb output '
		xtb_lmode.make_alm(filename+'.txt','_ah')
		addKaTopdb.addKa(filename+'.txt','_ah')
		xtb_lmode.make_alm(filename+'.txt','_dh')
		addKaTopdb.addKa(filename+'.txt','_dh')
	else:
		make_lmode_file.make_alm(filename+'.txt','_ah')
		a=addKaTopdb.addKa(filename+'.txt','_ah')
		make_lmode_file.make_alm(filename+'.txt','_dh')
		d=addKaTopdb.addKa(filename+'.txt','_dh')
		return [a,d]

def lmodefreq(filename,software='gaussian'):
	# change things for xtb
	if software=='xtb':
		print 'Using xtb output '
		xtb_lmode.make_alm(filename+'.txt','_ah')
		addKaTopdb.addKa(filename+'.txt','_ah')
		xtb_lmode.make_alm(filename+'.txt','_dh')
		addKaTopdb.addKa(filename+'.txt','_dh')
	else:
		if '-l' not in sys.argv:
			make_lmode_file.make_alm(filename+'.txt','_ah')
			make_lmode_file.make_alm(filename+'.txt','_dh')
		a=addFreq.addFreq(filename+'.txt','_ah')
		d=addFreq.addFreq(filename+'.txt','_dh')
		return [a,d]

def BCP(filename):
	return addBCP.job(filename)

def job(path):
	lis_excel={}
	li=path.split('/')[-1].split('.')
	if len(li)>1:
		filename='.'.join(li[:-1])
	else:
		filename=li[0]
	
	if path[-4:]!='.txt':
		xyz(filename,li[-1])
		print 'Calculating H-Bonds ...'
		curr=time.time()
		hb=hbonds(filename)
		print 'Calculation done in',time.time()-curr,'seconds'
		lis_excel['hb']=hb
	else:
		print 'Adding elements to .txt ...'
	
	if '-xtb' in sys.argv and '-l' in sys.argv:
		print 'Calculating local modes for xtb files ...'
		l = lmode(filename,'xtb')
		lis_excel['l']=l
	elif '-l' in sys.argv:
		print 'Calculating local modes ...'
		l=lmode(filename)
		lis_excel['l']=l
	if '-f' in sys.argv:
		print 'Calculating local modes frequencies ...'
		lf=lmodefreq(filename)
		lis_excel['lf']=lf

	if '-d' in sys.argv:
		print 'Fetching electron density at BCP (a.u) ...'
		bcp=BCP(filename)
		lis_excel['bcp']=bcp

	if '-LP' in sys.argv:
		print 'Adding all lone pair contribution to BD* of H ...'
		lp=addLPCont.job(filename+'.txt')
		lis_excel['lp']=lp

	if '-Charg' in sys.argv:
		print 'Adding Acceptor and Hydrogen charges ...'
		charg=addCharges.job(filename+'.fchk')
		lis_excel['charg']=charg

	if '-C' in sys.argv:
		print 'Adding Acceptor and Hydrogen charges from NBO calculations ...'
		C=addC.job(filename+'.g09.out')
		lis_excel['C']=C

	if '-R' in sys.argv:
		print 'Doing Intramolecular analysis ...'
		R=addRing.job(filename+'.txt')
		lis_excel['R']=R

	make_excel(lis_excel,filename)

	print 'Done!!'

if __name__ == "__main__":
	if len(sys.argv)<2:
		print '-c for carbon-hydrogen bond from .fchk file'
		print '-l for local mode calculation from .fchk file'
		print '-f for frequency calculation from .fchk'
		print '-Charg for charges from .fchk file (Mulliken charges)'
		print '-d for density at BCP from .sum file'
		print '-C for charges from .g09.out file (NBO population analysis)'
		print '-LP for lone pair contribution from nbo calculations in .g09.out file'
		print '-R to do Intramolecular analysis'
		
	else:
		job(sys.argv[1])




