# Natural Language Processing
Much of the approximately 30 zettabytes of data in the world exists in the form of unstructured or semi-structured documents, which may be in text or audio format (web pages, emails, voice recordings, Facebook posts, podcasts, tweets, and so forth). Natural language processing (NLP) is the interaction of machine learning with these data. Traditional topics in NLP include document search, automated translation, voice recognition, text classification, and text-to-speech; in 2018, the cutting edge of NLP includes chatbots and a Google assistant [that can schedule a haircut or make a restaurant reservation](https://www.youtube.com/watch?v=VZ9MBYfu_0A). 

This section of my repo contains my explorations and insights in NLP.

### Topics:
+ [Document Classification with Naive Bayes](https://github.com/chrisfalter/DataScience/tree/master/NLP/NaiveBayes) - One of the main NLP tasks is document classification. Look through this project if you want to understand how the Naive Bayes algorithm works and how it can be applied to the geolocation of tweets.
+ [Battle of the Tweet Classification Algorithms](https://github.com/chrisfalter/DataScience/blob/master/NLP/Battle_of_Tweet_Classification_Algorithms.ipynb) - Having written an implementation of the Naive Bayes algorithm to predict the geolocation of test tweets from a tweet corpus, I thought it would be worthwhile to see how it compares to other algorithms that can be used for document classification. This experiment uses scikit-learn's model selection features to compare the following algorithms:
  + Naive Bayes
  + Adaboost
  + Random Forest
  + K-Nearest Neighbors
  + Gradient Boost
  + Model Stack of Best 3 Models
