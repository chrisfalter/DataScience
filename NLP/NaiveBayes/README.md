## Document Classification with Naive Bayes
One of the main tasks in natural language processing is the classification of documents. Here are some examples:
+ Email routing: e.g., gMail routes emails (considered documents) to Inbox, Social, Promotions, or Spam tabs
+ Language identification: identifying the language in which a document has been written
+ Readability assessment: identifying the grade level at which a reader can be expected to understand a document

In this exercise we will be classifying the geographical origin of tweets using the Naive Bayes algorithm.
### How Naive Bayes Works
Let's start by reviewing Bayes Theorem. The standard equation is this:
![Bayes equation]("https://github.com/chrisfalter/DataScience/blob/master/NLP/NaiveBayes/Bayes_equation.jpg")

Read like this: "The probability of A, given B, equals the probability of B, given A, times the probability of A, divided by the probability of B"
