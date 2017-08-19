# Numpy for the Win!
Typically, data for machine learning are structured as a two dimensional table whose rows are observations and columns are variables. You can also think of the data as a set of vectors, one per observation, having as many dimensions as there are variables. However you conceptualize the data, though, in any data set of significant size you are going to be doing a lot of math over a large table/matrix of data.

To analyze such data, Python beginners might be tempted to write loops and perform an operation on each cell in the table. For all but the most trivial data sets, however, this is a big mistake. Instead, you should use the `numpy` library which is optimized for performing vectorized operations across a tabular structure. Betraying its scientific computing origins, numpy refers to tables of data as *arrays*.

## Numpy vs. Built-in Operations
I wrote a test script to illustrate numpy's superiority to naive looping code:

```python
import numpy as np
from time import perf_counter
      
def arrayMultiplicationLoop(a, b):
    result = np.empty(a.shape)
    rows,cols = a.shape
    for r in range(rows):
        for c in range(cols):
            result[r,c] = a[r,c] * b[r,c]
    return result
    
def arrayMultiplicationVectorized(a, b):
    return a*b
    
def executionTime(f, *args):
    start = perf_counter()
    f(*args)
    return perf_counter() - start
    
a = np.arange(1000000).reshape(1000,1000)
timeVector = executionTime(arrayMultiplicationVectorized, a, a)
timeLoop = executionTime(arrayMultiplicationLoop, a, a)
print("Vectorized wall clock time:", timeVector)
print("Loop wall clock time:", timeLoop)
```

The script creates a 1000 x 1000 array of data, then performs an element-wise multiplication in both looping and vectorized (numpy) fashion. 

### First result: Numpy is faster...by a lot!!
The execution time comparison on my laptop is quite remarkable:

```
Vectorized wall clock time: 0.0024505094793539754
Loop wall clock time: 1.8883722935192255
```

A difference of three orders of magnitude! And not a coincidence: the rank of the array is three orders of magnitude greater than a single cell. In other words, numpy can perform an operation across an entire vector (i.e., a row) basically as fast as Python's built-in operations can perform it on a single cell of data.

### Second result: The code is simpler...by a lot!!
Did you notice how simple the numpy-based function is? It's a single line of code:
```python
def arrayMultiplicationVectorized(a, b):
    return a*b
```
The code that loops over the array and uses built-in operators, on the other hand is far more complex:
```python
def arrayMultiplicationLoop(a, b):
    result = np.empty(a.shape)
    rows,cols = a.shape
    for r in range(rows):
        for c in range(cols):
            result[r,c] = a[r,c] * b[r,c]
    return result
```
Which function would you rather maintain in your codebase?

## Numpy's Notability
Friends don't let friends drink and drive, and they don't let them write Python loops for tabular data structures. Insist on numpy!

## Functional programming made simple by Python
I would also draw your attention to the functional programming that Python makes so interesting. The `executionTime` function takes two parameters: a function f and a set of arguments. It then calculates the processor instruction time needed to call/execute f with the supplied arguments. This allowed me to treat the two different matrix-processing functions (`arrayMultiplicationVectorized` and `arrayMultiplicationLoop`) as objects, passed as arguments to the `executionTime` function. Pretty cool.
