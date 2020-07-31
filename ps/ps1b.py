import math
input_number = int(raw_input("Type a number: "))
n = 1
numbers = 2
prime_sum = math.log(2)
while(n < (input_number/2)):
    numbers = 2 * n + 1
    test = 3
    i = 0
    while(test <= math.sqrt(numbers)):
        if ((numbers % test) != 0):
            test = test + 2
        else:
            i = -1
            break

    n = n + 1
    if (i == 0):
        prime_sum = prime_sum + math.log(numbers)
print prime_sum
print input_number
        
        
        
