
import numpy as np
import matplotlib.pyplot as plt
import cv2 
import os 

# IMAGE PROCESSING
imagecv = cv2.imread('stillAnotherNum.png', cv2.IMREAD_GRAYSCALE)
print(imagecv)
# Resize the image to 28x28
imagecv = cv2.resize(imagecv, (28, 28))

# Invert the colors
imagecv = cv2.bitwise_not(imagecv)

# Normalize the image
imagecv = imagecv.astype('float32') / 255


# OBTAIN TRAINING DATA
weightsInputToHiddenLayer = np.load('weights_I_H2.npy')
weightsHiddenToOutputLayer = np.load('weights_H_O2.npy')
biasesInputToHiddenLayer = np.load('biases_I_H2.npy')
biasesHiddenToOutputLayer = np.load('biases_H_O2.npy')


imageSelected = imagecv
imageSelected.shape += (1,)

# do the forward pass
# passing through from input to hidden layer
# do the matrix multiplication
hiddenLayerOutputBeforeActivation = weightsInputToHiddenLayer @ imageSelected.reshape(784, 1) + biasesInputToHiddenLayer
# apply sigmoid activation function before passing it to the next layer
hiddenLayerOutputAfterActivation = 1 / (1 + np.exp(-hiddenLayerOutputBeforeActivation))

# passing through from hidden to output layer
# do the matrix multiplication
outputLayerOutputBeforeActivation = weightsHiddenToOutputLayer @ hiddenLayerOutputAfterActivation + biasesHiddenToOutputLayer
# apply sigmoid actiavtion function
outputLayerOutputAfterActivation = 1 / (1 + np.exp(-outputLayerOutputBeforeActivation))
# print(outputLayerOutputAfterActivation * 100)
print(outputLayerOutputAfterActivation * 100)
print("You wrote:", outputLayerOutputAfterActivation.argmax())


import createData
# plt.imshow(imagecv.reshape(28, 28), cmap="Greys")
# plt.show()
# time.sleep(1)
# plt.close()


