import numpy as np
import cv2

imagecv = cv2.imread('stillAnotherNum.png', cv2.IMREAD_GRAYSCALE)

# imagecv = cv2.resize(imagecv, (28, 28))
imagecv = cv2.bitwise_not(imagecv)
imagecv = imagecv.astype('float32') / 255

# label = int(input("What is the number"))
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
# imagesArray = np.empty((0, 784))
# labelsArray = np.empty((0, 10))
# np.save('imagesArray', imagesArray)
# np.save('labelsArray', labelsArray)



label = int(input("Enter number: "))

imagesArray = np.load('imagesArray.npy')
labelsArray = np.load('labelsArray.npy')

flat = imagecv.flatten()

imagesArray = np.append(imagesArray, np.array([flat]), axis=0)
labelsArray = np.append(labelsArray, np.array([dic[label]]), axis = 0)

np.save('imagesArray', imagesArray)
np.save('labelsArray', labelsArray)



# imagesArray = np.load('imagesArray.npy')
# labelsArray = np.load('labelsArray.npy')
# print(imagesArray.shape)
# print(labelsArray.shape)
# print(imagesArray)
# print(labelsArray)


