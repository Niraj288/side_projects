import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd
import sys


def alin(a,b):
	ref = mda.Universe(a)
	mobile = mda.Universe(b)
	mobile0 = mobile.select_atoms('name CA').positions - mobile.atoms.center_of_mass()
	ref0 = ref.select_atoms('name CA').positions - ref.atoms.center_of_mass()

	# R is rotation matrix
	R, rmsd = align.rotation_matrix(mobile0, ref0)
	print rmsd
	mobile.atoms.translate(-mobile.select_atoms('name CA').center_of_mass())
	mobile.atoms.rotate(R)
	mobile.atoms.translate(ref.select_atoms('name CA').center_of_mass())
	name = a.split('.')[0]+'_on_'+b.split('.')[0]
	mobile.atoms.write("mobile_on_ref.pdb")

def rms(a,b):
	ref = mda.Universe(a)
	mobile = mda.Universe(b)
	return rmsd(mobile.select_atoms('name CA').positions, ref.select_atoms('name CA').positions, superposition=True)

if __name__=='__main__':
	print alin(sys.argv[1],sys.argv[2])




