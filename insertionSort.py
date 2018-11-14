array = input("Array of integers: ")
intArray = [int(x) for x in array.split(",")]

#intersertion for

for j in range(1,len(intArray)):
    print(intArray)
    temp = intArray[j]
    i = j-1
    while i>=0 and intArray[i] > temp:
        intArray[i+1] = intArray[i]
        i = i - 1
    intArray[i+1] = temp

print(intArray)
print("Done")