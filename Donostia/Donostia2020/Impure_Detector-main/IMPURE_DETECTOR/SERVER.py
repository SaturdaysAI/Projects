################################################################################
### server.py
################################################################################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Dummy server, interacts with the client receiving, altering and returning
compressed numpy arrays.
Setup/run:
 1. pip install Flask --user
 2. export FLASK_APP=server.py; flask run
"""

# ### MODULES
import io
import zlib
from flask import Flask, request, Response, jsonify
# VISION
import numpy as np
import os
import cv2
import jsonpickle
import json
import time
import ssl
import sys
from modules import impure_detector



# ## CONFIG
# FLASK
#SERVER_HOST= "localhost"
SERVER_HOST = '192.168.1.59'
SERVER_PORT = 8090
API_PATH = "/api/test"
# VISION




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

# ## MAIN SERVER DESCRIPTOR/ROUTINE

# Initialize the Flask application
app = Flask(__name__)
img_counter = 0

# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, 'jasoak')
os.makedirs(uploads_dir, exist_ok=True)

# route http posts to this method
@app.route(API_PATH, methods=['POST'])
def test1234():
    """
    Expects a compressed, binary np array. Decompresses it, multiplies it by 10
    and returns it compressed.
    """
    r = request
    data = uncompress_nparr(r.data) #uncompress data



    is_success, buffer = cv2.imencode(".jpg", data)
    io_buf = io.BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)  # image
    #---------------------------------------------------------------------
    results, violations = impure_detector(decode_img)

    # Bug fix variable metrics
    try:
        if not isinstance(results[0][0], list):
            aux = (-1, (0, 0, 0, 0), (0,-1))
            results.append(aux)
    except IndexError:
        print("size of: ",results)
    #---------------------------------------------------------------------

    '''
    print("\n\nReceived array (compressed size = "+\
          str(r.content_length)+"):\n"+str(data))
    '''

    # build a response dict to send back to client
    response_pickled = jsonpickle.encode([results, violations])
    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)


