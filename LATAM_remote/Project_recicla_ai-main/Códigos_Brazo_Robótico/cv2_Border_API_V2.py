import cv2
import numpy as np
import time
import requests
import serial

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

new_object = True
start_time = 0.0
api_request = False
class_text = ' '
prob_text = ' '
 
def send_api():
    API_ENDPOINT = 'https://nig4obljh6.execute-api.us-east-2.amazonaws.com/beta'
    image = '/home/pi/Desktop/image.jpg'
    data = open(image, 'rb').read()
    headers = {'Content-Type':'image/jpeg'}
    
    response = requests.post(url=API_ENDPOINT, headers=headers, data=data)
    
    return response.json()

def empty(a):
    pass


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(orig, img,imgContour):
    global new_object
    global start_time
    global api_request
    global class_text
    global prob_text
    
    offset = 20
    
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    cnt = max(contours, key=cv2.contourArea)
    areaMin = 4000
    area = cv2.contourArea(cnt)
    
    if  area > areaMin:
        cv2.drawContours(imgContour, [cnt], -1, (255, 0, 255), 7)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        x , y , w, h = cv2.boundingRect(approx)
        
        x = x - offset
        y = y - offset
        w = w + (2*offset)
        h = h + (2*offset)
        
        cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

        cv2.putText(imgContour, "Class: " + class_text, (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                    (0, 255, 0), 2)
        cv2.putText(imgContour, "Prob: " + prob_text, (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (0, 255, 0), 2)
            
        if new_object == True:
            start_time = time.time()
            new_object = False
            print('new object')
        else:
            end_time = time.time()
            
            if (end_time - start_time) > 3 and (api_request == False):
                cropped_image = orig[y:y+h,x:x+w]
                cv2.imwrite('/home/pi/Desktop/image.jpg', cropped_image)
                response = send_api()
                class_text = str(response['class'])
                prob_text = str(response['probability'])+'%'
                txt2send = class_text + '\n'
                ser.write(txt2send.encode('utf-8'))
                api_request = True
                    
    else:
        new_object = True
        api_request = False
        class_text = ' '
        prob_text = ' '
        print('No object')

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
    
    while True:
        success, img = cap.read()
        imgContour = img.copy()
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        threshold1 = 49
        threshold2 = 37
        imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        getContours(img, imgDil,imgContour)
        imgStack = stackImages(1,([imgContour]))
        cv2.imshow("Result", imgStack)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()