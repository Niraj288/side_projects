import os
import sys
import numpy as np 
import math

def distance(a,b):
  
  res=0
  for i in range (len(a)):
    res+=(a[i]-b[i])**2
  return math.sqrt(res)

def get_val(data,i,j,d,inde):
        lis=[]
        li=map(float,[data[i][0],data[j][0]])
        li.sort()
        r=distance(data[i][1:4],data[j][1:4])
        m1,m2=0,0
        #print data[i],inde
        if r==0:
          d[tuple(li)]+=[0.5*data[i][0]**2]
          return
        for c,ex in data[i][inde]:
          c,ex=float(c),float(ex)
          m1+=c*math.exp(-ex*r/2)
        for c,ex in data[j][inde]:
          c,ex=float(c),float(ex)
          m2+=c*math.exp(-ex*r/2)
        d[tuple(li)]+=[m1*m2]

def get_val2(data,i,j,d,inde):
        lis=[]
        li=map(float,[data[i][0],data[j][0]])
        li.sort()
        r=distance(data[i][1:4],data[j][1:4])
        if r==0.0:
                if data[i][inde]<0:
                        lis.append(-0.5*data[i][inde]**2)
                else:
                        lis.append(0.5*data[i][inde]**2)#data[i][0])
        else:
                #lis.append(r)
                lis.append((data[i][inde]*data[j][inde])/r)
        d[tuple(li)]+=[lis[-1]]

#align with 70 places for each bond
def align(d,size):
        t=500
        ma=0
        for i in d:
                k=d[i]
                k.sort(reverse=1)
                d[i]=k
                ma+=len(d[i])

        lis=[]
        a,b=size

        for i in range (1,a):
                for j in range (1,b):
                        li=[float(i),float(j)]
                        li.sort()
                        if len(d[tuple(li)])==0:
                                continue
                        #if len(d[tuple(li)])>50:
                        # print len(d[tuple(li)])
                        lis+=d[tuple(li)]+[0.0]#*(120-len(d[tuple(li)]))
        if len(lis)>300:
                print len(lis)
        if len(lis)<t:
                lis+=[0.0]*(t-len(lis))
        if len(lis)>t:
                print 'Warning : Data loss ',len(lis),t
        return lis

def get_list2(i,data,inde,a):
  lis=[]
  for l in range (len(data)):
    r=distance(data[i][1:4],data[l][1:4])
    if r==0:
        lis.append(0.0)
    else:
        m1,m2=0,0
        for c,ex in data[i][inde]:
          c,ex=float(c),float(ex)
          m1+=c*math.exp(-ex*r/2)
        for c,ex in data[l][inde]:
          c,ex=float(c),float(ex)
          m2+=c*math.exp(-ex*r/2)
        lis.append(m1*m2)
  return lis+[0.0]*(a-len(lis))

#Simple sort
def process3(data,size,d3):
  k=len(data[0])
  indexes=[]#[0]
  if k>3:
    indexes+=range(4,k)
  lis=[]
  #print indexes
  a,b=size
  #data=alignd(data,indexes)
  for inde in indexes:
          li=[]
          for i in range (len(data)):
                  li+=get_list2(i,data,inde,a)

          lis+=li+[0.0]*(a*b-len(li))
          li.sort(reverse=1)
  if len(lis)==a*b*len(indexes):
          return np.array(lis)
  else:
          raise Exception('Data exceeded maximum atoms limit !!')

def process(data,size,d3):
  k=len(data[0])
  indexes=[0]#[0]
  if k>3:
    indexes+=range(4,k)
  big_li=[]
  #print indexes
  for inde in indexes:
    a,b=size
    d={}
    vs=[]
    for i in range (1,a):
      for j in range (1,b):
        li=[float(i),float(j)]
        li.sort()
        d[tuple(li)]=[]
    for i in range (len(data)):
      for j in range (i+1):
        li=[data[i],data[j]]
        li.sort()
        if inde==0:
          val=get_val2(data,i,j,d,0)
        else:
          val=get_val(data,i,j,d,inde)

    big_li+=align(d,size)
  return np.array(big_li)

if __name__=='__main__':
  print len(process([[1,0,0,0,-1],[2,1,0,0,-4],[1,0,1,0,2]],[10,10],0))





  