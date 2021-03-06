# Scala
Although Scala may be considered a niche language (PyPL says it has only 5% of the Python's usage), the niche it occupies is very important!
+ Scala is the native language of Apache Spark and Apache Storm, 2 very important big data platform components.
+ Scala is a functional language that is well-suited for reactive, high-volume processing. Using Scala guides you seamlessly into the parallel processing against immutable data paradigm.
+ Scala compiles directly to Java byte code, so it can make use of _any_ Java library.

At first glance Scala does not look much different than Python, but since I started working with it seriously I have found that it is different enough that you should not attempt to analogize between the two languages. You will find thousands of Stackoverflow questions framed like this: "I can very easily do _X_ in Python, but the Python syntax doesn't work in Scala. What is the Scala one true way?" _This question has no answer because Scala provides a dozen different ways to do any particular task._ But I am confident that perseverance will eventually reap the reward of Scala fluency.

### Scala Adventures
Note that the links take you to zepl.com, which provides free hosting for public, individual Zeppelin notebooks. 

+ [Exploring the Millionsong Data Set](https://www.zepl.com/viewer/notebooks/bm90ZTovL2NocmlzZmFsdGVyLzRhNDRlOGJlMGE3MjQzNjc4MGVmYmMwNWYyMTBlNjBhL25vdGUuanNvbg) - This Scala Zeppelin notebook loads UCI's data into a Spark DataFrame and performs exploratory analysis. Spark DataFrames often process an order of magnitude faster than RDDs, so they're worth knowing.
+ [Regression Model to Predict Year of Song Publication](https://www.zepl.com/viewer/notebooks/bm90ZTovL2NocmlzZmFsdGVyL2FmODNjMjNjNjc3ZjRjYjFiYjk4NjBkNTIzNjg5Y2Q1L25vdGUuanNvbg) - Continuing the exploration of the UCI Millionsong data set, this notebook tests a linear regression model from the `org.apache.spark.ml` library for predicting the year of song publication. The notebook also uses the built-in data munging features of `org.apache.spark.ml.feature` to preprocess data. The various steps form a pipeline of type `org.apache.spark.ml.feature.Pipeline`, whose API is very similar to Python’s scikit-learn Pipeline API. This makes the Spark Pipeline a good toolkit for data scientists.
