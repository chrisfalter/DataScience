#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:44:07 2017

@author: Chris Falter 
"""
import nltk
import sys
from TweetClassifier import TweetClassifier

def printWordsForLocation(location, words):
    print("Location: " + location + " Top 5: " + str(words))
    

def main():    
    trainPath, testPath, outputPath = sys.argv[1], sys.argv[2], sys.argv[3]
    classifierDynamic = TweetClassifier(True)
    with open(trainPath, 'r', encoding='latin1', newline='\n') as trainTweets:
        classifierDynamic.train(trainTweets)
    with open(testPath, 'r', encoding='latin1', newline='\n') as testTweets:
        predictionsDynamic = classifierDynamic.predict(testTweets)    
    correctDynamic = sum([p.predicted == p.actual for p in predictionsDynamic])
    print("Accuracy of dynamic feature generation = " + str(correctDynamic / len(predictionsDynamic)))

    classifierStatic = TweetClassifier(False)
    with open(trainPath, 'r', encoding='latin1', newline='\n') as trainTweets:
        classifierStatic.train(trainTweets)
    with open(testPath, 'r', encoding='latin1', newline='\n') as testTweets:
        predictionsStatic = classifierStatic.predict(testTweets)    
    correctStatic = sum([p.predicted == p.actual for p in predictionsStatic])

    if correctStatic > correctDynamic:
        predictions = predictionsStatic
        correct = correctStatic
        classifier = classifierStatic
    else:
        predictions = predictionsDynamic
        correct = correctDynamic
        classifier = classifierDynamic

    print("Accuracy = " + str(correct / len(predictions)))
       
    # print top 5 predicted words per location
    top5PerLocation = classifier.top5PerLocation()
    for loc in top5PerLocation:
        printWordsForLocation(loc, top5PerLocation[loc])
        
    with open(outputPath, 'w', encoding='latin1') as output:
        for p in predictions:
            output.write(' '.join([p.predicted, p.actual, p.tweet]))
        
if __name__ == "__main__":
    main()
