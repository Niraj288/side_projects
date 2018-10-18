from pymol import cmd
import os
import sys


#cmd.h_add(selection='(all)')
#preset.ball_and_stick(selection='all', mode=1)
lis=cmd.get_object_list(selection='(all)')

for i in lis:
	xyz = cmd.get_coordset(i, 1)
	print xyz