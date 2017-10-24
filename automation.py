import os
from module import zmatrix 

file='test5.xyz'
filename=file.split('.')

s0='%chk='+filename+'.chk\n'

s1="""%nprocshared=64
%mem=39GB
#p opt=z-matrix freq b3lyp/6-31g(d,p) nosymm 
empiricaldispersion=gd3bj int=ultrafine
"""

s2=filename+'\n0 1\n'

s3=zmatrix.string(file)

f=open(filename+'.g16','w')
f.write(s0)
f.write(s1)
f.write(s2)
f.write(s3)
f.write('\n')


