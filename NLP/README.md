# Natural Language Processing

Much of the approximately [60 zettabytes](https://www.seagate.com/our-story/data-age-2025/) of data in the world in 2021 exists in the form of unstructured or semi-structured documents, which may be in text or audio format (web pages, emails, voice recordings, Facebook posts, podcasts, tweets, and so forth). Natural language processing (NLP) entails text analytics and/or machine learning with these data. Traditional topics in NLP include document search, machine translation, voice recognition, text classification, sentiment analysis, and text-to-speech, among others.

This section of the repo contains explorations and insights in NLP.

## Supervised Text Classification

A document corpus often come with a label of some kind: 
* Is an email spam or not? 
* What is the geolocation of a tweet?
* Is a social media post fake news or real?

The goal would be to train a classifier that can be deployed to predict at scale whether new emails are spam, where tweets without location tags were tweeted from, whether a viral news article should be given a warning label, etc.

To improve model accuracy, text classification projects typically use a preprocessing pipeline to reduce noise. A pipeline for a bag-of-words analysis might include steps such as:
* Lower-case all alphabetical characters
* Expand contractions
* Remove stop words (a/an/the, helping verbs, pronouns, etc.)
* Remove punctuation
* [Stem](https://en.wikipedia.org/wiki/Stemming) or [lemmatize](https://en.wikipedia.org/wiki/Lemmatisation) words 

An alternative for relatively short documents such as tweets is to use a transformer neural network to produce a document embedding, then use the embeddings as inputs to the classifier. This approach cannot be used with long documents because transformers have a quadratic computational complexity (or as computer scientists say, they are of order O(n<sup>2</sup>)), limiting their input to only 512 word pieces, which is roughly 300-400 words. However, researchers are experimenting with advanced architectures that could increase the input length to 1024 word pieces ([Extended Transformer Construction](https://www.groundai.com/project/etc-encoding-long-and-structured-inputs-in-transformers/5)) or 2304 word pieces ([Transformer-XL](https://www.aclweb.org/anthology/P19-1285.pdf)).

Explore text classification with me by checking out these projects:
+ [Document Classification with Naive Bayes](https://github.com/chrisfalter/DataScience/tree/master/NLP/Classification/NaiveBayes) - Look through this project if you want to understand how the Naive Bayes algorithm works and how it can be applied to the geolocation of tweets.
+ [Battle of the Tweet Classification Algorithms](https://github.com/chrisfalter/DataScience/blob/master/NLP/Classification/Battle_of_Tweet_Classification_Algorithms.ipynb) - Having written an implementation of the Naive Bayes algorithm to predict the geolocation of test tweets from a tweet corpus, I thought it would be interesting to compare it to other algorithms. This experiment uses scikit-learn's model selection features to compare the following algorithms:
  + Naive Bayes
  + Adaboost
  + Random Forest
  + K-Nearest Neighbors
  + Gradient Boost
  + Model Stack of Best 3 Models
+ [Spam Classification with PySpark](https://github.com/chrisfalter/DataScience/blob/master/ML_Spark/SpamClassifier_SPARK.ipynb) - This notebook uses logistic regression to build a spam classifier against the CSMDC 2010 Spam data set, which has 4327 labeled observations. It uses the `PySpark` interface to Spark MLLib, which provides a lot of "big data" functionality. However, the exploration runs into some serious shortcomings in `pyspark.mllib` for real-world use. Fortunately, Spark also provides updated machine learning functionality in the `pyspark.ml` library, which future notebooks may explore.

## Topic Analysis

No topic labels? No problem! You can use a method such as latent semantic analysis (LSA) or latent Direchlet analysis (LDA) to assign documents to _latent_ topics. The basic intuition of these methods is that "Each document can be described by a distribution of topics, and each topic can be described by a distribution of words." ([link](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-latent-dirichlet-allocation-437c81220158)) 

An important issue with LSA and LDA is how many topics, _k_, to use in the analysis. The most elegant approach is to try a range of values for _k_ and choose the _k_ that maximizes the model's coherence score, a measure of how neatly the documents can be divided into the latent topics. 

LDA has some important practical advantages over LSA:
* Topics are characterized by positive associations with words in LDA. In LSA, a topic can have either positive or negative associations with a word.
* An LDA model can be used to classify previously unseen documents, whereas LSA requires training a _de novo_ model every time new documents are analyzed.

Consequently, I have favored the use of LDA when performing topic analysis. Here are some illustrative notebooks:
+ [Supervised Topic Modeling with Latent Dirichlet Allocation](https://github.com/chrisfalter/DataScience/blob/master/NLP/TopicAnalysis/lda_with_sklearn.ipynb) - This notebook trains a highly accurate LDA model on the BBC corpus of 2225 news articles classified into 5 topics: Politics, Business, Sport, Tech, and Entertainment. It also shows how to explore the word-topic space generated by LDA and how to explore misclassifications.

## Sentiment Analysis

If you want to know how your customers feel about your products, you could read thousands of individual reviews or surveys. And how would you summarize what you have learned? Or you could train a sentiment analysis model to score the data and use the output to summarize how your customers feel. While sentiment analysis typically makes a binary prediction (positive vs. negative) using a classifier such as logistic regression, Amazon reviews provide a finer-grained perspective along a range of scores from 1 star (the most negative) to 5 stars (the most positive). Thus a linear regression model can be used to predict where along the range of sentiment a particular review falls. [This experiment](https://github.com/chrisfalter/DataScience/blob/master/NLP/Sentiment/SentimentAnalysisOfAmazonReviews.ipynb) also demonstrates how to use `sklearn.model_selection.GridSearchCV` to tune a preprocessing pipeline.

## Embeddings
 
In the early days of NLP--not long after the invention of papyrus, it seems by now--words were represented as vectors of length _N_ where _N_ is the vocabulary size. This has two disadvantages: 
1. Semantic relationships between words are unavailable; and 
2. The dimensionality of the data is extremely high. 

Word embeddings with Word2Vec mitigate these problems by embedding each vocabulary word in a much smaller vector space. In this vector space, similar words are mathematically closer than dissimilar words, thereby capturing semantic relationships. [This notebook](https://github.com/chrisfalter/DataScience/blob/master/NLP/Embeddings/word2vec.ipynb) shows how I created a word2vec embedding over the NLTK Inaugural corpus. Here's [the PDF](https://github.com/chrisfalter/DataScience/blob/master/NLP/Embeddings/word2vec.pdf) if you prefer that format, although you'll need to view the annotated T-SNE projection of sample words [here](https://github.com/chrisfalter/DataScience/blob/master/NLP/Embeddings/tsne.png) because the `nbconvert` tool couldn't render the image into PDF.

## Open Domain Question Answering

ODQA has been extremely difficult in practice due to the computational expense of computing embeddings and the mathematical distances between them over a large corpus. However, the latest innovation, dense passage retrieval, makes the computation feasible enough to start running experiments for your business. If your organization manages large case files or other ad hoc large collections of documents, you need to know this stuff! [This PDF](https://github.com/chrisfalter/DataScience/blob/master/NLP/Dense-Passage-Retrieval.pdf) contains the slides for [my ODQA presentation on YouTube](https://www.youtube.com/watch?v=nRAKIfA4faM).
