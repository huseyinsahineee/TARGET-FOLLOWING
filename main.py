import cv2
import numpy as np
import serial
import pygame
import datetime

ser = serial.Serial('COM5', 9600) # Seri haberleşme bağlantısını açın
cap = cv2.VideoCapture(0)

pygame.mixer.init()
pygame.mixer.music.load('C:\\Users\\husey\\Desktop\\proje\\arama.mp3')
pygame.mixer.music.play(-1)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower boundary RED color range values; Hue (0 - 10)
    #lower1 = np.array([0, 100, 20])
    #upper1 = np.array([10, 255, 255]) 
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255]) 
  
    mask = cv2.inRange(hsv, lower2, upper2)
    ret, thresh = cv2.threshold(mask, 40, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_contour_area = 2000 # Minimum kontur alanı için eşik değeri
    max_contour_area = 50000 # Maksimum kontur alanı için eşik değeri

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area and area < max_contour_area:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Kırmızı nesnenin merkez noktasını (x, y) bulun
            cx = x + w // 2
            cy = y + h // 2

            # Arduino'ya seri haberleşme ile (cx, cy) pozisyonunu gönderin
            ser.write(str(cx).encode() + b',' + str(cy).encode() + b'\n')

    # Görüntünün genişliği ve yüksekliğini kullanarak merkez noktayı bulun
    height, width, _ = frame.shape
    cx = width // 2
    cy = height // 2

    # "Hüseyin ŞAHİN" yazısı
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_right_corner = (width-160, height-35) # sağ alt köşe koordinatları
    font_scale = 0.7
    font_thickness = 2
    font_color = (0, 0, 0) # siyah renk
    text1 = "Huseyin SAHIN"
    cv2.putText(frame, text1, bottom_right_corner, font, font_scale, font_color, font_thickness)

    # "16290762" yazısı
    bottom_right_corner = (width-115, height-10) # "Huseyin ŞAHIN" yazısının altında konumlandırma
    text2 = "16290762"
    cv2.putText(frame, text2, bottom_right_corner, font, font_scale, font_color, font_thickness)

    # Sistem saatini ve tarihini alın
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S") # saat:dakika:saniye
    current_date = now.strftime("%d/%m/%Y") # gün/ay/yıl

    # Saat ve tarih yazısını oluşturun ve görüntü üzerinde gösterin
    time_text = current_time 
    font = cv2.FONT_HERSHEY_SIMPLEX
    top_right_corner = (width-100, 40) # sağ üst köşe koordinatları
    font_scale = 0.7
    font_thickness = 2
    font_color = (0, 0, 0) # siyah renk
    cv2.putText(frame, time_text, top_right_corner, font, font_scale, font_color, font_thickness)
    date_text = current_date
    font = cv2.FONT_HERSHEY_SIMPLEX
    top_right_corner = (width-146, 20) # sağ üst köşe koordinatları
    font_scale = 0.7
    font_thickness = 2
    font_color = (0, 0, 0) # siyah renk
    cv2.putText(frame, date_text, top_right_corner, font, font_scale, font_color, font_thickness)


    # Merkez noktayı görüntü üzerinde çizin
    cv2.line(frame, (cx-10, cy), (cx+10, cy), (0, 0, 0), thickness=3)
    cv2.line(frame, (cx, cy-10), (cx, cy+10), (0, 0, 0), thickness=3)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close() # Seri haberleşme bağlantısını kapatın
cap.release()
cv2.destroyAllWindows()