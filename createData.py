from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import cv2
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# imagesArray = np.empty((0, 784))
# labelsArray = np.empty((0, 10))
# np.save('imagesArray_175by175', imagesArray)
# np.save('labelsArray_175by175', labelsArray)
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
    pixels = data.get('pixels')
    label = int(data.get('label'))
    
    pixels = np.array(pixels)
    pixels = pixels.reshape(175, 175)
    pixels = cv2.resize(pixels, (28, 28))



    
    # OBTAIN TRAINING DATA
    weightsInputToHiddenLayer = np.load('weights_I_H_175by175.npy')
    weightsHiddenToOutputLayer = np.load('weights_H_O_175by175.npy')
    biasesInputToHiddenLayer = np.load('biases_I_H_175by175.npy')
    biasesHiddenToOutputLayer = np.load('biases_H_O_175by175.npy')

    imageSelected = pixels
    imageSelected.shape += (1,)

    hiddenLayerOutputBeforeActivation = weightsInputToHiddenLayer @ imageSelected.reshape(784, 1) + biasesInputToHiddenLayer
    hiddenLayerOutputAfterActivation = 1 / (1 + np.exp(-hiddenLayerOutputBeforeActivation))
    outputLayerOutputBeforeActivation = weightsHiddenToOutputLayer @ hiddenLayerOutputAfterActivation + biasesHiddenToOutputLayer
    outputLayerOutputAfterActivation = 1 / (1 + np.exp(-outputLayerOutputBeforeActivation))
    

    # *$*$*$*$*$*$* ENABLE FOR TESTING *$*$*$*$*$*$*
    imagesArray_175by175 = np.load('imagesArray_175by175.npy')
    labelsArray_175by175 = np.load('labelsArray_175by175.npy')

    flat = pixels.flatten()

    imagesArray_175by175 = np.append(imagesArray_175by175, np.array([flat]), axis=0)
    labelsArray_175by175 = np.append(labelsArray_175by175, np.array([dic[label]]), axis = 0)

    np.save('imagesArray_175by175', imagesArray_175by175)
    np.save('labelsArray_175by175', labelsArray_175by175)
    print("saved as", label)
    
    prediction = int(outputLayerOutputAfterActivation.argmax())
    response_data = {'prediction': prediction}
    


    


    # imagesArray = np.load('imagesArray_175by175.npy')
    # labelsArray = np.load('labelsArray_175by175.npy')
    # print(labelsArray[-3])
    # ran = imagesArray[-3]
    
    # plt.imshow(ran.reshape(28, 28), cmap="Greys")
    # plt.show()



    imagesArray = np.load('imagesArray_175by175.npy')
    labelsArray = np.load('labelsArray_175by175.npy')
    print(imagesArray.shape)
    print(labelsArray.shape)
    # return jsonify({'prediction':'test'})

    return jsonify(response_data)
    

if __name__ == '__main__':
    app.run(debug=True)