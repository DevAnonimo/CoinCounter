import numpy as np
from cv2 import cv2
 
stream = cv2.VideoCapture("Video/moedas.mp4")
 
if(stream.isOpened() == False):
    print("Erro ao carregar o arquivo")

while(stream.isOpened()):
    ret, frame = stream.read()

    if ret == True:
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) == ord('q'):
            break

        else:
            break

cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
all_circs = cv2.HoughCircles(cinza, cv2.HOUGH_GRADIENT, 0.5, 150, param1=20, param2=30, minRadius=60, maxRadius=90)
all_circs_rounded = np.uint16(np.around(all_circs))
 
print(all_circs_rounded)
print(all_circs_rounded.shape)
print('No vídeo contém ' + str(all_circs_rounded.shape[1]) + ' moedas.')

stream.release()
cv2.destroyAllWindows()
