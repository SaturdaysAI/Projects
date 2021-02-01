#!/usr/bin/env python
# coding: utf-8

# # YOLOv4-tiny: DISTANCE DETECTOR

# ### MODULES
import cv2
import numpy as np
import time
from scipy.spatial import distance as dist
import os
import ssl
import sys
import json
import time


cv2. __version__

# ### IMPORT ALGORITH

net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4_tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]



#           ******************************* FUNCTIONS ***************************************

def PERSON_FLTR_1(OUTS, THRESHOLD, H,W):
    
    class_ids = []
    confidences = []
    boxes = []
    centroids = []
    
    for out in OUTS:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # PERSON DETECTED
            if (confidence > THRESHOLD) and class_id == 0: 

                center_x = int(detection[0]*W) 
                #from the bounding box to the center
                center_y = int(detection[1]*H) 
                #from the bb to cy
                w = int(detection[2]*W)
                h = int(detection[3]*H)
                
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                centroids.append((center_x,center_y))
                
                
    return   class_ids,confidences, boxes, centroids 


def PERSON_FLTR_2(IDX,ID,CONF, BB, CENTROIDS):
    
    results = []
    # loop over the indexes we are keeping
    for i in IDX.flatten():
        # extract the bounding box coordinates
        (x, y) = (BB[i][0], BB[i][1])
        (w, h) = (BB[i][2], BB[i][3])
        # update our results list to consist of the person
        # prediction probability, bounding box coordinates,
        # and the centroid
        r = (CONF[i], (x, y, x + w, y + h), CENTROIDS[i])
        results.append(r)
    # return the list of results
    return results

# define the minimum safe distance (in pixels) that two people can be
# from each other
MIN_DISTANCE = 200 # Test/Error
n = 0 #camera
THRESHOLD = 0.4
H, W = 480,640
cap = cv2.VideoCapture(n)#0 for the first webcam and 1 for the second one
                        #...and if we want just put a video folder here
#GET FRAMES IN REAL TIME:
start_time = time.time() #colect start time
frame_id = 0 #colects frame quanty


def YOLO(frame, net, output_layers):

    #Standard Yolo Size 320x 320 /416 x 416
    # Function = blobFromImage(imag, scale_factor, size,mean*, swapRB*, crop)
    blob = cv2.dnn.blobFromImage(frame, (1 / 255.0),
                                 (320,320),(0,0,0), True, crop = False)
    net.setInput(blob)
    # 2 Detections (300, 85) / (1200, 85)
    OUTS = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    centroids = []
    results = []
    for out in OUTS:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # PERSON DETECTED
            if (confidence > THRESHOLD) and class_id == 0:
                center_x = int(detection[0] * W)
                # from the bounding box to the center
                center_y = int(detection[1] * H)
                # from the bb to cy
                w = int(detection[2] * W)
                h = int(detection[3] * H)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                centroids.append((center_x, center_y))

    # NON MAX SUPPRESSION
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.5)
    # if not this...error
    if len(indexes) > 0:
        # loop over the indexes we are keeping
        for i in indexes.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # update our results list to consist of the person
            # prediction probability, bounding box coordinates,
            # and the centroid
            r = (confidences[i], (x, y, x + w, y + h), centroids[i])
            results.append(r)

    return results

def impure_detector(frame):

    flag = False
    violations = set()
    results = YOLO(frame, net, output_layers)

    # extract all centroids from the results and compute the
    # Euclidean distances between all pairs of the centroids
    centroids = np.array([r[2] for r in results])
    # A little bug
    try:
        D = dist.cdist(centroids, centroids, metric="euclidean")
    except Exception:
        flag = True
        pass
    if (not flag):
        # loop over the upper triangular of the distance matrix
        for i in range(0, D.shape[0]):
            for j in range(i + 1, D.shape[1]):
                # check to see if the distance between any two
                # centroid pairs is less than the configured number
                # of pixels
                Dpatch = np.amax(D[i, j])  # Error in calculous

                if Dpatch < MIN_DISTANCE:
                    # UPDATE VIOLATIONS
                    violations.add(i)
                    violations.add(j)
    violations.add(-1)
    violations.add(-2)
    return [results, violations]

#           ******************************* FUNCTIONS ***************************************
