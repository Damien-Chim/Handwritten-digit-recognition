imagesArray = np.load('imagesArray_175by175.npy')
    labelsArray = np.load('labelsArray_175by175.npy')
    print(labelsArray[-1])
    ran = imagesArray[-1]
    
    plt.imshow(ran.reshape(28, 28), cmap="Greys")
    plt.show()