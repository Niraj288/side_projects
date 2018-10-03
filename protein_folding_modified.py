# get sequence from protein
import os
import sys
import folding_connections as fdc
import EvsT

def get_sequence(lines):
        d={}
        arr_a=set()
        for line in lines:
                if "TER" in line.split()[0]:
                        break
                if line.split()[0] in ['ATOM']:
                        #print line
                        id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
                        s=line.strip().split()[-1]
                        d[int(_0)]=rt
                        arr_a.add(int(_0))
        lis = list(arr_a)
        d[lis[0]] = 'N'+d[lis[0]]
        d[lis[-1]] = 'C'+d[lis[-1]]
        arr = [d[i] for i in lis]
        return ' '.join(arr)

def make_xleap_input(f):
	file = open(f,'r')
	lines= file.readlines()
	file.close()

	name = '.'.join(f.split('/')[-1].split('.')[:-1])

	st=''
	st+='source oldff/leaprc.ff14SB\n'#leaprc.gaff\n'#oldff/leaprc.ff99\n'
	seq = get_sequence(lines)
	st+=name +' = sequence { '+seq+' }\n'

	st+='saveoff '+name+' '+name+'_linear.lib\n'
	st+='savepdb '+name+' '+name+'_linear.pdb\n'

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
  ntpr=100,
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
  nstlim=10000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=0.,
            value2=50.,    /
&wt type='TAUTP', istep1=0,istep2=10000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=10000,value1=1.0,                             
            value2=1.0,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()
 	
 	f = open('heat2.in','w')
	f.write("""Stage 2 heating from 50K to 100K
 &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=10000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=50.,
            value2=100.,    /
&wt type='TAUTP', istep1=0,istep2=10000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=10000,value1=1.0,                             
            value2=1.0,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()

	f = open('heat3.in','w')
	f.write("""Stage 3 heating from 100 to 150K
  &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=10000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=100.,
            value2=150.,    /
&wt type='TAUTP', istep1=0,istep2=10000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=10000,value1=1.0,                             
            value2=1.0,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()

	f = open('heat4.in','w')
	f.write("""Stage 4 heating from 150 to 200K
  &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=10000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=150.,
            value2=200.,    /
&wt type='TAUTP', istep1=0,istep2=10000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=10000,value1=1.0,                             
            value2=1.0,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()

	f = open('heat5.in','w')
	f.write("""Stage 1 heating of from 200 to 300K
  &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=20000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=20000,value1=200.,
            value2=250.,    /
&wt type='TAUTP', istep1=0,istep2=20000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=20000,value1=1.0,                             
            value2=1.0,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()

	f = open('heat6.in','w')
	f.write("""Stage 6 heating 300K to 300K
  &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=10000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=999.,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=300.,
            value2=300.,    /
&wt type='TAUTP', istep1=0,istep2=10000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=10000,value1=1.,                             
            value2=1.,  /
&wt type='END'  /

 DISANG=dist.RST

 
 """)
	f.close()

def equillibrium():
        f = open('equil1.in','w')
        steps = '5000'
        st="""Stage 2 equilibration 1 0-2.5ns

&cntrl
  imin=0, irest=0, ntx=1,
  nstlim=steps, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=200, ntwx=200,
  ntb=0, igb=1,
  cut=20,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=steps,value1=300.,
            value2=300.,    /
&wt type='TAUTP', istep1=0,istep2=steps,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=steps,value1=1.,            
            value2=1.,  /
&wt type='END'  /

 DISANG=dist.RST

 
 
 """
        st = st.replace('steps',steps)
        f.write(st)
        f.close()


def make_rst_file(name):
  
  if 'unmodified' in os.getcwd():
    print 'Unmodified category !'
    f = open('dist.RST','w')
    f.write(st)
    f.close()
    return

  dic = fdc.connection_analysis(name+'_linear.pdb')
  st=''
  print 'Modified Category !'
  for i,j in dic:
    if dic[(i,j)][-1]=='NH-N':
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(i)+', '+str(j)+' , r1= 1.6, r2= 2.2, r3= 2.2, r4= 2.7, rk2= 40.27408, rk3= 40.27408, /\n'
    elif dic[(i,j)][-1]=='NH-O':
      #continue
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(i)+', '+str(j)+' , r1= 1.52, r2= 2.12, r3= 2.12, r4= 2.52, rk2= 35.959, rk3= 35.959, /\n'

  f = open('dist.RST','w')
  f.write(st)
  f.close()


def run_folding(file):
        name = '.'.join(file.split('/')[-1].split('.')[:-1])

        print 'Initializing protein folding for '+name+ ' ...'

        print 'Making a straight chain with topology files ...'
        make_xleap_input(file)
        os.system('xleap -f xleap_input')

        print 'Making RST file ...'
        make_rst_file(name)

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
"""
        st = st.replace('name',name)
        os.system(st)

        print 'Equillibrium structure simulation ...'
        equillibrium()
        st = """sander -O -i equil1.in -p name.prmtop -c heat6.rst -r equil1.rst -o equil1.out -x equil1.mdcrd"""
        st = st.replace('name',name)
        os.system(st)


	
	
if __name__=='__main__':
  run_folding(sys.argv[1])
  print 'Running analysis on equil1.out ...'
  EvsT.job(sys.argv[1])
  #make_rst_file(sys.argv[1])


