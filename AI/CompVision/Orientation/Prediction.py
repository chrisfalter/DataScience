from enum import Enum

class Orientation(Enum):
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    
    def __lt__(A, B):
        return A.value < B.value

class Prediction():    
    def __init__(self, photoId, orientation, weights):
        self.photoId = photoId
        self.orientation = orientation
        self.weights = weights

def checkAccuracy(testData, predictions):
    total = 0
    right = 0
    
    for test, predict in zip(testData, predictions):
        if test.orientation == predict.orientation:
            right += 1        
        total += 1
        
    print("Accuracy: ", right / total)
