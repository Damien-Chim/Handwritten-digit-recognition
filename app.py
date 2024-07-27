from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import cv2
import json
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    pixels = data.get('pixels')
    
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

    pred = int(outputLayerOutputAfterActivation.argmax())
    response_data = {'prediction': pred}
    return jsonify(response_data)

@app.route('/user_reports', methods=['POST'])
def user_reports():
    data = request.get_json()
    actualNumber = data.get('actualNumber')
    pixels = data.get('pixels')
    toSave = {actualNumber: pixels}
    saveDataToJson(toSave)
    
    return jsonify({"Reponse from python": "Successfully wrote user report to file"})

def saveDataToJson(toSave):
    with open("userReports.json", "r") as fp:
        currentJson = json.load(fp)

    currentJson.append(toSave)

    with open("userReports.json", "w") as fp:
        json.dump(currentJson, fp)

    return

if __name__ == '__main__':
    app.run(debug=True)


