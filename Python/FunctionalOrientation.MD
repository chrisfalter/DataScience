In languages such as Java and C#, functions have to belong to some kind of containing structure such as a class. While Python provides the ability to write classes, it also allows you to simply write functions as free-standing code. This kind of flexibility is why so many programmers love Python; you don't have to invest in scaffolding such as class structure unless you really need it. In fact, the ability to just write a few functions and call them forthwith is why Python is so popular as a scripting language.

For my fifth Python assignment at this summer at IU, I decided to implement some simple functions as a library. 

```python
# file: Assignment5.py

def sumList(nums):
    result = 0
    for num in nums:
        result += num
    return result

def squareEach(nums):
    for i in range(len(nums)):
        nums[i] = nums[i]**2
        
def toNumbers(strList):
    for i in range(len(strList)):
        strList[i] = eval(strList[i])
        
def convert_to_number_list(s):
    nums = s.split()
    toNumbers(nums)
    return nums
```

Pythonistos will recognize that these little functions duplicate functionality that built in to the language, but hey! -- it's a learning experience. 

Then I imported the library and used several of the functions to solve the assignment:

```python
# file: main.py

import Assignment5 as a5

def main():
    p = input('Enter a path/name for a file with numbers: ')
    f = open(p, "r")
    print()
    line_num = 1
    for line in f.readlines():
        nums = a5.convert_to_number_list(line)
        a5.squareEach(nums)
        print('Sum of squares in line', line_num, 'is', a5.sumList(nums))
        line_num += 1
    # I should really close the file here!       

if __name__ == '__main__':
    main()
```

It is a best practice to write your code in such a way that resources (such as a file opened for reading) are guaranteed to be closed. I implemented that code in a subsequent assignment. Stay tuned! 
