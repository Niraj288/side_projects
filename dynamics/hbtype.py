import data
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import copy
style.use("ggplot")

def get_arch(i,d,links_h,links_o,hbonds,obonds):
	vs = set()
	liss = []

	# acceptor oxygen hydrogen bonds
	l1 = hbonds[i]

	# two hydrogens from acceptor oxygen
	try:
		a,b = links_o[i]
		l2 = []
		if a in obonds:
			l2 = obonds[a]
		if b in obonds:
			l2 = obonds[b]
	except ValueError:
		return None


	for j in l1:
		st = str(i)+'-'+str(j)

		
		if st not in vs:
			# donar oxygen hydrogen bonds
			try:
				o = links_h[j][0]
				#print o, j
				if o in hbonds:
					l3 = hbonds[o]
				else:
					l3 = []

			except KeyError:
				return None

			# donar hydrogen links
			try:
				a,b = links_o[o]
				if a == j:
					c = b 
				else:
					c = a
				if c in obonds:
					l4 = obonds[c]
				else:
					l4 = []
			except ValueError:
				return None
			if len(l1) > 1:
				ck = copy.copy(l1)
				ck.remove(j)
				liss.append([st, l3, l4, ck, l2]) # Yunwen type
				#liss.append([st, l2, [l1[1]], l3, l4]) # Niraj Type
				'''
				if l1[0] == j:
					liss.append([st, l3, l4, [l1[1]], l2]) # Yunwen type
					#liss.append([st, l2, [l1[1]], l3, l4]) # Niraj Type
				else:
					liss.append([st, l3, l4, [l1[0]], l2])
					#liss.append([st, l2, [l1[0]], l3, l4])
				'''
			else:
				liss.append([st, l3, l4, [], l2])
				#liss.append([st, l2, [], l3, l4])

			
			#print st
			vs.add(st)

	return liss






def hbtype(d,links_h,links_o,hbonds,obonds):
	hb = []

	for i in hbonds:
		l = get_arch(i,d,links_h,links_o,hbonds,obonds)
		if l:
			hb += l

	return hb 

def result(d,links_h,links_o,hbonds,obonds):

	res = {}
	for i in range (4):
		for j in range (4):
			for k in range (4):
				for l in range (4):
					st = str(i)+str(j)+'-'+str(k)+str(l)
					res[st] = []

	
	hb = hbtype(d,links_h,links_o,hbonds,obonds)
	warns = 0
	for i in hb:
		if i:
			a,b,c,d = map(str,map(len,i[1:]))
			st = i[0]
			try:
				res[a+b+'-'+c+d].append([st,a,b,c,d])
			except KeyError:
				print 'Warning : '+a+b+'-'+c+d+' type HB found with id as'+str(i)
				warns += 1
	if warns:
		print 'Number of warnings:',warns
	return res 


def visual(d,links_h,links_o,hbonds,obonds):

	res = result(d,links_h,links_o,hbonds,obonds)
	lis = []
	for i in res:
		lis.append([len(res[i]), i])

	lis.sort(reverse = True)

	x_labels = [i[1] for i in lis if i[0]!= 0]
	frequencies = [i[0] for i in lis if i[0]!=0]

	print lis

	plt.figure(figsize=(12, 8))
	freq_series = pd.Series.from_array(frequencies)
	ax = freq_series.plot(kind='bar')
	ax.set_ylabel('Frequency')
	ax.set_xticklabels(x_labels)

	plt.show()






if __name__=='__main__':
	d,links_h,links_o,hbonds,obonds=data.data()
	visual(d,links_h,links_o,hbonds,obonds)
	'''
	res = result(d,links_h,links_o,hbonds,obonds)
	for i in res:
		if len(res[i]) > 0:
			print i, len(res[i])
	'''










