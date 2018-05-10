import numpy as np
from matplotlib import pyplot as plt
from Prediction import Orientation
from sklearn import preprocessing

class Thumbnail():
    def __init__(self, photoId, orientation, pixelArray):
        self.photoId = photoId          # string
        self.orientation = orientation  # instance of Orientation enum
        self.pixelArray = pixelArray    # numpy array of pixels
    
    def showImage(self):
        image = np.zeros((8, 8, 3))
        
        for i in range(64):
            image[i // 8][i % 8][0] = self.pixelArray[i*3]
            image[i // 8][i % 8][1] = self.pixelArray[i*3+1]
            image[i // 8][i % 8][2] = self.pixelArray[i*3+2]
        
        plt.imshow(image)
        plt.show()
        
    def normalize(self):
        self.pixelArray = self.pixelArray / np.linalg.norm(self.pixelArray)
        return self.pixelArray
        
    def grayscale(self):
        pixels = np.zeros(64)
        for i in range(0, 192, 3):
            new = int(i/3)
            pixels[new] = np.sum(self.pixelArray[i:i+3])/3
        self.pixelArray = pixels
    
            
