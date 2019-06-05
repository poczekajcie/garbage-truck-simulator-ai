from sklearn import datasets
from sklearn.svm import SVC
from scipy import misc
from pathlib import Path
import random
from PIL import Image

def predictDigits():
    path = Path('/home/kuba/Desktop/garbage-truck-simulator-ai/DigitRecognition/House_Digits')

    random_filename = random.choice(list(path.glob('*.png')))

    image = Image.open(random_filename)
    image.show()
 
    digits = datasets.load_digits()

    features = digits.data 
    labels = digits.target

    clf = SVC(gamma = 0.001)
    clf.fit(features, labels)

    img = misc.imread(random_filename)
    img = misc.imresize(img, (8,8))
    img = img.astype(digits.images.dtype)
    img = misc.bytescale(img, high=16, low=0)

    x_test = []

    for eachRow in img:
        for eachPixel in eachRow:
            x_test.append(sum(eachPixel)/3.0)

    print(clf.predict([x_test]))

    input("Press Enter to continue...")

    return True;

predictDigits()

