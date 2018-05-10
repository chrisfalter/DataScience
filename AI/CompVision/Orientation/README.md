## Detecting Picture Orientation with a Hand-Rolled Feed Forward Neural Network
I had a lot of fun working with my teammates Anthony Duer and Alex DeCourcy on building machine learning algorithms from scratch to predict the orientation of pictures. Anthony implemented K-Nearest Neighbors, Alex implemented AdaBoost, and I implemented a feed-forward neural network. In this post I describe how you can use the code in this directory to train the neural network and predict test observations.
### The Data
Pictures are micro-thumbnails of dimension 8x8x3. Each picture is stored as a single line of 192 space-separated values (ranging from 0 to 255) in a text file. About 40,000 images are in train-data.txt, along with an orientation value of 0, 90, 180, or 270, and a picture ID. The pictures were extracted from a Flickr public dataset released under the Creative Commons license that allows only academic, non-commercial use. Anthony and I wrote the code in fileIO.py that can read the images from the file.
### Neural Network Architecture
This section describes the neural network code that I wrote.
#### Activation Functions
Since the derivatives used in backpropagation depend on the activation function, I wrote an Activation class that accepts an initialization argument that specifies one of the activation functions (ReLu, Tanh, and Sigmoid) which are implemented as classes. Since the different activation functions seemed to work best with different learning rates and bias factors, each activation class was given a `learningRate` and `biasFactor` property function. Also, different weight initializations worked best for different activation functions--at least according to my reading of the literature. See the file activations.py for details.
#### Controlling Hyperparameters
The NeuralNet class in nn.py accepts two initialization arguments:
1. Activation function type, and
2. A list of layer dimensions. Note that the input layer is assumed to have dimension 192 and so is not specified in the argument.

The class implements the train and predict functions, along with several helper functions. The maximum number of training epochs is set via the `epochs` variable, and the `batchSize` variable controls the size of the mini-batch gradient descent. The best-so-far weights were stored in memory, then written to a [activation-function-name].npy file at the end of training.
### Training Script

### Results

### Credit to My Teammates
