# Introduction to Python Unit Testing
When I was a wee programming lad, no one I knew wore bicycle helmets or wrote automated tests. You just wrote your code, tested it at your workstation, committed it, and crossed your fingers while the test team did its work. We live in an enlightened age now, and realize that unit tests help you design and document reliable code that can be maintained. Did you notice all the wonderful qualities I jammed into one sentence? Good design, good documentation, reliability, maintainability. No wonder everyone is monitoring unit test code coverage! And folks are wearing bicycle helmets, too. 

Naturally, Python provides unit test functionality. The simplest way is to write a test class that inherits from unittest.TestCase. This provides two capabilities:

1. The test class inherits functionality such as the ability to call self.assertEquals() and self.assertListEquals().
2. unittest.main() can identify test functions that should be included in the test run. Specifically, it finds every function whose name begins with "test" and executes it.

Here's the unit test class I wrote for an early assignment in my IU Python class:

```python
# file: test_assignment5.py

import unittest
import Assignment5 as a5
import Question5 as q5

class test_assignment5(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_sumList(self):
        args_map = [([1,2,3], 6), 
                    ([-1.2, 1.2, 2.0], 2.0), 
                    ([-2,2,3.4], 3.4)]
        for args in args_map:
            self.assertEqual(a5.sumList(args[0]), args[1], "failed on args {}".format(args))
            
    def test_squareEach(self):
        args_map = [([0.5,1,2], [0.25,1,4]), ([-2,0,2.5,100], [4,0,6.25,10000])]
        for args in args_map:
            a5.squareEach(args[0])
            self.assertListEqual(args[0], args[1])
            
    def test_convert_to_number_list(self):
        args_map = [('1 3 5 -4 7 -11', [1,3,5,-4,7,-11]), ('', [])]
        for args in args_map:
            self.assertListEqual(a5.convert_to_number_list(args[0]), args[1])
            
    def test_toNumbers(self):
        args_map = [(['1','0','-2','25'], [1, 0, -2, 25]), ([], [])]
        for args in args_map:
            a5.toNumbers(args[0])
            self.assertListEqual(args[0], args[1]) 
            
    def test_countDigits(self):
        args_map = [("213 Goldfinch Ln, Summerville", 3), ('', 0), ("!@$!@#%^4567890 BVNKROFU", 7)]
        for args in args_map:
            self.assertEqual(q5.countDigits(args[0]), args[1], "failed on args {}".format(args))
        

if __name__ == '__main__':
    unittest.main()
```

For this initial stab at Python unit tests, I wrote a single test function for each function under test. Arguments and expected values are grouped as a tuple, and multiple test scenarios can be played for a function by iterating through a list of argument/expected-value tuples. At the cost of ease of comprehension, this methodology facilitates the quick creation of a relatively complete set of tests for a function library. For a later assignment I wrote unit tests in a way that maximizes comprehension. Stay tuned!

If you'd like to play with my code, just download [the function libraries and test class](https://github.com/chrisfalter/DataScience/blob/master/Python/IntroToUnitTest/IntroToUnitTests.zip), unzip them to a directory of your choice, navigate to that directory, and run the following command:

`$ python test_assignment5.py`

Make sure you have Python 3.5 or higher installed. The test run writes helpful output to the console. When all is well, you'll see something like this:

```
$ python test_assignment5.py

.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```
