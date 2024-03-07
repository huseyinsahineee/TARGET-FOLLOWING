import serial
import time
import cv2
import numpy as np
import datetime

cap1 = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture("http://192.168.1.33:8080/video")
# Set the default camera to cap1
current_cap = cap1
ser = serial.Serial("COM4", '9600', timeout=2)

Xposition = 90
Yposition = 90

while True:
    _, frame = current_cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_lower = np.array([0, 50, 50], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    mask = cv2.inRange(hsv, red_lower, red_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    rows, cols, _ = frame.shape
    center_x = int(rows / 2)
    center_y = int(cols / 2)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "x = "+str(x)+"y = "+str(y)
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255))
        #////////////////////////////////////////////////////////////////////
        medium_x = int((x + x+w)/2)
        medium_y = int((y + y+h)/2)
        #////////////////////////////////////////////////////////////////////
        cv2.line(frame, (medium_x,0),(medium_x,600),(0,255,0),2)
        text2 = "mediumX = " + str(medium_x)
        cv2.putText(frame, text2, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 50))
        #////////////////////////////////////////////////////////////////////
        cv2.line(frame, (0, medium_y), (600, medium_y), (0, 255, 0), 2)
        text3 = "mediumY = " + str(medium_y)
        cv2.putText(frame, text3, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 50))

        # ////////////////////////////////////////////////////////////////////
        if medium_x > center_x +50:
            Xposition += 2
         #   ser.write((str(Xposition) + 'a').encode('utf-8'))
           # time.sleep(0.03)
        if medium_x < center_x -50:
            Xposition -= 2
          #  ser.write((str(Xposition) + 'a').encode('utf-8'))
           # time.sleep(0.03)
        if medium_y > center_y + 50:
            Yposition += 2
           # ser.write((str(Yposition) + 'b').encode('utf-8'))
            # time.sleep(0.03)
        if medium_y < center_y - 50:
            Yposition -= 2
           # ser.write((str(Yposition) + 'b').encode('utf-8'))
        ser.write(('a'+ str(int(Xposition))+'b'+ str(int(Yposition))).encode('utf-8'))

        break
    height, width, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_right_corner = (width - 160, height - 35)
    font_scale = 0.7
    font_thickness = 2
    font_color = (0, 0, 0)
    text1 = "Huseyin SAHIN"
    cv2.putText(frame, text1, bottom_right_corner, font, font_scale, font_color, font_thickness)

    bottom_right_corner = (width - 115, height - 10)
    text2 = "16290762"
    cv2.putText(frame, text2, bottom_right_corner, font, font_scale, font_color, font_thickness)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    time_text = current_time
    top_right_corner = (width - 100, 40)
    cv2.putText(frame, time_text, top_right_corner, font, font_scale, font_color, font_thickness)

    date_text = current_date
    top_right_corner = (width - 146, 20)
    cv2.putText(frame, date_text, top_right_corner, font, font_scale, font_color, font_thickness)

    cv2.imshow("frame",frame)
  # cv2.imshow("mask",mask )
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('1'):
        current_cap = cap1
    #elif key == ord('2'):
    #    current_cap = cap2
ser.close()
cap1.release()
#cap2.release()
cv2.destroyAllWindows()






