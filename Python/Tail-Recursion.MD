The goal of tail recursion is to have calculated the final answer when the floor condition is reached. When the end of the recursion is reached, the function calls do not (in theory) have to cascade up the stack to return the final value because the final value has already been calculated. In some programming languages like Haskell, this approach allows the compiler to optimize the recursion by using a goto rather than creating a new stack frame on each recursion. This in turn allows recursion to reach an indefinite depth without overflowing the available memory.

To illustrate, here is a factorial function designed with tail recursion:

```python
def factorial(n, previous = 1):
    print("n =", n, ", previous =", previous) 
    if n == 1:
        return previous
    else:
        return factorial(n-1, previous*n)
```

Note that I have provided a default argument for the "previous" formal parameter, which allows me to call the function more simply. Here's what happens when I use the function to calculate 4!:

factorial-output.PNG

The first parameter *(n)* is used to keep track of when the floor condition is reached. The second parameter *(previous)* is used to accumulate the value that gets returned.

Tail recursion usually does not avoid call stack growth in Python. The Python language architect, Guido von Rossum, [has described in detail](http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html) why he does not plan to ever introduce tail recursion optimization in Python. If Guido is against it, it's not going to happen.

You can, however, roll your own tail recursion optimization by using advanced Python features. See [this blog post](http://www.kylem.net/programming/tailcall.html) for details if you are interested.
