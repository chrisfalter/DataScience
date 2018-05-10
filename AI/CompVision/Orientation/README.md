## Detecting Picture Orientation with a Hand-Crafted Feed Forward Neural Network
I had a lot of fun working with my teammates Anthony Duer and Alex DeCourcy on building machine learning algorithms from scratch to predict the orientation of pictures. Anthony implemented K-Nearest Neighbors, Alex implemented AdaBoost, and I implemented a feed-forward neural network. In this post I describe how you can use the code in this directory to train the neural network and predict test observations. 

This post assumes that you already understand the basics of neural networks. If you need a primer, I highly recommend [Conde Nast's introduction to the topic](https://technology.condenast.com/story/a-neural-network-primer).
### The Data
The pictures we worked with are micro-thumbnails of dimension 8x8x3. Each picture is stored as a single line of 192 space-separated values (ranging from 0 to 255) in a text file. About 40,000 images are in `train-data.txt`, along with an orientation value of 0, 90, 180, or 270 and a picture ID. The pictures were extracted from a Flickr public dataset released under the Creative Commons license that allows only academic, non-commercial use. Anthony and I wrote the code in fileIO.py that can read the images from the file.
### Neural Network Architecture
This section describes the neural network code that I wrote.
#### Activation Functions
Since the derivatives used in backpropagation vary depending on the activation function, I wrote an Activation class that accepts an initialization argument specifying which activation functions (ReLu, Tanh, or Sigmoid) to use. Since the different activation functions seemed to work best with different learning rates and bias factors, each activation class was given a `learningRate` and `biasFactor` property function. Also, different weight initializations worked best for different activation functions--at least according to my reading of the literature--so each function-associated class had a weight initialization property. See the file `activations.py` for details.
#### Hyperparameters
The `NeuralNet` class in `nn.py` accepts two initialization arguments:
1. Activation function type, and
2. A list of hidden layer dimensions. The input layer has fixed dimensions of 1 x 192 and the output layer 1 x 4 (one neuron for each predicted orientation), so they are not specified in the argument.

The `NeuralNet` class implements the `train()` and `predict()` functions along with several helper functions. The maximum number of training epochs is set via the `epochs` variable, and the `batchSize` variable controls the size of the mini-batch gradient descent. Given more time I would have added class initialization arguments for epochs, batch size, and learning rate. I will be using extremely capable open-source frameworks like Tensorflow, PyTorch, and Keras on future efforts, so I do not intend to make any further investments in this code. 

The best-so-far weights are stored in memory, then written to an `activation-function-name.npy` file at the end of training. Tracking these weights in memory, rather than writing to disc, might not support very large networks on memory-constrained machines. Given the tiny size of the training images and the capabilities of my laptop, however, the design choice was justifiable for this learning project.
### Training the Neural Network
The training process uses the 40,000 images in `train-data.txt` as a training set and the 1,000 images in `test-data.txt` as a validation set.

The `nnTrain.py` script follows these steps:
+ accepts command-line parameters for activation function type and hidden layer architecture
+ constructs a neural network of the requested type
+ loads the training and validation sets
+ trains the network until the validation accuracy converges for a sufficiently long period, or until the maximum training epochs is reach
+ prints epoch number, validation loss and accuracy to stdout in comma-delimited format after each epoch
+ saves the best-so-far weights to a `.npy` file at the end of training

The `nnExperiments.cmd` file drives the training process over a variety of architectures, saving the output of each training session into a CSV file. The file could easily be converted for use in a Bash environment by changing the file extension and the names of the output files.
### Results
A hidden layer architecture of 192 x 192 had the best generalization and accuracy over the validation data. This was somewhat surprising, as deep architectures with up to dozens of layers have prevailed in computer vision competitions. Architectures deeper or wider than 192 x 192 seemed to overfit the model for this problem, however. Larger architectures had lower training loss than the 192 x 192 network, but accomplished that lower loss by essentially memorizing the inputs. This left them less capable of generalizing to previously unseen images.

The ReLu activation function proved superior to the hyperbolic tangent and logistic (sigmoid) functions. This is not surprising; ReLu activation is generally used in competition-winning computer vision architectures. 

The validation accuracy of the best architecture was greater than 71%--not bad, given the tiny size of the images!
### Credit Where Credit Is Due
I modularized the team solution and wrote the start-up code for all of the files in this repository. I would be remiss, however, not to acknowledge the excellent work my teammates Anthony and Alex did on shared code in the following files:

DataFormats.py
FileIO.py
Orient.py
Prediction.py

I take credit or blame, as appropriate, for the remainder of the source files.
