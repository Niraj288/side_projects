import sys

def data():
	f=open('data.json','r')
	lines=f.readlines()
	f.close()

	d=eval(''.join(lines))
	fd={}
	for i in range (len(d)):
		fd[i+1]=d[i]
	return fd

def symbol_dict():
	fd=data()
	symbol={}
	for i in range (len(fd)):
		num=i+1
		symbol[fd[num]['symbol']]=num
	return symbol

