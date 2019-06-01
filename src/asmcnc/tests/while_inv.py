import time
from random import randint

count_1 = 0
count_2 = 0

def my_func(count_1, count_2):
    
    print('count = ' + str(count_1))    
    
    time.sleep((randint(0,4))/2)
    
    print('count = ' + str(count_2))
    

while True: 
    my_func(count_1, count_2)
    
    count_1 += 1
    count_2 += 1  
    

