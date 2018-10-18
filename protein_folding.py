# get sequence from protein
import os
import sys

def get_sequence(lines):
        d={}
        for line in lines:
                if "TER" in line.split()[0]:
                        break
                if line.split()[0] in ['ATOM','HETATM']:
                        #print line
                        id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
                        s=line.strip().split()[-1]
                        d[int(_0)]=rt

        d[1] = 'N'+d[1]
        d[len(d)] = 'C'+d[len(d)]
        arr = [d[i] for i in range (1,len(d)+1)]
        return ' '.join(arr)

def make_xleap_input(f):
	file = open(f,'r')
	lines= file.readlines()
	file.close()

	name = '.'.join(f.split('/')[-1].split('.')[:-1])

	st=''
	st+='source oldff/leaprc.ff99SB\n'
	seq = get_sequence(lines)
	st+=name +' = sequence { '+seq+' }\n'

	st+='saveoff '+name+' '+name+'_linear.lib\n'
	st+='saveoff '+name+' '+name+'_linear.pdb\n'

	st+='saveamberparm '+name+' '+' '+name+'.prmtop'+' '+name+'.inpcrd\n'
	st+='quit\n'
	g = open('xleap_input','w')
	g.write(st)
	g.close()

	return  

def minimization():
	text = """Stage 1 - minimisation
 &cntrl
  imin=1, maxcyc=1000, ncyc=500,
  cut=999., rgbmax=999.,igb=1, ntb=0,
  ntpr=100
 /
 """

 	g = open('min1.in','w')
 	g.write(text)
 	g.close()

def heating():
	f = open('heat1.in','w')
	f.write("""Stage 1 heating from 0 to 50K
 &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=0.0, temp0=50.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.
 /
 """)
	f.close()
 	
 	f = open('heat2.in','w')
	f.write("""Stage 1 heating from 50K to 100K
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=50.0, temp0=100.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.0,rgbmax=999.
 /
 """)
	f.close()

	f = open('heat3.in','w')
	f.write("""Stage 1 heating from 100 to 150K
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=100.0, temp0=150.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.0,rgbmax=999.
 /
 """)
	f.close()

	f = open('heat4.in','w')
	f.write("""Stage 1 heating from 150 to 200K
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=150.0, temp0=200.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.0,rgbmax=999.
 /
 """)
	f.close()

	f = open('heat5.in','w')
	f.write("""Stage 1 heating of from 200 to 250K
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=200.0, temp0=250.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.
 /
 """)
	f.close()

	f = open('heat6.in','w')
	f.write("""Stage 1 heating of TC5b 250 to 300K
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=10000, dt=0.0005,
  ntc=2, ntf=2,
  ntt=1, tautp=1.0,
  tempi=250.0, temp0=300.0,
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.
 /
 """)
	f.close()

def equillibrium():
	f = open('equil1.in','w')
	f.write("""Stage 2 equilibration 1 0-1ns
 &cntrl
  imin=0, irest=1, ntx=5,
  nstlim=25000, dt=0.002,
  ntc=2, ntf=2,
  ntt=1, tautp=0.5,
  tempi=325.0, temp0=325.0,
  ntpr=500, ntwx=500,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.
 /
 """)
	f.close()

	f = open('equil2.in','w')
	f.write("""Stage 2 equilibration 2 1-2ns
 &cntrl                                                                        
  imin=0, irest=1, ntx=5,                                                      
  nstlim=25000, dt=0.002,                                                    
  ntc=2, ntf=2,                                                                
  ntt=1, tautp=0.5,                                                            
  tempi=325.0, temp0=325.0,                                                    
  ntpr=500, ntwx=500,                                                          
  ntb=0, igb=1,                                                                
  cut=999.,rgbmax=999.                                                         
 /
 """)
	f.close()


def run_folding(file):
	name = '.'.join(file.split('/')[-1].split('.')[:-1])

	print 'Initializing protein folding for '+name+ ' ...'

	print 'Making a straight chain with topology files ...'
	make_xleap_input(file)
	os.system('xleap -f xleap_input')

	print 'Initial Minimization of the structure ...'
	minimization()
	st = 'sander -O -i min1.in -o min1.out -p name.prmtop -c name.inpcrd -r min1.rst'
	st = st.replace('name',name)
	os.system(st)

	print 'Heating the protein to fold from 0 till 300K in 6 steps ...'
	heating()
	st = """sander -O -i heat1.in -p name.prmtop -c min1.rst -r heat1.rst -o heat1.out -x heat1.mdcrd
sander -O -i heat2.in -p name.prmtop -c heat1.rst -r heat2.rst -o heat2.out -x heat2.mdcrd
sander -O -i heat3.in -p name.prmtop -c heat2.rst -r heat3.rst -o heat3.out -x heat3.mdcrd
sander -O -i heat4.in -p name.prmtop -c heat3.rst -r heat4.rst -o heat4.out -x heat4.mdcrd
sander -O -i heat5.in -p name.prmtop -c heat4.rst -r heat5.rst -o heat5.out -x heat5.mdcrd
sander -O -i heat6.in -p name.prmtop -c heat5.rst -r heat6.rst -o heat6.out -x heat6.mdcrd
sander -O -i heat7.in -p name.prmtop -c heat6.rst -r heat7.rst -o heat7.out -x heat7.mdcrd"""
	st = st.replace('name',name)
	os.system(st)

	print 'Equillibrium structure simulation ...'
	equillibrium()
	st = """sander -O -i equil1.in -p name.prmtop -c heat6.rst -r equil1.rst -o equil1.out -x equil1.mdcrd
sander -O -i equil2.in -p name.prmtop -c equil1.rst -r equil2.rst -o equil2.out -x equil2.mdcrd"""
	st = st.replace('name',name)
	os.system(st)


	
	





if __name__=='__main__':
	run_folding(sys.argv[1])