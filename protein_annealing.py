# get sequence from protein
import os
import sys
import folding_connections as fdc
import EvsT
import pdb_analysis_c5 as c5

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

def make_gaff_xleap(f,ty = 'gout'):
  name = '.'.join(f.split('/')[-1].split('.')[:-1])
  st = 'antechamber -i file -fi type -o name.mol2 -fo mol2 -c bcc -s 2'
  st = st.replace('name',name)
  st = st.replace('type',ty)
  st = st.replace('file',f)

  os.system(st)

  st = 'parmchk -i name.mol2 -f mol2 -o name.frcmod'
  st = st.replace('name',name)

  os.system(st)

  st = """source leaprc.gaff
SUS = loadmol2 name.mol2 
loadamberparams name.frcmod
saveoff SUS sus.lib 
saveamberparm SUS name.prmtop name.inpcrd 
quit
"""
  st = st.replace('name',name)
  g = open('xleap_input','w')
  g.write(st)
  g.close()

  return

def make_xleap_input(f,params):
        file = open(f,'r')
        lines= file.readlines()
        file.close()

        name = '.'.join(f.split('/')[-1].split('.')[:-1])

        st=''
        st+='source ff\n'#leaprc.gaff\n'#oldff/leaprc.ff99\n'
        st = st.replace('ff', params['ff'])
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


def annealing(params):
        f = open('ann.in','w')
        steps = params['steps']
        st="""Stage annealing

&cntrl
  imin=0, irest=0, ntx=1,
  nstlim=30000, 
  ntc=2, ntf=2,
  ntt=1, 
  ntpr=50, ntwx=50,
  ntb=0, igb=1,
  cut=20,rgbmax=999.,
  pencut=-0.001,
  nmropt=1,
 /

&wt type='TEMP0', istep1=0,istep2=10000,value1=400.,
            value2=400.,    /
&wt type='TEMP0', istep1=10001,istep2=20000,value1=400.,
            value2=100.,    /
&wt type='TEMP0', istep1=20001,istep2=30000,value1=0.,
            value2=0.,    /
                                    
&wt type='TAUTP', istep1=0,istep2=30000,value1=0.1,
            value2=0.1,     /
&wt type='REST', istep1=0,istep2=30000,value1=1.,            
            value2=1.,  /
&wt type='END'  /

 DISANG=dist.RST

 
 
 """
        #st = st.replace('steps',str(steps))
        f.write(st)
        f.close()


def make_rst_file(file, ty, params):

  name = '.'.join(file.split('/')[-1].split('.')[:-1])
  st=''
  if 'unmodified' in os.getcwd():
    print 'Unmodified category !'
    f = open('dist.RST','w')
    f.write(st)
    f.close()
    return

  if ty!='pdb':
    dic = fdc.connection_analysis(file)
  else:

    dic = fdc.connection_analysis(name+'_linear.pdb')
  
  print 'Modified Category !'
  for i,j,k in dic:
    ar,br = i,k 
    if 1 and dic[(i,j,k)][-1]=='NH-N':
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(ar)+', '+str(br)+' , r1= NH-Nd0, r2= NH-Nd1, r3= NH-Nd2, r4= NH-Nd2, rk2= NH-Nk1, rk3= NH-Nk2, /\n'
    elif 1 and dic[(i,j,k)][-1]=='NH-O':
      #continue
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(ar)+', '+str(br)+' , r1= NH-Od0, r2= NH-Od1, r3= NH-Od2, r4= NH-Od2, rk2= NH-Ok1, rk3= NH-Ok2, /\n'
    elif 0 and o and dic[(i,j)][-1]=='CH-O':
      #continue
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(ar)+', '+str(br)+' , r1= 1.72, r2= 2.3, r3= 2.5, r4= 3.0, rk2= 35.959, rk3= 35.959, /\n'
    elif 0 and dic[(i,j)][-1]=='CH-N':
      #continue
      st+=' &rst ixpk= 0, nxpk= 0, iat= '+str(ar)+', '+str(br)+' , r1= 1.72, r2= 2.32, r3= 2.5, r4= 3.0, rk2= 35.959, rk3= 35.959, /\n'
  
  for i in params:
    if 'NH' in i:
      st = st.replace(i,str(params[i]))

  f = open('dist.RST','w')
  f.write(st)
  f.close()


def run_folding(file, ty, params):
        name = '.'.join(file.split('/')[-1].split('.')[:-1])

        print 'Initializing protein folding for '+name+ ' ...'

        
        if ty!='pdb':
          #pass
          make_gaff_xleap(file, ty)
        else:
          print 'Making a straight chain with topology files ...'
          make_xleap_input(file,params)
        os.system('tleap -f xleap_input')
        
        print 'Making RST file ...'
        make_rst_file(file, ty, params)
        
        print 'Initial Minimization of the structure ...'
        minimization()
        st = 'sander -O -i min1.in -o min1.out -p name.prmtop -c name.inpcrd -r min1.rst'
        st = st.replace('name',name)
        os.system(st)

        print 'Annealing structure simulation ...'
        annealing(params)
        st = """sander -O -i ann.in -p name.prmtop -c min1.rst -r ann.rst -o ann.out -x ann.mdcrd"""
        st = st.replace('name',name)
        os.system(st)

        print 'Saving pdb file ...'
        st = "ambpdb -p name.prmtop -c ann.rst > ann.pdb"
        st = st.replace('name',name)
        os.system(st)


	
	
if __name__=='__main__':
  ty = sys.argv[1].split('.')[-1]

  params = {'NH-Nd0':1.5,
            'NH-Nd1':2.2,
            'NH-Nd2':2.2,
            'NH-Nd3':2.8,
            'NH-Nk1':40.,
            'NH-Nk2':40.,
            'NH-Od0':1.5,
            'NH-Od1':2.18,
            'NH-Od2':2.18,
            'NH-Od3':2.8,
            'NH-Ok1':35.,
            'NH-Ok2':35.,
            'steps':2500,
            'ff':'oldff/leaprc.ff99SB'}

  run_folding(sys.argv[1],ty, params)



