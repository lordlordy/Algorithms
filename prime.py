primeCache = set()
primeCache.add(2)

def calcPrimesUpTo(n):
    for x in range(3,n+1):
        for p in primeCache :
            if x % p == 0: 
                break # we have a factor
        else:
            print(str(x) + " is PRIME")
            primeCache.add(x)

import datetime

start = datetime.datetime.now()

calcPrimesUpTo(1000000)

print(datetime.datetime.now() - start)