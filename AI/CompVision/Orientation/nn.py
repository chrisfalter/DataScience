from Prediction import Prediction, Orientation
from DataFormats import Thumbnail
import numpy as np
from sklearn.utils import shuffle
from activations import Activation

dPosition = {Orientation.UP.value: 0, Orientation.RIGHT.value: 1, \
             Orientation.DOWN.value: 2, Orientation.LEFT.value: 3}
dPrediction = {0:Orientation.UP, 1:Orientation.RIGHT, 2:Orientation.DOWN, 3:Orientation.LEFT}

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
    
    def train(self, trainData, validationData, paramsFile):
        '''
        optimizes a model to prediction orientation of images
        
        Input:
            trainData - list of Thumbnail
            paramsFile - file to which this function writes optimized hyperparameters/weights
        
        Output:
            Method does not return a value; instead, it writes to paramsFile
        '''
        self.initTrainParams(trainData, validationData)
        # find loss of randomized NN so we can verify that training works
        Y_pred, _ = self.forward(self.Xvalidate)
        bestLoss = self.loss(self.Yvalidate, Y_pred)
        bestWs = None
        bestBs = None
        accuracy = self.accuracy(self.Yvalidate, Y_pred)
        self.printLoss("pre", bestLoss, accuracy)

        epochs = 1500
        batchSize = 10 # use mini-batch gradient descent
        tolerance = 0.06 # amount val-loss must be better than bestLoss to become bestLoss
        maxUnimprovedEpochs = 100
        unimprovedEpochs = 0
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
            if validationLoss + tolerance < bestLoss:
                bestWs = self.Ws
                bestBs = self.Bs
                bestLoss = validationLoss
                unimprovedEpochs = 0
            else:
                unimprovedEpochs += 1
                if unimprovedEpochs >= maxUnimprovedEpochs:
                    break
        # save params to file
        np.save(paramsFile, [bestWs, bestBs])
        
    def initTrainParams(self, trainData, validationData):
        # architecture
        numFeatures = len(trainData[0].pixelArray)
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
        self.X = np.array([trainData[i].normalize() for i in range(len(trainData))])
        self.Y = np.array([self.indicatorArray(trainData[i].orientation.value) for i in range(len(trainData))])
        self.Xvalidate = np.array([validationData[i].normalize() for i in range(len(validationData))])
        self.Yvalidate = np.array([self.indicatorArray(validationData[i].orientation.value) for i in range(len(validationData))])
        
    def predict(self, testData, paramsFile):
        '''
        returns predictions of orientation for each test image
        
        Input:
            testData - list of Thumbnail
            paramsFile - file with hyperparameters/weights
            
        Output:
            list of Prediction
        '''
        self.initTestParams()
        X = np.array([testData[i].normalize() for i in range(len(testData))])
        Ygt = np.array([self.indicatorArray(testData[i].orientation.value) \
                        for i in range(len(testData))])
        Yhat, _ = self.forward(X)
        accuracy = self.accuracy(Ygt, Yhat)
        predictions = [Prediction(testData[i].photoId, dPrediction[np.argmax(Yhat[i])], Yhat[i]) \
                       for i in range(len(Yhat))]
        return predictions        

    def initTestParams(self):
        params = np.load("relu.npy")
        self.Ws = params[0]
        self.Bs = params[1]
        self.I =  None 
        self.As = [] 
        self.Zs = []
        self.O = 4
       
    
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
        lr = self.activation.learningRate(epoch)
        
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
        
        