#%%
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import csv

#%%
# def timeit(f):
#     def i(*args,**kwargs):
#         start_time=time.time()
#         f(*args,**kwargs)
#         end_time=time.time()
#         # print('Running Time: {:.4}ms'.format((end_time-start_time)*10e3))
#         return (end_time-start_time)*10e3
#     return i


# generating random number
def generateLst(number:int):
    return [random.randint(-10e5,10e5) for _ in range(number)]


def bubble(lst:list):
    start_time=time.time()
    for i in range(len(lst)):
        for j in range(len(lst)-1,i,-1):
            if lst[j-1]>lst[j]:
                lst[j-1],lst[j]=lst[j],lst[j-1]
    end_time=time.time()
    return (end_time-start_time) 
    

#%%
n=[]
avgTime_lst=[]
timearr=np.zeros((10,10))
for k in range(200,2001,200):
    n.append(k)
    t=0
    count=10
    for j in range(count):
        tmpTime=bubble(generateLst(k))
        timearr[j,k//200-1]=tmpTime
        t+=tmpTime
    t/=count
    avgTime_lst.append(t)


plt.plot(n,avgTime_lst,marker='o')
# %%
with open('C:\\Users\\Redmibook_PC\\Desktop\\大二下教材课件\\4.3 算法设计\\作业\\2.2.csv','x',encoding='utf-8') as f:
    csvw=csv.writer(f)
    csvw.writerows(timearr)