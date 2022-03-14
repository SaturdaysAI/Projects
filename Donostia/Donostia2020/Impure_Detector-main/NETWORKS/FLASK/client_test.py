################################################################################
### client.py
################################################################################


#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
Dummy client, interacts with the server sending and receiving
compressed numpy arrays.

Run:
python client.py
"""


from __future__ import print_function
import io
import numpy as np
import zlib
import requests
import cv2
import imageio
import json
# ## CONFIG

SERVER_HOST= "localhost"
SERVER_PORT = 12345
API_PATH = "/api/test"
test_url = SERVER_HOST + API_PATH

# ## HELPERS

def compress_nparr(nparr):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, nparr)
    uncompressed = bytestream.getvalue()
    compressed = zlib.compress(uncompressed)
    return compressed, len(uncompressed), len(compressed)

def uncompress_nparr(bytestring):
    """
    """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))

# ## MAIN CLIENT ROUTINE
cam = cv2.VideoCapture(1)   #WebCam, if is not working change the number

cv2.namedWindow("test")     #Windows name
url = "http://"+SERVER_HOST+":"+str(SERVER_PORT)+API_PATH
while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            #break           #to avoid close the program
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()
            break
        elif k % 256 == 32:
            # SPACE pressed
            # img_name = "opencv_frame_{}.png".format(img_counter)    #names for the files
            # grab an image from the camera
            # imeread from memory
            # img = cv2.imread('lena.jpg')
            # img = cv2.imread('.jpg', frame)
            # _, img_encoded = cv2.imencode('.jpg', img)

            img = frame
            # encode
            is_success, buffer = cv2.imencode(".jpg", img)
            io_buf = io.BytesIO(buffer)                                                  #not an image
            # decode
            decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)  #image
            print("decode_img type:{}", type(decode_img))
            #imageio.imwrite('irudia.jpg', decode_img)

            #bytestream = io.BytesIO()
            #np.save(bytestream, decode_img)

            #input("\n\npress return...")
            compressed, u_sz, c_sz = compress_nparr(decode_img)
            #
            print("\nsending array to", url)
            print("size in bits (orig, compressed):", u_sz, c_sz)
            print ("decode_img type:{}",type(decode_img))
            print("compressed type:{}", type(compressed))
            #
            resp = requests.post(url, data=compressed,
                                 headers={'Content-Type': 'application/octet-stream'})  #HTTP
            #
            print("\nresponse:")
            #data = uncompress_nparr(resp.content)  #uncompress the response
            #print (data)
            dataJaso = resp.content
            #print (dataJaso)
            print(json.loads(dataJaso))
