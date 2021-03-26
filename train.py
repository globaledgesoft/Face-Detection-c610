import cv2
import os 
from PIL import Image
import numpy as np



recognizer = cv2.face.LBPHFaceRecognizer_create()
path="images/sahil"                 

def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        print(imagePath)
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        print(os.path.split(imagePath)[-1])
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(1)
    return np.array(IDs), faces


Ids, faces = getImagesWithID(path)
recognizer.train(faces, Ids)

recognizer.save('recognizer/trainningData.yml')
