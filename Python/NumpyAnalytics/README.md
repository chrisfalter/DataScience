# Numpy for the Analytics Win!

One of my Python assignments involved the tabulation of various statistics from a de-identified gradebook from an earlier version of the course. I worked hard on the assignment because I wanted my code to be expressive and fluent. The key to using `numpy`, I discovered, is to find and use the numpy functions that can do in a single line what would require 10 lines of code with Python's built-in functions. The resulting numpy code is quite elegant, and looks like it could be written in 15 seconds. Trust me, looks can be deceiving! 

I invite you to look through the code in this /NumpyAnalytics directory. The source in main.py illustrates several important numpy features.

## File handling
The main() function loads the gradebook from a grades.npy file, as seen below. The file had been created from a previous session in which numpy's save function had been used to persist an array representing the gradebook. 


```python
    # load the grades from disk
    gradebook = np.load("./Grades.npy")
```

Subsequent code in main.py/main() persisted  aggregated statistics and data using the numpy save function. For example, the following line of code persists the averageGrades array into a file named "AverageGrades.npy":

```python
    np.save("AverageGrades", averageGrades
```

## Slicing

## Filtering

## Views
You as you can create a view of a SQL table without making a copy of the data, you can create a view of a numpy array by using slicing or filtering. This facilitates analysis of the various fields of data in the array.

```python
    # create views of the gradebook
    weights = gradebook[0,1:] # first row, except for 0,0
    student_ids = gradebook[1:,0] # first column, except for 0,0
    student_ids = np.array([str(x) for x in student_ids])
    scores = gradebook[1:,1:]
```

## Designating an axis of operation

## Element-wise operations
From the calc_weights function
