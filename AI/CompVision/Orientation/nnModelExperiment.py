from Prediction import Prediction, Orientation
from DataFormats import Thumbnail
import numpy as np
from sklearn.utils import shuffle
from activations import Activation

def learningRate(epoch):
    return 4e-3 / (2.0 + epoch)

dPosition = {Orientation.UP.value: 0, Orientation.RIGHT.value: 1, \
             Orientation.DOWN.value: 2, Orientation.LEFT.value: 3}

class NeuralNet():
    
    def __init__(self, atype, hidden):
        '''
        Input:
            atype - Tanh, Relu, or Sigmoid
            hidden - list of hidden layer sizes. E.g., [192, 128, 64] specifies
                     3 hidden layers with 192, 128, and 64 nodes each
        '''
        self.activation = Activation(atype)
        self.hidden = hidden
    
    def train(self, trainData, paramsFile):
        '''
        optimizes a model to prediction orientation of images
        
        Input:
            trainData - list of Thumbnail
            paramsFile - file to which this function writes optimized hyperparameters/weights
        
        Output:
            Method does not return a value; instead, it writes to paramsFile
        '''
        self.initTrainParams(trainData, paramsFile)
        # find loss of randomized NN so we can verify that training works
        Y_pred, _ = self.forward(self.Xvalidate)
        self.bestLoss = self.loss(self.Yvalidate, Y_pred)
        accuracy = self.accuracy(self.Yvalidate, Y_pred)
        self.printLoss("pre", self.bestLoss, accuracy)

        epochs = 500
        batchSize = 10 # use mini-batch gradient descent
        numObservations = len(self.X)
        for epoch in range(epochs):
            # shuffle data
            X, Y = shuffle(self.X, self.Y)
            i, j = 0, 0
            for i in range(0, numObservations - batchSize, batchSize):
                j += batchSize
                # forward
                self.I = X[i:i + batchSize]
                Yhat, hidden = self.forward(self.I)
                # backprop
                self.backprop(Y[i:i + batchSize], Yhat, hidden, epoch)
#                Yhats.append(Yhat)
#                if j % 5000 == 0:
#                    Yt = Y[j - 5000:j]
#                    Y_pred = np.vstack(Yhats)
#                    trainingLoss = self.loss(Yt, Y_pred)
#                    self.printLoss(epoch, j, trainingLoss)
#                    Yhats = []
                    
            # last mini-batch
            i += 10
            self.I = X[i:numObservations]
            Yhat, Z = self.forward(self.I)
            self.backprop(Y[i:numObservations], Yhat, Z, epoch)
            
            # check validation loss
            Yhat_V, _ = self.forward(self.Xvalidate)
            validationLoss = self.loss(self.Yvalidate, Yhat_V)
            validationAccuracy = self.accuracy(self.Yvalidate, Yhat_V)
            self.printLoss(epoch, validationLoss, validationAccuracy)
#            if validationLoss < self.bestLoss:
#                self.printLoss("best validation so far", validationLoss)
#                self.bestWs = self.Ws
#                self.bestBs = self.Bs
#                self.bestLoss = validationLoss
            # MAYBE: if delta-trainingLoss < tolerance, stop training
        # TODO: save params to file
        
    def initTrainParams(self, data, paramsFile):
        # architecture
        numFeatures = len(data[0].pixelArray)
        numHidden = len(self.hidden)
        self.O = 4 # 4 output neurons
        
        # weights + bias neurons
        self.Ws = []
        self.Bs = [] 
        self.Ws.append(self.activation.initializeWeights(numFeatures, self.hidden[0], numHidden + 1))
        self.Bs.append(np.zeros(self.hidden[0]))       
        for i in range(1, numHidden):
            self.Ws.append(self.activation.initializeWeights(self.hidden[i-1], self.hidden[i], numHidden + 1))
            self.Bs.append(np.zeros(self.hidden[i]))
        self.Ws.append(self.activation.initializeWeights(self.hidden[i], self.O, numHidden + 1))
        self.Bs.append(np.zeros(self.O))
        
        # input data and neuron activations will be assigned during training
        self.I =  None 
        self.As = [] 
        self.Zs = []
        
        # training data
        self.X = np.array([data[i].normalize() for i in range(len(data))])
        self.Y = np.array([self.indicatorArray(data[i].orientation.value) for i in range(len(data))])
        self.X, self.Y = shuffle(self.X, self.Y)
        validationSize = 5000
        self.Xvalidate, self.X = self.X[-validationSize:], self.X[:-validationSize]
        self.Yvalidate, self.Y = self.Y[-validationSize:], self.Y[:-validationSize]
        
    def predict(self, testData, paramsFile):
        '''
        returns predictions of orientation for each test image
        
        Input:
            testData - list of Thumbnail
            paramsFile - file with hyperparameters/weights
            
        Output:
            list of Prediction
        '''
        pass
    
    
    def indicatorArray(self, y):
        ''' 
        returns an array:
            length = number of output classes
            all elements are 0.0, except the y-th, which is set to 1.0
            (the 1.0 indicates that y is the ground truth class of the observation)
        '''
        a = np.zeros(self.O)
        a[dPosition[y]] = 1
        return a
    
    def softmax(self, Z):
        '''
        returns an array of floats between 0 and 1 representing the softmax 
        weight of each element in the array
        '''
        A = np.exp(Z)
        return A / A.sum(axis=1, keepdims=True)

    def forward(self, X):
        # TODO: add a boolean parameter to indicate training v. prediction, cache
        # input data + activations (or not) based on the parameter
        self.As.clear()
        self.Zs.clear()
        self.I = X
        Z = X
        for i in range(len(self.Ws) - 1):
            A, Z = self.activation.activate(Z, self.Ws[i], self.Bs[i])
            self.As.append(A)
            self.Zs.append(Z)
        # output layer
        lastHidden = A
        return self.softmax(A.dot(self.Ws[i+1] + self.Bs[i+1])), lastHidden        
    
    def backprop(self, Ygt, Yhat, H, epoch):
        '''
        Ygt - output ground truth
        Yhat - forward prop output
        H - output of the last hidden layer
        epoch - int representing which training loop 
        '''
        numLayers = len(self.Ws)
        lr = learningRate(epoch)
        
        # CALCULATE ERRORS
        deltas = []
        errors = []
        # last hidden -> output layer
        ds, E = self.activation.dO(Yhat, Ygt, H)
        deltas.append(ds)
        errors.append(np.sum(E, axis = 0))
        # hidden layers
        for i in range(numLayers - 2, 0, -1):
            A_in = self.As[i-1]
            A_out = self.As[i]
            ds, E = self.activation.dAHidden(A_in, A_out, E, self.Ws[i+1])
            deltas.insert(0, ds)
            errors.insert(0, np.sum(E, axis = 0))
        # input -> 1st hidden layer
        ds, E = self.activation.dAHidden(self.I, self.As[0], E, self.Ws[1])
        deltas.insert(0, ds)
        errors.insert(0, np.sum(E, axis = 0))

        ## ADJUST WEIGHTS + BIAS
        for i in range(len(self.Ws)):
            self.Ws[i] -= lr * deltas[i]
            self.Bs[i] -= self.activation.biasFactor() * lr * errors[i]
    
    def loss(self, Ygt, Yhat):
        ''' 
        Inputs:
            Ygt - ground truth
            Yhat - predicted
        '''
        return -np.sum(Ygt * np.log(Yhat))
    
    def accuracy(self, Ygt, Yhat):
        ''' 
        Inputs:
            Ygt - ground truth
            Yhat - predicted
        '''
        Yp = np.zeros((len(Yhat), self.O), dtype = np.int8)
        maxes = np.argmax(Yhat, axis = 1)
        for i in range(len(Yhat)):
            Yp[i,maxes[i]] = 1
        return np.sum(np.all(np.equal(Ygt, Yp), axis = 1)) / float(len(Ygt))
        
    
    def printLoss(self, epoch, loss, accuracy):
        print(','.join([str(epoch),str(loss), str(accuracy)]))
        
        