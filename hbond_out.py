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
		addFreq.addFreq(filename+'.txt','_ah')
		addFreq.addFreq(filename+'.txt','_dh')

def BCP(filename):
	addBCP.job(filename)

def job(path):
	li=path.split('/')[-1].split('.')
	if len(li)>1:
		filename='.'.join(li[:-1])
	else:
		filename=li[0]
	
	if path[-4:]!='.txt':
		xyz(filename,li[-1])
		print 'Calculating H-Bonds ...'
		curr=time.time()
		hbonds(filename)
		print 'Calculation done in',time.time()-curr,'seconds'
	else:
		print 'Adding elements to .txt ...'
	
	if '-xtb' in sys.argv and '-l' in sys.argv:
		print 'Calculating local modes for xtb files ...'
		lmode(filename,'xtb')
	elif '-l' in sys.argv:
		print 'Calculating local modes ...'
		lmode(filename)
	if '-f' in sys.argv:
		print 'Calculating local modes frequencies ...'
		lmodefreq(filename)

	if '-d' in sys.argv:
		print 'Fetching electron density at BCP (a.u) ...'
		BCP(filename)

	if '-LP' in sys.argv:
		print 'Adding all lone pair contribution to BD* of H ...'
		addLPCont.job(filename+'.txt')

	if '-Charg' in sys.argv:
		print 'Adding Acceptor and Hydrogen charges ...'
		addCharges.job(filename+'.fchk')

	if '-C' in sys.argv:
		print 'Adding Acceptor and Hydrogen charges from NBO calculations ...'
		addC.job(filename+'.g09.out')

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
		
	else:
		job(sys.argv[1])




