#!/usr/bin/env python3
"""
Task: Train a classifier that will predict the orientation of an image (0, 90, 180, or 270)
To train: ./orient.py train train_file.txt model_file.txt [model]
where [model] is one of nearest, adaboost, nnet, or best.
Output is [model]_file.txt, which will contain :
    * optimized parameters determined by training
    * (if necessary, for example with KNN) training data

To test: 
./orient.py test test_file.txt model_file.txt [model]
output: file output.txt which indicates the estimated label for each image in 
the test file. The output file should correspond to one test image per line,
with the photo id, a space, and then the estimated label, e.g.:
test/124567.jpg 180
test/8234732.jpg 0

@author: Alex DeCourcy, Anthony Duer, Chris Falter
"""
import sys
from knn import KNN
from adaboost import Adaboost
from nn import NeuralNet
from best import Best
from activations import Relu
from fileIO import readImages, writePredictions
from Prediction import checkAccuracy

models = {"nearest": KNN(),
          "adaboost": Adaboost(),
          "nnet": NeuralNet(Relu(), "192,192"),
          'best': Best()}

def main():
    action = sys.argv[1].lower() 
    if action == "train":
        trainFile, paramsFile, modelName = sys.argv[2:5]
        model = models[modelName]
        trainData = readImages(trainFile)
        model.train(trainData, paramsFile)
    if action == "test":
        testFile, paramsFile, modelName = sys.argv[2:5]
        model = models[modelName]
        testData = readImages(testFile)
        predictions = model.predict(testData, paramsFile)
        checkAccuracy(testData, predictions)
        writePredictions(predictions, "output.txt")

if __name__ == '__main__':
    main()
