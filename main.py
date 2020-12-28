import cv2
import numpy as np

import detector
import classifier
import parse

# load model
model = classifier.define_model()
model.load_weights("./model_weights/model_final_full.tf")

def calculate(img_path):
    img = cv2.imread(img_path)
    chars = detector.detect(img)
    # predict
    s = ""
    for c in chars:
        c = c.reshape(1, 45, 45, 1)
        c = c.astype('float32')
        pred = np.argmax(model.predict(c))
        if (pred == 10):
            s += "+"
        elif (pred == 11):
            s += "-"
        elif (pred == 12):
            s += "*"
        elif (pred == 13):
            s += "/"
        elif (pred == 14):
            s += "("
        elif (pred == 15):
            s += ")"
        else:
            s += str(pred)
    v = parse.evaluate(s)
    print("Expression: ",s)
    return v


if __name__ == '__main__':
    # set path for input image
    img_path = "./test2.jpg"
    v=calculate(img_path)
    print("Result:", v)
    img=cv2.imread(img_path)
    img=cv2.resize(img,(680,480))
    cv2.imshow("input",img)
    cv2.waitKey(0)