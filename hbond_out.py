import os
import sys
import pdb
import pdb1
import com2xyz
import make_lmode_file
import addKaTopdb

#give com file
def xyz(filename):
	com2xyz.make_xyz(filename+'.com')

def hbonds(filename):
	try:
		f=open(filename+'.pdb','r')
		f.close()
		try:
			pdb.job(filename+'.pdb',filename+'.xyz')
		except KeyError:
			pdb1.job(filename+'.xyz')
	except IOError:
		pdb1.job(filename+'.xyz')

def lmode(filename):
	make_lmode_file.make_alm(filename+'.txt','_ah')
	addKaTopdb.addKa(filename+'.txt','_ah')
	make_lmode_file.make_alm(filename+'.txt','_dh')
	addKaTopdb.addKa(filename+'.txt','_dh')

def job():
	path=sys.argv[1]
	filename=path.split('/')[-1].split('.')[0]
	xyz(filename)
	hbonds(filename)
	lmode(filename)

job()



