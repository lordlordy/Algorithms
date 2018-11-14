def binomialcoeffient(n,k):
    row = binomialcoeffientForRow(n)
    return row[k]

def binomialcoeffientForRow(n):
    a = []
    for i in range(n):
        a.append((1))
        c = len(a) - 1
        while c > 0:
            a[c] = a[c] + a[c-1]
            c -= 1
    return a


print(binomialcoeffient(8,4))