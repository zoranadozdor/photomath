import cv2
from imutils.contours import sort_contours
import imutils

def detect(img):
    #preprocess
    img = cv2.resize(img, (680, 480),interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #ret, thresh = cv2.threshold(blur, 95, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 17, 9)
    #find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    chars = []

    #save coordinates and bounding boxes
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if (w < 7 or h < 7): continue
        roi = thresh[y:y + h, x:x + w]
        resized = cv2.resize(roi, (45,45),interpolation = cv2.INTER_AREA)
        chars.append(resized)
    return chars


if __name__ == '__main__':
    img_path = "./test5.jpg"
    img = cv2.imread(img_path)
    img=cv2.resize(img,(680,480))
    chars=detect(img)