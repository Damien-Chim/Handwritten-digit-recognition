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

with open("userReports.json", "r") as fp:
    userReports = json.load(fp)

for i in range(len(userReports)):
    for claimedLabel, pixelArray in userReports[i].items():
        pixels = np.array(pixelArray)
        pixels = pixels.reshape(175, 175)
        pixels = cv2.resize(pixels, (28, 28))
        
        plt.imshow(pixels.reshape(28, 28), cmap="Greys")
        plt.title("Sample number " + str(i) + " User claim: " + str(claimedLabel))
        plt.show()

        y_or_n = str(input("save?"))

        if y_or_n == "y":
            imagesArray_175by175 = np.load('imagesArray_175by175.npy')
            labelsArray_175by175 = np.load('labelsArray_175by175.npy')

            flat = pixels.flatten()

            imagesArray_175by175 = np.append(imagesArray_175by175, np.array([flat]), axis=0)
            labelsArray_175by175 = np.append(labelsArray_175by175, np.array([dic[int(claimedLabel)]]), axis = 0)

            np.save('imagesArray_175by175', imagesArray_175by175)
            np.save('labelsArray_175by175', labelsArray_175by175)
            print("saved as", claimedLabel)

            imagesArray = np.load('imagesArray_175by175.npy')
            labelsArray = np.load('labelsArray_175by175.npy')
            print(imagesArray.shape)
            print(labelsArray.shape)

            imagesArray = np.load('imagesArray_175by175.npy')
            labelsArray = np.load('labelsArray_175by175.npy')
            print(labelsArray[-1])
            ran = imagesArray[-1]
            plt.imshow(ran.reshape(28, 28), cmap="Greys")
            plt.show()

        else:
            print("did not save")