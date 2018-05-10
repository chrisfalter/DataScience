# -*- coding: utf-8 -*-
"""
Harness for training/testing neural net without perturbing source control
over orient.py

@author: cfalter
"""
import sys
from nn import NeuralNet
from activations import Tanh, Relu, Sigmoid
from fileIO import readImages, writePredictions
import numpy as np

def main():
    np.seterr(all='raise')
#    action = sys.argv[1].lower() 
    action = 'train'
    actArg, hiddenArg = sys.argv[1:3]
    actArg = actArg.lower()
    activation = Tanh() if actArg == "tanh" else Relu() if actArg == "relu" else Sigmoid()
    hidden = [int(sub) for sub in hiddenArg.split(',')]
    if action == "train":
#        trainFile, paramsFile, modelName = sys.argv[2:5]
        trainFile, paramsFile, modelName = "train-data.txt", "", ""
        model = NeuralNet(activation, hidden)
        trainData = readImages(trainFile)
        model.train(trainData, paramsFile)
    elif action == "test":
        testFile, paramsFile, modelName = sys.argv[2:5]
        model = NeuralNet(Tanh(), hidden)
        testData = readImages(testFile)
        predictions = model.predict(testData, paramsFile)
        writePredictions(predictions, "output.txt")
    else:
        print("Invalid arguments!")

if __name__ == '__main__':
    main()


