import os
import sys
import pdb
import pdb1
import com2xyz
import make_lmode_file
import addKaTopdb

#give com file
def xyz(filename,end):
	com2xyz.make_xyz(filename+'.'+end)

def hbonds(filename):
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

def lmode(filename):
	make_lmode_file.make_alm(filename+'.txt','_ah')
	addKaTopdb.addKa(filename+'.txt','_ah')
	make_lmode_file.make_alm(filename+'.txt','_dh')
	addKaTopdb.addKa(filename+'.txt','_dh')

def job():
	path=sys.argv[1]
	li=path.split('/')[-1].split('.')
	filename=li[0]
	print 'Making xyz ...'
	xyz(filename,li[1])
	print 'Calculating H-Bonds ...'
	hbonds(filename)
	print 'Calculating local modes ...'
	lmode(filename)
	print 'Done!!'

job()



