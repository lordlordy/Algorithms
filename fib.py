cache = dict()

def fib(n):
    if n <= 2:
        return 1
    else:
        a = 0
        if cache[str(n-1)]:
            a = cache[str(n-1)]
        else:
            a = fib(n-1)
            
        b = 0
        if cache[str(n-2)]:
            b = cache[str(n-2)]
        else:
            b - fib(n-2)
        return a + b


#n = int(input("number: "))

import datetime
import sys



for n in range(0,1000):
    start = datetime.datetime.now()
    f = fib(n)
    cache[str(n)] = f
    print( datetime.datetime.now() - start)
    # sys.stdout = open("Test.txt",'a')
    print("{}, ".format(f))
    #print(n,f, sep=": -> ", end="\t: ")
    #print(timeTaken)
    # sys.stdout.close()
