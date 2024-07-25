import numpy as np
import matplotlib.pyplot as plt
import cv2 
from PIL import Image
import streamlit as st

# Initialisation

# Images and respective labels
images = np.load('imagesArray.npy')
labels = np.load('labelsArray.npy')
# imagesTest, labelsTest = get_mnist2()

# Weights
weightsInputToHiddenLayer = np.random.uniform(-0.5, 0.5, (20, 784))
weightsHiddenToOutputLayer = np.random.uniform(-0.5, 0.5, (10, 20))

# Biases
biasesInputToHiddenLayer = np.zeros((20, 1))
biasesHiddenToOutputLayer = np.zeros((10, 1))

# learning rate
learningRate = 0.01

# Epoch - number of time to pass through all the samples
epochs = 175

# number of correct guesses
numberOfCorrectGuesses = 0


# Forward pass
for i in range(epochs):
    for image, label in zip(images, labels):
        # coverting the vector to a 784 by 1 matrix in order for matrix multiplication
        image.shape += (1,)
        label.shape += (1,)
        
        # passing through from input to hidden layer
        # do the matrix multiplication
        hiddenLayerOutputBeforeActivation = weightsInputToHiddenLayer @ image + biasesInputToHiddenLayer
        # apply sigmoid activation function before passing it to the next layer
        hiddenLayerOutputAfterActivation = 1 / (1 + np.exp(-hiddenLayerOutputBeforeActivation))

        # passing through from hidden to output layer
        # do the matrix multiplication
        outputLayerOutputBeforeActivation = weightsHiddenToOutputLayer @ hiddenLayerOutputAfterActivation + biasesHiddenToOutputLayer
        # apply sigmoid actiavtion function
        outputLayerOutputAfterActivation = 1 / (1 + np.exp(-outputLayerOutputBeforeActivation))

        # calculating loss
        averageLoss = np.sum((outputLayerOutputAfterActivation - label) ** 2, axis=0)
        numberOfCorrectGuesses += int(np.argmax(label) == np.argmax(outputLayerOutputAfterActivation))

        # performing backpropagation
        delta_o = outputLayerOutputAfterActivation - label
        weightsHiddenToOutputLayer += -learningRate * delta_o @ np.transpose(hiddenLayerOutputAfterActivation)
        biasesHiddenToOutputLayer += - learningRate * delta_o

        delta_h = np.transpose(weightsHiddenToOutputLayer) @ delta_o * (hiddenLayerOutputAfterActivation * (1 - hiddenLayerOutputAfterActivation))
        weightsInputToHiddenLayer += - learningRate * delta_h @ np.transpose(image)
        biasesInputToHiddenLayer += - learningRate * delta_h

    # Show accuracy for this epoch
    print("Epoch number", i)
    print(f"Acc: {round((numberOfCorrectGuesses / images.shape[0]) * 100, 2)}%")
    numberOfCorrectGuesses = 0

np.save('weights_I_H2', weightsInputToHiddenLayer)
np.save('weights_H_O2', weightsHiddenToOutputLayer)
np.save('biases_I_H2', biasesInputToHiddenLayer)
np.save('biases_H_O2', biasesHiddenToOutputLayer)