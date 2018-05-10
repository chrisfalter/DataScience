import numpy as np
from Prediction import Orientation
from DataFormats import Thumbnail

def readImages(imageFile):
    '''
    returns a numpy array of Thumbnail extracted from imageFile
    '''
    #def __init__(self, photoId, orientation, pixelArray):
    
    images = []
    orientations = {0 : Orientation.UP, 90 : Orientation.RIGHT, \
                    180 : Orientation.DOWN, 270 : Orientation.LEFT}
    
    with open(imageFile, 'r') as file:
        for row, data in enumerate(file):
            values = data.split()
            
            photoId = values[0]
            orientation = orientations[int(values[1])]
            pixelArray = np.array([int(x) for x in values[2:]])
            
            images.append(Thumbnail(photoId, orientation, pixelArray))

    return images    

def writePredictions(predictions, outputFile):
    '''
    writes the list of predictions to a file named "output.txt"
    '''
    with open(outputFile, 'w') as file:
        for prediction in predictions:
            file.write(prediction.photoId + " " + str(prediction.orientation.value) + "\n")
    
    return
