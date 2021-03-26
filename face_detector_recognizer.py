# develop an Smart Camera use case - face recognition application
import numpy as np
import cv2

label_mapper = ['Unknown', 'sahil']

def draw_named_box(label, img, coords):
    # function is used for to draw bounding box on the image 
    x, y, w, h = coords
    lbl_txt = label_mapper[label]
    if label == 0:
        color = (0, 0, 255)
    else:
        color = (0, 255, 0)
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
    size = cv2.getTextSize(lbl_txt, 1, 1, 1)
    x_e = x+size[0][0]
    y_e = y+size[0][1]
    cv2.rectangle(img, (x-5, y-10), (x_e+5, y_e), color, cv2.FILLED)
    img = cv2.putText(img, lbl_txt, (x, y), 1, 1, (0,0,0), 1, 1)
    return img


def predict(recognizer):
    # perform perdict function 
    face_cascade = cv2.CascadeClassifier('cascade/haarcascade_frontalface_default.xml')
    detected = 0
    i=0

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("appsrc ! videoconvert ! omxh264enc ! h264parse ! mp4mux ! filesink location=video.mp4", fourcc, 30, (1280, 720), True)
    cap = cv2.VideoCapture("qtiqmmfsrc ldc=TRUE !video/x-raw, format=NV12, width=1280, height=720, framerate=30/1 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

    while(cap.isOpened()):
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            label, dist_val = recognizer.predict(roi_gray)
            print(dist_val)
            if(dist_val>70):
                label = 0
            else:
                i += 1
            img = draw_named_box(label, img, (x, y, w, h))
        out.write(img)
    out.release()
    cap.release()


if __name__ == "__main__":
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/trainningData.yml")
    predict(recognizer)
