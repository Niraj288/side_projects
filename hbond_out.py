import os
import sys
import pdb
import pdb1
import pdb_c
import module
import make_lmode_file
import addKaTopdb
import xtb_lmode

#give com file
def xyz(filename,end):
	print 'Exit status :',module.make_xyz(filename+'.'+end)

def hbonds(filename):
	if '-c' in sys.argv:
		print 'Using xyz file ...'
		print 'Considering C-H...O bonds ...'
		pdb_c.job(filename+'.xyz')
		print 'Success using xyz.'
		return
	try:
		print 'Using pdb ...' 
		f=open(filename+'.pdb','r')
		f.close()
		try:
			pdb.job(filename+'.pdb',filename+'.xyz')
			print 'Success using pdb .'
		except KeyError:
			print 'Mismatch of heavy atoms in pdb and com or fchk file !!'
			print 'Using xyz file ...'
			pdb1.job(filename+'.xyz')
	except IOError:
		print 'No pdb file found !'
		print 'Using xyz file ...'
		pdb1.job(filename+'.xyz')
		print 'Success using xyz.'

def lmode(filename,software='gaussian'):
	if software=='xtb':
		print 'Using xtb output '
		xtb_lmode.make_alm(filename+'.txt','_ah')
		addKaTopdb.addKa(filename+'.txt','_ah')
		xtb_lmode.make_alm(filename+'.txt','_dh')
		addKaTopdb.addKa(filename+'.txt','_dh')
	else:
		make_lmode_file.make_alm(filename+'.txt','_ah')
		addKaTopdb.addKa(filename+'.txt','_ah')
		make_lmode_file.make_alm(filename+'.txt','_dh')
		addKaTopdb.addKa(filename+'.txt','_dh')

def job(path):
	li=path.split('/')[-1].split('.')
	if len(li)>1:
		filename='.'.join(li[:-1])
	else:
		filename=li[0]
	print 'Making xyz ...'
	xyz(filename,li[-1])
	
	print 'Calculating H-Bonds ...'
	hbonds(filename)
	print 'Calculating local modes ...'
	if '-xtb' in sys.argv:
		lmode(filename,'xtb')
	else:
		lmode(filename)
	print 'Done!!'

if __name__ == "__main__":
	job(sys.argv[1])




