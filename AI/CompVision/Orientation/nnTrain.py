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
    action = sys.argv[1].lower() 
    activationArg, hiddenArg = sys.argv[2:4]
    activationArg = activationArg.lower()
    activation = Tanh() if activationArg == "tanh" else Relu() if activationArg == "relu" else Sigmoid()
    hidden = [int(sub) for sub in hiddenArg.split(',')]
    modelName = activationArg
    if action == "train":
        trainFile, testFile = "train-data.txt", "test-data.txt"
        model = NeuralNet(activation, hidden)
        trainData = readImages(trainFile)
        validationData = readImages(testFile)
        model.train(trainData, validationData, modelName)
    elif action == "test":
        testFile, paramsFile = "test-data.txt", activationArg + ".npy"
        model = NeuralNet(activation, hidden)
        testData = readImages(testFile)
        predictions = model.predict(testData, paramsFile)
        writePredictions(predictions, "output.txt")
    else:
        print("Invalid arguments!")

if __name__ == '__main__':
    main()


