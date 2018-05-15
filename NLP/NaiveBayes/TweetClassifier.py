# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:24:52 2017

@author: Chris Falter
"""
import re
from collections import Counter, defaultdict
from nltk.corpus import stopwords
from nltk import download
import string
import numpy as np
import pandas as pd

class Prediction():
    
    def __init__(self, predictedLocation, actualLocation, tweet):
        self.predicted = predictedLocation
        self.actual = actualLocation
        self.tweet = tweet

def getLocationAndTweet(s):
    '''
    Returns a tuple (location, tweet)
    location = first token in string s
    tweet = remainder of string s
    '''
    divider = s.find(' ')
    return s[:divider], s[divider + 1:] 

specialEntitiesRegex = re.compile("&[a-z]+;")

def removeSpecialEntities(s):
    m = specialEntitiesRegex.search(s)
    while (m):
        s = s[:m.start()] + s[m.end():]
        m = specialEntitiesRegex.search(s)
    return s

cityInitials = ['la', 'orl', 'washing']

def identifyCityInitials(tokens):
    initialList = []
    for token in tokens:
        for initials in cityInitials:
            if token.startswith(initials):
                initialList.append(initials)
    if (initialList):
        return tokens + initialList
    return tokens

def identifyMonikers(tokens, monikers):
    monikerList = []
    for tok in tokens:
        for moniker in monikers:
            if moniker in tok:
                monikerList.append(moniker)
    if monikerList:
        return tokens + monikerList
    return tokens        

# make sure the list of stop words is available
download("stopwords")

printable = set(string.printable)
punc = string.punctuation.replace(' ','') # don't remove spaces! They demarcate words
punctuationRemover = str.maketrans(punc, ' '*len(punc))
commonTweetWords = ['job','hiring','jobs','careerarc','street','opening','work','apply','st'] 
commonTweetWords += list("abcdefghijklmnopqrstuvwxyz") + list("01234456789")
stopWords = set(stopwords.words('english') + commonTweetWords)

parsedLocations = set()
def parseLocationMonikers(location, monikers):
    if location in parsedLocations:
        return
    extractMonikersFromLocation(location, monikers)
    parsedLocations.add(location)

def extractMonikersFromLocation(location, monikers):
    # remove the comma(s) and lower-case
    location = location.replace(',', '').lower()    
    # get the individual words
    tokens = location.split('_')
    for t in tokens:
        if len(t) > 4:
            monikers.add(t[0:4])
        else:
            monikers.add(t)
    numTokens = len(tokens)
    if numTokens > 2:
        abbreviation = ''
        numInitials = numTokens - 1
        for i in range(numInitials):
            abbreviation += tokens[i][0]
        monikers.add(abbreviation)

class TweetClassifier():
    '''
    train() method determines priors for P(location), P(token | location)
    test() method applies naive Bayes classification to each tweet
    '''
    
    def __init__(self, isDynamicLocations = False):
        '''
        Inputs:
            tokenOccurrenceThreshold = minimum number of occurrences of token 
            for it to be used in predicting location
        '''
        self.tokenOccurrenceThreshold = 1
        
        # accumulators
        self.numTweets = 0
        self.tweetCounts = Counter()
        self.wordCount = Counter()
        self.tokens = defaultdict(Counter)
    
        # probability tables
        self.locationPrior = None # will be a ndarray of log(P(location))
        self.tokenPriors = {} # dictionary: key = token, value = ndarray of P(token|location)
        
        # dictionary to keep track of locations
        self.locations = dict()
        
        # extracting monikers
        self.isDynamicLocations = isDynamicLocations
        if isDynamicLocations:
            self.monikers = set()
        else:
            self.monikers = set(['ny','york','manh',
            'dc',
            'bost',
            'chic','illin',
            'hollw','angel',
            'orlan','fl',
            'sf','bay','fran',
            'tl','georgia',
            'houst','tx','tex',
            'phil','delph','penn',
            'sd','dieg',
            'toro','canad','ontar'])
        
    def _getTokens(self,tweet):
        '''
        Returns a list of tokens after removing punctuation and stopwords + lower-casing
        '''
        # TODO: try stemming the words
        # remove HTML special entities (such as '&gt;') first
        s = removeSpecialEntities(tweet)
        # strip unprintable characters
        s = ''.join(filter(lambda x: x in printable, s))
        # lower-case so that each use of a word is coalesced, regardless of case
        s = s.lower()
        # remove punctuation
        s = s.translate(punctuationRemover)
        # tokenize + remove stop words
        tokens = list(filter(lambda t: t not in stopWords, s.split()))
        tokens = identifyCityInitials(tokens)
        tokens = identifyMonikers(tokens, self.monikers)
        return tokens

    def train(self, tweets):
        '''
        Returns dictionary of token/key to [dictionary of locations (keys) to
        likelihood of appearing in a tweet from that location (value)] as value
        
        Input:
            tweets - list of strings. First token = location, remainder = tweet
        '''
        for t in tweets:
            self.numTweets += 1
            loc, tweet = getLocationAndTweet(t)
            self.tweetCounts[loc] += 1
            if self.isDynamicLocations:
                extractMonikersFromLocation(loc, self.monikers)
            for token in self._getTokens(tweet):
                self.wordCount[loc] += 1
                self.tokens[token][loc] += 1  
        self._calculateProbabilities()                          
        
    def predict(self, tweets):
        '''
        Returns list of Prediction objects
        
        Input:
            tweets = list of tweets. First token = location, remainder = tweet
        '''
        result = []
        for t in tweets:
            loc, tweet = getLocationAndTweet(t)
            prediction = self._predictLocation(tweet)
            result.append(Prediction(prediction, loc, tweet))
        return result
    
    def _calculateProbabilities(self):
        '''
        Calculate the following prior probabilities:
            * Probability of a tweet (regardless of content) being from a location.
              Must be calculated for each location, should sum to 1.0 over all locations
            * Probability that a token will be in a tweet, given a location
              Must be calculated for each token whose count exceeds min threshold,
              over all locations
        Token probabilities will omit tokens that occur less than the threshold
        Token probabilities will use LaPlace smoothing to allow predictions to use
            logarithms, which will prevent underflow (see 
        https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html)
        '''
        locationDistribution = []
        for i, location in enumerate(self.tweetCounts):
            self.locations[i] = location
            locationDistribution.append(self.tweetCounts[location] / self.numTweets)
        self.locationPrior = np.log(np.array(locationDistribution))
        
        # Laplace smoothing step 1: add number of terms to word count
        sizeVocabulary = len(self.tokens)
        for key in self.wordCount:
            self.wordCount[key] += sizeVocabulary 
        
        # Laplace smoothing step 2: add 1 to number of occurrences for each word, each location
        # will do this while building the probability tables for P(token | location)
        for token in self.tokens:
            wordBag = self.tokens[token]
            if sum([wordBag[k] for k in self.tweetCounts]) < self.tokenOccurrenceThreshold:
                continue
            priors = [(wordBag[loc] + 1) / self.wordCount[loc] for loc in self.tweetCounts]
            self.tokenPriors[token] = np.log(np.array(priors))                
    
    def _predictLocation(self, tweet):
        tokens = self._getTokens(tweet)
        #numTokens = len(tokens)
        estimates = self.locationPrior.copy()
        for token in tokens:
            tokenPriors = self.tokenPriors.get(token)
            if not tokenPriors is None:
                estimates += tokenPriors
        return self.locations[np.argmax(estimates)]                    
    
    def top5PerLocation(self):
        '''
        Returns a dictionary:
            key = location
            value = list of 5 words that predict most highly for the location
        '''
        # the result
        top5Dict = {}
        # for translating column from numbers to city names
        cityDict = {}
        cities = list(self.tweetCounts.keys())
        for i, city in enumerate(cities):
            cityDict[i] = city
        # DataFrame with rows = word probabilities, columns = locations
        # Instantiate from the tokenPriors dict, 
        # with key = word and value = ndarray of probabilities (one per location)
        vocabDf = pd.DataFrame.from_dict(self.tokenPriors, orient='index').rename(columns = cityDict)
        for city in cities:
            # create a DataFrame with one column containing the top 5 values
            # for one location
            dfCity = vocabDf[[city]].nlargest(20, columns = city)
            # The index consists of the 5 words that are associated with the 
            # values. Those are the words we seek!
            top5Dict[city] = list(dfCity.index)
        return top5Dict
        
        
