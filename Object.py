import cv2
import numpy as np
  

vid = cv2.VideoCapture(0)

def on_trackbar(val):#function for trackbar
    pass

cv2.namedWindow("Trackbars")#create window for trackbar

cv2.createTrackbar("LowH", "Trackbars", 0, 180, on_trackbar)
cv2.createTrackbar("HighH", "Trackbars", 180, 180, on_trackbar)

cv2.createTrackbar("LowS", "Trackbars", 0, 255, on_trackbar)
cv2.createTrackbar("HighS", "Trackbars", 255, 255, on_trackbar)

cv2.createTrackbar("LowV", "Trackbars", 0, 255, on_trackbar)
cv2.createTrackbar("HighV", "Trackbars", 255, 255, on_trackbar)
#trackbar parameters


while True:

    #
    ret, frame = vid.read()#capturing frames in while loop
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#conversion of frame to hsv
    # Display the resulting frame
  
    l_h = cv2.getTrackbarPos("LowH", "Trackbars")
    l_s = cv2.getTrackbarPos("LowS", "Trackbars")
    l_v = cv2.getTrackbarPos("LowV", "Trackbars")
    u_h = cv2.getTrackbarPos("HighH", "Trackbars")
    u_s = cv2.getTrackbarPos("HighS", "Trackbars")
    u_v = cv2.getTrackbarPos("HighV", "Trackbars")
    #getting values from trackbar slider

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])#lower and upper values for hsv image

    mask = cv2.inRange(hsv, lower, upper)#creating hsv mask
    result = cv2.bitwise_and(frame, frame, mask=mask)#anding the mask with image
    
    #draw bounding box

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#finding contours
    for cnt in contours:#loop for contours
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(result, cnt, -1, (255, 0, 0), 3)#drawing contours
            peri = cv2.arcLength(cnt, True)#finding perimeter
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)#drawing rectangle
            cv2.putText(frame, "Object", (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    
    cv2.imshow("Result", result)#showing result
    cv2.imshow("Original Feed", frame)#showing live feed on box

    key = cv2.waitKey(1)#press esc to exit
    if key == 27:#27 is the ascii value of esc
        break
