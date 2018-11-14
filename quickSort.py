
# implementation of quick sort following glgorithmics
import random
import datetime

def quicksort(array):
    _quicksort(array, 0, len(array)-1)

def _quicksort(array, start, end):
    if start < end:
        i = _pivot(array, start, end)
        _quicksort(array, start, i-1)
        _quicksort(array, i+1, end)

def _pivot(array, start, end):
    startvalue = array[start]
    k = start
    i = end
    while array[k] <= startvalue and k < end:
        k += 1
    while array[i] > startvalue:
        i -= 1
    while k < i:
        tempk = array[k]
        tempi = array[i]
        array[k] = tempi
        array[i] = tempk
        while k < end and array[k] <= startvalue:
            k += 1
        while array[i] > startvalue:
            i -= 1

    temps = array[start]
    tempi = array[i]
    array[start] = tempi
    array[i] = temps
    return i

a = [int(random.random()*1000) for i in range(100)]
print(a)
start = datetime.datetime.now()
quicksort(a)
print(a)
print(datetime.datetime.now() - start)
