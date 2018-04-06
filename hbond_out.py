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
import addBCP

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

def BCP(filename):
	addBCP.job(filename)

def job(path):
	li=path.split('/')[-1].split('.')
	if len(li)>1:
		filename='.'.join(li[:-1])
	else:
		filename=li[0]
	print 'Making xyz ...'
	xyz(filename,li[-1])
	
	print 'Calculating H-Bonds ...'
	curr=time.time()
	hbonds(filename)
	print 'Calculation done in',time.time()-curr,'seconds'
	if '-xtb' in sys.argv and '-l' in sys.argv:
		print 'Calculating local modes for stb files ...'
		lmode(filename,'xtb')
	elif '-l' in sys.argv:
		print 'Calculating local modes ...'
		lmode(filename)
	if '-d' in sys.argv:
		print 'Fetching electron density at BCP (a.u) ...'
		BCP(filename)
	print 'Done!!'

if __name__ == "__main__":
	if len(sys.argv)<2:
		print '-c for carbon-hydrogen bond'
		print '-l for local mode calculation'
		print '-d for density at BCP from .sum file'
	else:
		job(sys.argv[1])




