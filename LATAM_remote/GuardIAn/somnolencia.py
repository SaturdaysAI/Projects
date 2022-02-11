from scipy.spatial import distance
from imutils import face_utils
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import _thread
import imutils
import time
import dlib
import cv2


def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = distance.euclidean(eye[0], eye[3])
	
    # compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	
    # return the eye aspect ratio
	return ear

hilo_flag= True #Solo para desarrollo, version final solo True
l_alarma = _thread.allocate_lock() # Puede ser N Locks, pero solo puede ser adquirido uno a la vez
def sound_alarm():
    global ejecucion
    while hilo_flag:
        l_alarma.acquire()
        ALARM = AudioSegment.from_mp3("sound/alarm3.mp3")
        for i in np.arange(3):
            play(ALARM)


# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.22
EYE_AR_CONSEC_FRAMES = 10
EYE_AR_NOT_DETECTED_FRAMES = 20

# initialize the frame counters for drowsiness and eyes distraction
# as well as a boolean used to indicate if the alarm is going off
COUNTER_DROWSINESS = 0
COUNTER_EYES_NOT_DETECTED = 0
ALARM_ON = False
ENVIO_ALERTA = False
MENSAJE_ALERTA = ""

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


l_alarma.acquire() # Obtengo el candado previo a crear hilo
_thread.start_new_thread(sound_alarm,()) #Crea un único hilo para las alarmas 

def deteccionSomnolencia(frame):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    global COUNTER_DROWSINESS 
    global COUNTER_EYES_NOT_DETECTED
    
    frame = imutils.resize(frame, width=450)
	
	# detect faces in the grayscale frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
	
	#Si subjects se encuentra vacio no se detectaron ojos en el cuadro 
    if not subjects:
        COUNTER_EYES_NOT_DETECTED += 1        
        if COUNTER_EYES_NOT_DETECTED >= EYE_AR_NOT_DETECTED_FRAMES:
			#Si esta distraido
            #MENSAJE_ALERTA = "***CONDUCTOR DISTRAIDO!***"
            MENSAJE_ALERTA = "Conductor distraido : " + current_time 
            cv2.putText(frame, MENSAJE_ALERTA, (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #print(f"Desbloqueando lock de distraccion ojos: {COUNTER_EYES_NOT_DETECTED} , {EYE_AR_NOT_DETECTED_FRAMES}")
            if l_alarma.locked():
                l_alarma.release()
    else:
        COUNTER_EYES_NOT_DETECTED = 0
        time.sleep(0.02)
        if not l_alarma.locked():
            l_alarma.acquire()

        
        for subject in subjects:

			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)#converting to NumPy Array

			# extract the left and right eye coordinates, then use the
			# coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]			
            rightEye = shape[rStart:rEnd]

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

			# average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
            

			# compute the convex hull for the left and right eye
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
		
			# visualize each of the eyes
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		
			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:      
                COUNTER_DROWSINESS += 1
                # if the eyes were closed for a sufficient number of then sound the alarm
                if COUNTER_DROWSINESS >= EYE_AR_CONSEC_FRAMES:
						#Si esta somsoliento
                        #MENSAJE_ALERTA = "***ALERTA DE SOMNOLENCIA!***"
                        MENSAJE_ALERTA = "Conductor dormido : " + current_time  
                        cv2.putText(frame, MENSAJE_ALERTA, (10, 30),
							cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        #print(f"Desbloqueando lockde somnolencia: {COUNTER_DROWSINESS} , {EYE_AR_CONSEC_FRAMES}")
                        if l_alarma.locked():
                            l_alarma.release()
			# otherwise, the eye aspect ratio is not below the blink
			# threshold, so reset the counter and alarm
            else:
                COUNTER_DROWSINESS = 0
                time.sleep(0.02)
                if not l_alarma.locked():
                    l_alarma.acquire()
					
    return frame