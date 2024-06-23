#%%
from sortClass import cAlg
import random
import time
import numpy as np
import csv
import matplotlib.pyplot as plt

#%%
# timeArr is for counting and statics
timeArr = np.zeros((10,10,5))
scaleLst= [iNum for iNum in range(200,2001,200)]
MycAlg = cAlg(0,[])
sortingFuncLst = [
        MycAlg.Alg_Sort1,
        MycAlg.Alg_Sort2,
        MycAlg.Alg_Sort3,
        MycAlg.Alg_Sort4,
        MycAlg.Alg_Sort5,
    ]

#%%

for scaleId, scale in enumerate(scaleLst):

    # For each scale, program will carry out 10 tests 
    # to find the average performance 
    for testId in range(10):

        # Initialize random array
        # fD = [random.randint(-1e5,1e5) for _ in range(scale)]

        # For each test, program will run the 5 types of
        # sorting algorithm to distinc the differences
        for AlgId in range(5):

            # Initialize Alg Class with iNum and fD
            fD = [random.randint(-1e5,1e5) for _ in range(scale)]
            MycAlg.set_fD(scale,fD)

            start_time = time.time()
            sortingFuncLst[AlgId]()
            end_time = time.time()

            # Take record of the consumption time
            timeArr[scaleId,testId,AlgId] = end_time - start_time
            
            print(f'''
            Scale: {scale}
            Test: {testId}
            Alg: {AlgId}
            ''')


#%%
# Get the record and plot the result
avgTimeArr=np.zeros((5,10))
for algId in range(5):
    for scaleId in range(10):
        avgTimeArr[algId,scaleId] = timeArr[scaleId,:,algId].mean()
    plt.plot(scaleLst, avgTimeArr[algId,:])

plt.legend(('Bubble Sort','Insertion Sort','Selection Sort','Shell Sort','Quick Sort'))
plt.xlabel('Problem Size')
plt.ylabel('Consumption Time (s)')

with open(f'time{str(random.randint(1,1e5))}.csv','x',encoding='utf-8') as f:
    time_csv=csv.writer(f)
    time_csv.writerows(avgTimeArr)





#%%
scale=2000
# Initialize random array
fD = [random.randint(-1e5,1e5) for _ in range(scale)]
# Initialize Alg Class with iNum and fD
MycAlg = cAlg(scale,fD)


MycAlg.Alg_Sort2()
print(MycAlg.fD)
print(MycAlg.fD==sorted(MycAlg.fD))





