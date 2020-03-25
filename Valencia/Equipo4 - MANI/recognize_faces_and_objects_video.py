# USAGE
# python recognize_faces_and_objects_video.py --encodings encodings.pickle --input videos/<video_file_name>.mp4 --output output/<output_vide>.avi --display 1

# In order for this code to work, you need as well:
# - video folder
# - output folder
# - Trained Weights for the object detection
# - pickle object of encoded face embeddings for the face recognition

##################################################################################################################################
# IMPORTANT INFO                                                                                                                 #
# This code has been developed by Group 4 of the first Saturdays AI edition in Valencia. Please make sure to mention it,         #
# in case you use it in your projects. Also note that part of this code (face detection algorithm) was based on code downloaded  #
# from pyimagesearch.com . You may want to mention that as well. Also note that this code has been writtenin order to process a  #
# video file. If you want to read from a camera in real time, you will have to substitute the corresponding parts of the code.   # 
##################################################################################################################################

# Import the necessary packages for face recognition
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# Import the necessary packages for object detection
from gtts import gTTS # Google Text to Speech
import numpy as np
from IPython.display import Audio # Audio method from IPython's Display Class
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose, Add, Input, Activation
from tensorflow.keras.models import Model
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
ap.add_argument("-i", "--input", required=True,
    help="path to input video")
ap.add_argument("-o", "--output", type=str,
    help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
    help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
    help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# Define the Neural Network for object detection
def FCN8( nClases ,  input_height=224, input_width=224):

    assert input_height%32 == 0
    assert input_width%32 == 0
    IMAGE_ORDERING =  "channels_last" 

    img_input = Input(shape=(input_height,input_width, 3))
    
    ## Block 1
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1', data_format=IMAGE_ORDERING )(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2', data_format=IMAGE_ORDERING )(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool', data_format=IMAGE_ORDERING )(x)
    f1 = x
    
    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2', data_format=IMAGE_ORDERING )(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool', data_format=IMAGE_ORDERING )(x)
    f2 = x

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3', data_format=IMAGE_ORDERING )(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool', data_format=IMAGE_ORDERING )(x)
    pool3 = x

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3', data_format=IMAGE_ORDERING )(x)
    pool4 = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool', data_format=IMAGE_ORDERING )(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1', data_format=IMAGE_ORDERING )(pool4)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2', data_format=IMAGE_ORDERING )(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3', data_format=IMAGE_ORDERING )(x)
    pool5 = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool', data_format=IMAGE_ORDERING )(x)
    
    n = 4096
    o = ( Conv2D( n , ( 7 , 7 ) , activation='relu' , padding='same', name="conv6", data_format=IMAGE_ORDERING))(pool5)
    conv7 = ( Conv2D( n , ( 1 , 1 ) , activation='relu' , padding='same', name="conv7", data_format=IMAGE_ORDERING))(o)
    conv7_4 = Conv2DTranspose( nClases , kernel_size=(4,4) ,  strides=(4,4) , use_bias=False, data_format=IMAGE_ORDERING )(conv7)
    pool411 = ( Conv2D( nClases , ( 1 , 1 ) , activation='relu' , padding='same', name="pool4_11", data_format=IMAGE_ORDERING))(pool4)
    pool411_2 = (Conv2DTranspose( nClases , kernel_size=(2,2) ,  strides=(2,2) , use_bias=False, data_format=IMAGE_ORDERING ))(pool411)
    pool311 = ( Conv2D( nClases , ( 1 , 1 ) , activation='relu' , padding='same', name="pool3_11", data_format=IMAGE_ORDERING))(pool3)
        
    o = Add(name="add")([pool411_2, pool311, conv7_4 ])
    o = Conv2DTranspose( nClases , kernel_size=(8,8) ,  strides=(8,8) , use_bias=False, data_format=IMAGE_ORDERING )(o)
    o = (Activation('softmax'))(o)
    
    model = Model(img_input, o)
    return model


# Create model object out of the neural network previously defined
print("[INFO] Building Neural Network Model...")
n_clases = 3 # Number of classes currently 3: cars, people, background
model = FCN8(nClases     = n_clases,  
             input_height = 224, 
             input_width  = 224)

# Load weights for the object detection 
print("[INFO] loading weights...")
PathPesos="Pesos.h5"
model.load_weights(PathPesos)

def readImage( path , width , height ):
        img = Image.open('foto.jpg')
        img.save('foto.png')
        img = mpimg.imread('foto.png')
        if ((width!=0) & (height != 0)):
            img = cv2.resize(img, ( width , height ))#/ 127.5 - 1
        return img

def reshape_video_frame(frame_object_detection, width , height ):
        if ((width!=0) & (height != 0)):
            frame_object_detection = np.float32(cv2.resize(frame_object_detection, ( width , height ))) #/ 127.5 - 1

        return frame_object_detection

def FindContoursPeople(MP):
    contours, hierarchy  = cv2.findContours(MP,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if c.shape[0]>20:
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            if cY < MP.shape[1]/3:
                strY = " lejos"
            elif cY <MP.shape[1]*2/3:
                strY = " a media distancia"
            else:
                strY = " cerca"
            
            if cX<MP.shape[0]/3:
                strX = " a la Izquierda"
            elif cX < MP.shape[0]*2/3:
                strX = " en el centro"
            else:
                strX = " a la derecha"
            
            strP = " Hay una persona" + strY + strX

            return strP

def FindContoursCars(MC):
    contours, hierarchy  = cv2.findContours(MC,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if c.shape[0]>20:
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            if cY < MC.shape[1]/3:
                strY = " lejos"
            elif cY < MC.shape[1]*2/3:
                strY = " a media distancia"
            else:
                strY = " cerca"
        
        
            if cX<MC.shape[0]/3:
                strX = " a la izquierda"
            elif cX < MC.shape[0]*2/3:
                strX = " en el centro"
            else:
                strX = " a la derecha"
            
            strC = "hay un coche" + strY + strX

            return strC

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# ONLY FOR CAMERA
# Initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
#print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start()
#writer = None
#time.sleep(2.0)

# Capture video
print("[INFO] processing video...")
stream = cv2.VideoCapture(args["input"])
writer = None

# Loop over frames from the video file stream, and detect faces and objects (people, cars, bac)
while True:

    # ONLY FOR CAMERA
	# grab the frame from the threaded video stream
    # frame = vs.read()

    ## ONLY FOR VIDEO
    (grabbed, frame) = stream.read()
    # if the frame was not grabbed, then we have reached the
    # end of the stream
    if not grabbed:
        break

    print("[INFO] Object detection...")
    frame_object_detection_cropped = frame[0:480, 184:664] # Dimensions depend on your input video
    frame_object_detection_resized = imutils.resize(frame_object_detection_cropped, height=224)
    frame = imutils.resize(frame_object_detection_cropped, width = 750)
    cv2.imwrite('foto.png', frame_object_detection_resized)
    frame_object_detection = mpimg.imread('foto.png')
    cv2.imshow("X_tests",frame_object_detection)

    if(True): # Put here a condition in order to choose when to execute the object detection. Default: Always

        y_pred = model.predict(frame_object_detection[np.newaxis, :])
        y_pred_corr=y_pred.round(0).squeeze()
        MP=np.uint8(y_pred_corr[:,:,2]) # Mascara Personas
        MC=np.uint8(y_pred_corr[:,:,1]) # Mascara Coches

	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = frame
    r = frame.shape[1] / float(rgb.shape[1])

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame, then compute
	# the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
	# loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

		# check to see if we have found a match
        if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
            name = max(counts, key=counts.get)
		
		# update the list of names
        names.append(name)

	# loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # if the video writer is None *AND* we are supposed to write
    # the output video to disk initialize the writer
    if writer is None and args["output"] is not None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 20, (frame.shape[1], frame.shape[0]), True)
    # if the writer is not None, write the frame with recognized
    # faces to disk
    #if writer is not None:
        #writer.write(frame)

    # check to see if we are supposed to display the output frame to
    # the screen
    if args["display"] > 0:
        y_pred_corr = cv2.resize(y_pred_corr, ( 750 , 750))
        frame = cv2.resize(frame, ( 750 , 750))
        added_image=frame.copy()
        added_image[y_pred_corr[:,:,0]==1,2]=255
        added_image[y_pred_corr[:,:,1]==1,1]=255
        added_image[y_pred_corr[:,:,2]==1,0]=255
        cv2.imshow("Frame", added_image)
        key = cv2.waitKey(1) & 0xFF

    if writer is not None:
        writer.write(added_image)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

# do a bit of cleanup
#cv2.destroyAllWindows()
#vs.stop()
stream.release()

# check to see if the video writer point needs to be released
if writer is not None:
	writer.release()