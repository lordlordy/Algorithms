import random
import datetime

def insertionSort(array):
    for j in range(1,len(array)):
        temp = array[j]
        i = j-1
        while i>=0 and array[i] > temp:
            array[i+1] = array[i]
            i = i - 1
        array[i+1] = temp

a = [int(random.random()*10000) for i in range(2000)]
print(a)
start = datetime.datetime.now()
insertionSort(a)
print(a)
print(f'sort took: {datetime.datetime.now() - start}')