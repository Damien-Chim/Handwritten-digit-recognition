from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import cv2
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

dic = {
    0 : np.array([1.,0.,0.,0.,0.,0.,0.,0.,0.,0.]),
    1 : np.array([0.,1.,0.,0.,0.,0.,0.,0.,0.,0.]),
    2 : np.array([0.,0.,1.,0.,0.,0.,0.,0.,0.,0.]),
    3 : np.array([0.,0.,0.,1.,0.,0.,0.,0.,0.,0.]),
    4 : np.array([0.,0.,0.,0.,1.,0.,0.,0.,0.,0.]),
    5 : np.array([0.,0.,0.,0.,0.,1.,0.,0.,0.,0.]),
    6 : np.array([0.,0.,0.,0.,0.,0.,1.,0.,0.,0.]),
    7 : np.array([0.,0.,0.,0.,0.,0.,0.,1.,0.,0.]),
    8 : np.array([0.,0.,0.,0.,0.,0.,0.,0.,1.,0.]),
    9 : np.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,1.])
}

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    js_variable = data.get('pix')


    # *$*$*$*$*$*$* ENABLE FOR TESTING *$*$*$*$*$*$*
    label = int(data.get('lab'))
    


    pixels = np.array(js_variable)
    
    pixels = pixels.reshape(150, 150)
    pixels = cv2.resize(pixels, (28, 28))

    
    # OBTAIN TRAINING DATA
    weightsInputToHiddenLayer = np.load('weights_I_H2.npy')
    weightsHiddenToOutputLayer = np.load('weights_H_O2.npy')
    biasesInputToHiddenLayer = np.load('biases_I_H2.npy')
    biasesHiddenToOutputLayer = np.load('biases_H_O2.npy')

    imageSelected = pixels
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
    # print(outputLayerOutputAfterActivation * 100)
    print("You wrote:", outputLayerOutputAfterActivation.argmax())
    
    

    
    # *$*$*$*$*$*$* ENABLE FOR TESTING *$*$*$*$*$*$*
    imagesArray = np.load('imagesArray.npy')
    labelsArray = np.load('labelsArray.npy')

    flat = pixels.flatten()

    imagesArray = np.append(imagesArray, np.array([flat]), axis=0)
    labelsArray = np.append(labelsArray, np.array([dic[label]]), axis = 0)

    np.save('imagesArray', imagesArray)
    np.save('labelsArray', labelsArray)
    print("saved")
    


    pred = int(outputLayerOutputAfterActivation.argmax())
    response_data = {'prediction': pred}
    return jsonify(response_data)
    


    




    # imagesArray = np.load('imagesArray.npy')
    # labelsArray = np.load('labelsArray.npy')
    # print(labelsArray[-1])
    # ran = imagesArray[-1]
    
    # plt.imshow(ran.reshape(28, 28), cmap="Greys")
    # plt.show()



    # imagesArray = np.load('imagesArray.npy')
    # labelsArray = np.load('labelsArray.npy')
    # print(imagesArray.shape)
    # print(labelsArray.shape)

    
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)


