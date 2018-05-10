# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 01:18:49 2017

@author: cfalter
"""

import numpy as np
from scipy.special import expit
import math

class Activation():
    
    def __init__(self, atype):
        '''
        atype = instance of Tanh, Relu, or Sigmoid
        '''
        self.atype = atype
        
    def activate(self, X, W, b):
        '''
        Represents the activation of a neural layer
        
        Inputs:
            X - array of data
            W - array of weights
            b - array of bias neurons
        
        Output:
            output of nodes after activation function is applied
        '''
        return self.atype.activate(X.dot(W) + b)
    
    def dAHidden(self, A_in, A_out, E_next, W):
        '''
        E - array of Error being propagated back from next layer
        W - array of weights leading from this layer to the layer that is source of E
        Z - array of outputs from this layer
        returns 2 arrays: inputs.T .* errors, errors
        '''
        E = E_next.dot(W.T) * self.atype.derivative(A_out)
        deltas = A_in.T.dot(E)
        return deltas, E
    
    def dO(self, Y, T, H):
        '''
        gradient from output back to nearest hidden layer
        T - ground Truth
        Y - activations (predictions) of output layer
        H - activations from nearest/last hidden layer
        returns 2 arrays: inputs.T .* errors, errors
        '''
        E = Y - T
        return H.T.dot(E), E # Y - T = derivative of softmax 
    
    def initializeWeights(self, N, Nplus1, numLayers):
        '''
        N - number of nodes in this layer
        Nplus1 - number of nodes in next layer
        '''
        return self.atype.initializeWeights(N, Nplus1, numLayers)
    
    def learningRate(self, epoch):
        return self.atype.learningRate(epoch)
    
    def biasFactor(self):
        return self.atype.biasFactor()
        

class Tanh():
    
    def activate(self, Z):
        return np.tanh(Z), Z
    
    def derivative(self, Z):
        return 1 - Z*Z # https://github.com/lazyprogrammer/machine_learning_examples/blob/master/ann_class/backprop.py
    
    def initializeWeights(self, N, Nplus1, numLayers):
        # Glorot algorighm; see https://intoli.com/blog/neural-network-initialization/
        bound = math.sqrt(6 / (N + Nplus1))
        return np.random.uniform(-bound, bound, (N, Nplus1))
    
    def learningRate(self, epoch):
        return 8e-2 / (40.0 + epoch)
    
    def biasFactor(self):
        return 0.1
    
class Relu():
    
    def activate(self, Z):
        return Z * (Z > 0), Z
    
    def derivative(self, Z):
        return Z > 0 # https://github.com/lazyprogrammer/machine_learning_examples/blob/master/ann_class/backprop.py
    
    def initializeWeights(self, N, Nplus1, numLayers):
        # uniform distribution, slight skew toward positive suggested by https://intoli.com/blog/neural-network-initialization/
        bound = math.sqrt(6 / N)
        skew = bound / (10 * numLayers)
        return np.random.uniform(skew - bound, skew + bound, (N, Nplus1))

    def learningRate(self, epoch):
        return 8e-3/ (2.0 + epoch)
    
    def biasFactor(self):
        return 1.0
    

class Sigmoid():
    
    def activate(self, Z):
        return expit(Z), Z
        
    def derivative(self, Z):
        try:
            return Z * (1 - Z) # https://github.com/lazyprogrammer/machine_learning_examples/blob/master/ann_class/backprop.py
        except:
            return 100 * np.ones(Z.shape)
 
    def initializeWeights(self, N, Nplus1, numLayers):
        # Glorot algorighm; see https://intoli.com/blog/neural-network-initialization/
        bound = math.sqrt(6 / (N + Nplus1))
        return np.random.uniform(-bound, bound, (N, Nplus1))

    def learningRate(self, epoch):
        return 1e-2 * (100.0 + epoch)
    
