import random

class cAlg:
    def __init__(self,_N:int,_fD:list) -> None:
        self.N=_N
        self.fD=_fD

    def __del__(self):
        pass

    def Initialization(self):
        self.fD=[random.randint(-1e5,1e5) for _ in range(self.N)]

    def get_fD(self):
        return self.fD
    
    def set_fD(self, _N:int, _fD:list):
        self.N=_N
        self.fD=_fD.copy()


    def Alg_Sort1(self):
        # bubble sort 
        for i in range(self.N):
            for j in range(self.N-1,i,-1):
                if self.fD[j-1]>self.fD[j]:
                    self.fD[j-1],self.fD[j]=self.fD[j],self.fD[j-1]

    def Alg_Sort2(self):
        # insertion sort
        for i in range(self.N):
            currentVal=self.fD[i]
            j = i
            while j>0 and self.fD[j-1] > currentVal:
                self.fD[j] = self.fD[j-1]
                j-=1
            self.fD[j] = currentVal
            # for j in range(i,0,-1):
            #     if self.fD[j]<self.fD[j-1]:
            #         self.fD[j],self.fD[j-1]=self.fD[j-1],self.fD[j]
            #     elif self.fD[j-1]<self.fD[j]:
            #         break

    def insertionSort(arr):
        for i in range(len(arr)):
            for j in range(i,0,-1):
                if arr[j]<arr[j-1]:
                    arr[j],arr[j-1]=arr[j-1],arr[j]
                elif arr[j-1]<arr[j]:
                    break
    
    def insertionSortLR(self,l,r):
        for i in range(l,r+1):
            for j in range(i,l,-1):
                if self.fD[j]<self.fD[j-1]:
                    self.fD[j],self.fD[j-1]=self.fD[j-1],self.fD[j]
                elif self.fD[j-1]<self.fD[j]:
                    break
    
    def Alg_Sort3(self):
        # Selection Sort
        for i in range(self.N):
            minidx=self.N-1
            for j in range(self.N-1,i-1,-1):
                if self.fD[j]<self.fD[minidx]:
                    minidx=j
            self.fD[i],self.fD[minidx]=self.fD[minidx],self.fD[i]

    def Alg_Sort4(self):
        # Shell Sort
        gap=self.N//2
        while gap > 0:
            for i in range(gap,self.N):
                currentVal =self.fD[i]
                j=i
                while j-gap>=0 and currentVal<self.fD[j-gap]:
                    self.fD[j]=self.fD[j-gap]
                    j-=gap
                self.fD[j]=currentVal
            gap//=2

    def Alg_Sort5(self):
        # Quick Sort 
        def pivotIdx(l,r):
            ai,bi,ci=l,(l+r)//2,r
            a=self.fD[ai]
            b=self.fD[bi]
            c=self.fD[ci]

            if a<=b:
                if b<=c:
                    return bi
                if c<=a:
                    return ai
                if c>a and c<b:
                    return ci
            if b<a:
                if a<=c:
                    return ai
                if c<=b:
                    return bi
                if c>b and c<a:
                    return ci
                
        def swap(i,j):
            self.fD[i],self.fD[j]=self.fD[j],self.fD[i]
            
        def quickSort(l,r):
            # When the scale is small, typically use insertion sort to reduce 
            # the space occupied by the recursive call
            if r-l<9:
                cAlg.insertionSortLR(self,l,r)
                return
            l0=l
            r0=r
            pi=pivotIdx(l,r)
            pivot=self.fD[pi]
            swap(pi,r0)
            r-=1
            while l<r:
                while self.fD[l]<pivot and l<r:
                    l+=1
                while self.fD[r]>=pivot and l<r:
                    r-=1
                swap(l,r)
            swap(l,r0)
            quickSort( l0, l-1)
            quickSort( l+1, r0)

        quickSort( 0, self.N-1)








