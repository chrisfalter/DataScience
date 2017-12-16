# A Gentle Introduction to Numpy for Analytics

One of my Python assignments involved the tabulation of various statistics from a de-identified gradebook. Wanting to find an expressive and fluent syntax for analyzing data, I explored the `numpy` library. Serendipity! I learned that a single line of numpy can accomplish as much as several lines of built-in Python. The result is not only more efficient computationally, it is often easier to understand at a glance, which means it's good code. As Martin Fowler explains, _"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."_

I invite you to look through the code in this /NumpyAnalytics directory. The source in Question.py illustrates several important numpy features. Note that all the examples in this post assume the almost universal namespace import: `import numpy as np`.

## File handling
The numpy file IO functions use a binary format by default, yielding great efficiency in data persistence. My code illustrates a simple way to use this efficiency.

The Question.py/main() function loads the gradebook from a file named grades.npy, as seen below. The file had been created by using numpy's `save()` function to persist an array representing the gradebook. We'll see more on this function a little further on.


```python
    # load the grades from disk
    gradebook = np.load("./Grades.npy")
```

The resulting gradebook variable is of type `numpy.ndarray`, which means it's ready for immediate use in a data pipeline.

Subsequent code in Question.py/main() persists aggregated statistics and data using the numpy save function. For example, the following line of code persists the averageGrades array into a file named "AverageGrades.npy":

```python
    np.save("AverageGrades", averageGrades
```
Note that if you do not provide a file extension, the numpy `save` function appends the default `.npy`.
## Slicing
Once the gradebook array is loaded, my analysis obtains a slice of data via a numerical indexing.  For example, this line of code sets the `scores` array to be all observations from index 1 to the end (written `[1:]`) in both dimensions of the array.
```python
scores = gradebook[1:,1:]
```
By convention, the rows and columns of a two-dimensional data set are the first and second indexes of an array, respectively. Since Python uses zero-based indexing, the above line of code incorporates all but the first row and column of the `gradebook` array into the `scores` array. This table provides examples of slicing a numpy array by passing a range or single number to its bracket indexer.
Slice Notation | What You Get
--------------------|----------------
`my_array[:,:]` | A view of all the data in `my_array`
`my_array[0,:]` | The first row
`my_array[1,:]` | The second row
`my_array[1:2,:]` | The second row (the final number in a range acts as a stop sign)
`my_array[0:2,:]` | The first 2 rows
`my_array[-1,:]` | The last row (start at the end, count back one)
`my_array[0:-2,:]` | All but the last 2 rows
`my_array[:-2,:]` | All but the last 2 rows (the leading 0 is optional)
`my_array[:,0]`| The first column
`my_array[:,-1]`| The last column
`my_array[:,-3:]`| The last 3 columns
`my_array[5:-1,-2:]`| The last 2 columns of the 6th thru next-to-last rows


## Views
Just as you can create a view of a SQL table without making a copy of the data, you can use slicing to create a view of a numpy array without copying it. This facilitates analysis of the various fields of data in the array at minimal cost in memory I/O and computation time. The following code from Question.py creates three different views of the gradebook array without any copying:

```python
    # create views of the gradebook
    weights = gradebook[0,1:] # first row, except for 0,0
    student_ids = gradebook[1:,0] # first column, except for 0,0
    student_ids = np.array([str(x) for x in student_ids]) # creates a new array
    scores = gradebook[1:,1:] # all but the first row and first column
```
Updating an element in the `weights` array would also update the corresponding element in the `gradebook` array, since `weights` is a view into `gradebook`.
## Selection by Index
By passing a numeric list or array to an array bracket indexer, you can select specific rows and/or columns. 
```python
COLS_Labs = np.arange(6,17) # 6 ... 16
# skipping some code in Question.py
group = weights[COLS_Labs] # returns a copy of weights[6:17] 
```
It's important to note that the array returned by the selection operation is a *new* array,  not a view into the array that was sub-selected. In the code above, therefore, updating a value in the `group` array would *not* update corresponding values in the `weights` array.
## Filtering by Value
Numpy provides a variety of ways to filter array data. In the gradebook assignment, I wanted to substitute a reasonable default for invalid values. The following line of code assumes that all values greater than 102 or less than 0 are invalid, and sets them to 0:
```python
scores = np.where(np.logical_or(scores < 0, scores > 102), 0, scores)
```
To understand the code, work your way from the inside to the outside. The [np.logical_or function](https://docs.scipy.org/doc/numpy/reference/generated/numpy.logical_or.html) returns an array of boolean True or False shaped like the array to which the logical predicates are applied. Thus it returns a True wherever the value in an array cell is less than 0 OR greater than 102, and returns False otherwise. Applying the operation to a `scores` array with these values...
```
[ -0.5,  78.3, 94]
[101.8, 139.4, 67]
```
...would yield the following array of boolean:
```
[True, False, False]
[False, True, False]
```
Now we move to the outer function, [np.where](https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html), which takes three positional arguments: 
1. a condition array of boolean type that provides the shape of the output array
2. a value or array of values used to populate the output array wherever the condition array is `True`.
3. a value or array of values used to populate the output array wherever the condition array is `False`.

In our 2 row by 3 column example, a True in the condition array yields a 0 (2d argument) in the output array, and a False  yields the corresponding value from the `scores` array (3d argument). So the final result is:
```
[    0, 78.3, 94]
[101.8,    0, 67]
```
It would be reasonable to argue that a 0 is not the best default for invalid values; perhaps the mean or median value of the column would be more appropriate. Coming up with a plausible default for invalid or missing values is why data analysis will always mix a little art and intuition in with the math.
## Designating an axis of operation
Numpy provides a large set of functions (`sum`, `mean`, `median`, `max`, `min`, `std` [standard deviation], etc.) that can be applied over values in an array. By default, these are applied to all the values in all dimensions of the array. If we apply the function `np.sum` to the output `scores` array from the previous section, for example, we get the scalar  341.1:
```python
sumOfScores = np.sum(scores) # 341.1 = 0 + 78.3 + 94 + 101.8 + 0 + 67
```
However, you can apply a function along an axis to return an _array_ of values that has one fewer dimension than the input array.
```python
studentGrades = np.mean(scores, axis = 1) # returns the mean along each row 
print(studentGrades)                      # [57.433, 56.267]
```
57.433 is the mean of the first row (0, 78.3, and 94), while 56.267 is the mean of the second row (101.8, 0, and 67).  Alternatively, you could apply the mean along the columns by passing the argument axis = 0:
```python
averageAssignmentScores = np.mean(scores, axis = 0) # returns the mean along each column 
print(averageAssignmentScores)                      # [50.9, 39.15, 80.5]
```
50.9 is the mean of the first column (0 and 101.8), 39.15 is the mean of the second column (78.3 and 0), and 80.5 is the mean of the third column (94 and 67).
## Element-wise operations
From the calc_weights function 
