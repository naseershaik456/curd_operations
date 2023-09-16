# Here print prime numbers range of a numbers

def prime(a):
    space = ""
    for i in range(a):
        if i == 0 or i == 1:
            continue
        else:
            for j in range(2,int(i/2)+1):
                if i % j == 0:
                    break
            else:
                space = space + str(i) + " "
    return space
                    
a = int(input())
result = prime(a)
print(result)