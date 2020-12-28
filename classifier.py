import numpy as np
import os
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Flatten,Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import detector

DATA_DIR="./train_full"
def load_dataset():
    X=[]
    y=[]
    for dirpath, dirnames, files in os.walk(DATA_DIR):
        for file_name in files:
            img = cv2.imread(dirpath + "/" + file_name)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 17, 9)
            X.append(thresh)
            label=dirpath.split("\\")[-1]
            if(label=="+"): label="10"
            if (label == "-"): label = "11"
            if (label == "mul"): label = "12"
            if (label == "div"): label = "13"
            if (label == "("): label = "14"
            if (label == ")"): label = "15"
            label=int(label)
            y.append(label)

    X=np.array(X)
    X = X.reshape((X.shape[0], 45, 45, 1))
    y=to_categorical(y)
    return X,y


def define_model():
    model = Sequential()
    model.add(Conv2D(30, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(45, 45, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(16, activation='softmax'))
    # compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model,X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model.fit(X_train, y_train, epochs=10,shuffle = True)
    _,acc_train = model.evaluate(X_train, y_train)
    _,acc_test = model.evaluate(X_test, y_test)
    print(acc_train)
    print(acc_test)
    model.save_weights("./model_weights/model_final_full.tf",save_format='tf')

if __name__ == '__main__':

    #X,y=load_dataset()
    #np.save("./train_data/train_x_f", np.array(X))
    #np.save("./train_data/train_y_f", np.array(y))

    X = np.load("./train_data/train_x_f.npy")
    y = np.load("./train_data/train_y_f.npy")
    model=define_model()
    train_model(model,X,y)

    img_path = "./test2.jpg"

    img = cv2.imread(img_path)
    chars = detector.detect(img)

    # predict
    s = ""
    for c in chars:
        c = c.reshape(1, 45, 45, 1)
        c = c.astype('float32')
        pred = np.argmax(model.predict(c))
        print(pred)
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