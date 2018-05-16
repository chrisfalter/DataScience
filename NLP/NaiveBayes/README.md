## Document Classification with Naive Bayes
One of the main tasks in natural language processing is the classification of documents. Here are some examples:
+ Email routing: e.g., gMail routes emails (considered documents) to Inbox, Social, Promotions, or Spam tabs
+ Language identification: identifying the language in which a document has been written
+ Readability assessment: identifying the grade level at which a reader can be expected to understand a document

In this exercise we will be classifying the geographical origin of tweets using the Naive Bayes algorithm.
### Bayes Theorem
Let's start by reviewing Bayes Theorem. The standard equation is...

![Bayes equation](Bayes_equation.jpg?raw=true)

...which reads like this: "The probability of A (given B) equals the probability of B (given A) times the probability of A, divided by the probability of B"

Bayes Theorem gives you a framework for updating a belief when you observe new evidence for or against the belief, as demonstrated by the following formulation of the theorem:

![Bayes in English](Bayes_in_English.jpg?raw=true)

Let's define the terms:
+ **Prior probability** is the measure of our belief about some hypothesis *A* before we observe new evidence *B*. It corresponds to *P(A)* in the standard formulation. 
+ A **Likelihood function**  measures the probability that the evidence *B* would be observed, given the existence of *A*. This supports the intuitive notion that the greater the likelihood, the more the posterior belief in the hypothesis will increase.
+ The **Evidence function** measures the probability that the evidence *B* would be observed, independent of *A* or *not-A*. The fact that it is in the denominator supports the intuitive notion that the more likely the observation of *B* is--independent of *A*--the less the observation can be used to support hypothesis *A*.
+ The **Posterior probability** is the measure of our belief in hypothesis *A* now that we have observed evidence *B*.

If you would like to explore Bayes Theorem beyond this brief summary, blogger Li Chun provides[ a nice example and explanation](http://www.lichun.cc/blog/2013/07/understand-bayes-theorem-prior-likelihood-posterior-evidence/).

### The Naive Bayes Algorithm
When an observation *B* is multinomial, you can substitute the dimensions of B (b<sub>1</sub>, b<sub>2</sub>, etc.) as a set in place of B:

![Multinomial Bayes Equation](Multinomial_Bayes.jpg?raw=true)

If you must consider all of the interactions between B's dimensions, applying this equation to a hypothesis becomes extremely complex. But you can simplify the equation dramatically by adopting the *naive* assumption that B's dimensions are independent:

![Naive Bayes Equation](Naive_Bayes_Equation.jpg?raw=true)

While this independence assumption of Naive Bayes is not true in every case, it is true frequently enough that it supports a surprisingly accurate prediction model. At the same time, the algorithm is ready to make predictions just by calculating all of the priors and likelihoods in a single pass through the observations. It has a time complexity of O(ns), where n = the number of documents and s = average size of a document. In other words, its time complexity is linear, which makes Naive Bayes a highly attractive algorithm for classifying very large document corpora. Indeed, my implementation is able to evaluate approximately 36,000 train and test tweets in just a few seconds on a laptop.
### Naive Bayes Applied to Tweet Geolocation
Consider a tweet that has 3 words, *w<sub>1</sub>, w<sub>2</sub>, and w<sub>1</sub>*. You want to measure the hypothesis that it was tweeted from a certain metropolis, *city<sub>1</sub>*. Naive Bayes provides the mathematical framework:

![Bayes for tweets](Bayes_for_tweets.jpg?raw=true)

If you are comparing multiple hypotheses for the tweet's geolocation--e.g.., that it might have been tweeted from *city<sub>1</sub>* or *city<sub>2</sub>* or *city<sub>3</sub>*, etc.--then you do not need to calculate the denominator. The posterior for each hypothesis reflects division by the same P(b<sub>1</sub>)P(b<sub>2</sub>)P(b<sub>3</sub>); therefore the denominator can be ignored. Naive Bayes simply predicts the highest probability posterior from among all the candidate hypotheses.

It's worth noting that Naive Bayes is not very good at estimating the actual posterior probabilities, even though it is very good at predicting the best hypothesis.

### Design Decisions
This section discusses the source code in [the TweetClassifier class](TweetClassifier.py) and related functions. The [geolocate.py script file](geolocate.py) simply processes command line arguments, runs the TweetClassifier `train()` and `predict()` methods, and writes output to the console and file system.
#### Data Structures
The TweetClassifier structures each document as a bag of words. Since each tweet is roughly the same 140 character length, there is no need to normalize by number of words in a document. Term frequency-inverse document frequency (TF-IDF) also seems unnecessary in light of the fact that the probability of a word (given each of the 10 cities) already identifies the distribution that matters in the analysis of tweet geolocation.

#### Avoiding Zero Probabilities.
In Naive Bayes the probability of a class, given a document, is the product of the prior probability of the class times the probability of each word in the document given the class. However, for rare words the probability might be zero for almost all of the classes, rendering the class probabilities as zero. Given a tweet with two or more rare words, every class could be evaluated as having a zero probability.

The `_calculateProbabilities()` method in the TweetClassifier class uses Laplace smoothing by adding one to the word occurrence count for each class (city). To avoid imbalances between classes with different sample sizes, the size of the total vocabulary in the corpus is added to the denominator which is used to calculate the probability of a word, given a location.

#### “Dirty” Data
Inspection of a sample of tweets revealed several problems that interfered with accurate prediction:
+ Non-ASCii characters
+ Punctuation characters
+ HTML Special Entities (e.g., “&amp;gt;”)
To address these problems, the TweetClassifier.py source file provides multiple functions to rmove all such characters from the tweets.

#### Lower Case vs. Upper Case
In order to prevent different character case preferences of Twitter users from influencing the analysis, all tweets were lower-cased.

#### Inclusion/Exclusion of Rare Terms
Since extremely rare terms might have undue influence on the analysis, the algorithm was tested by varying the minimum threshold for word appearances in the training corpus. Specifically, accuracy for a threshold of appearances N = { 1 - 20 } was evaluated, and the
maximum accuracy was selected. The threshold of N = 0 provided maximum accuracy, and the accuracy decreased almost monotonically as the appearance threshold increased. This should not be surprising; every small piece of information can increase the accuracy of the analysis.
#### Stop Words
Very common words such as *a*, *an*, and *the* can have an outsize influence on the location probability calculation. Their appearances among the classes can be assumed to have a random distribution. Since random distributions are often at least slightly imbalanced in the real world, the inclusion of stop words can bias the the model's predictions. Consequently, I used the NLTK stopwords module to remove stop words.
#### Feature Generation via Location Name Fragments
Inspection of the tweets shows that users have very inventive and effectively random ways of incorporating place-name fragments into their tweets. For example, a user from Philadelphia might refer to a Philly radio personality as @oracleOfDelphia. A nearby horse farm might have the name @filliesOfDelphia. And so forth.

Thus the use of location name fragments can facilitate accuracy of prediction. An unseen word in a test document that contains “delph” as a substring, for example, likely originates in Philadelphia. Thus the TweetClassifier creates a set of location name fragments and uses them to generate tokens in the tweets being evaluated. This feature generation improved the score on the test data from ~64% to ~70%.

Since the location candidates of future tweet datasets is unknown, the TweetClassifier uses two feature generation strategies: a hard-coded one based on the original set of 12 locations, and a dynamic one. Both strategies are used, and the one which has the
most accurate results is used to write the output. The dynamic feature generation strategy improves the accuracy on the test data from ~64% to ~67%. 

### Instructions for Running the Code
Download the Python and txt files from this directory. Your command-line should include arguments for 3 paths:
+ The training data file
+ The test data file
+ An output file that holds each individual prediction in CSV format.

Use the following syntax:

`python geolocate.py path-to-training-data path-to-test-data path-to-output-file`
