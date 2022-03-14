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
import io
import zlib

from flask import Flask, request, Response
import numpy as np
import os
import cv2
import jsonpickle

# ## CONFIG
SERVER_HOST= "localhost"
SERVER_PORT = 12345
API_PATH = "/api/test"
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
    #
    data = uncompress_nparr(r.data) #uncompress data
    print("data type:{}", type(data))
    #nparr = np.frombuffer(r.data, np.uint8)

    is_success, buffer = cv2.imencode(".jpg", data)
    io_buf = io.BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)  # image
    #img = cv2.imdecode(nparr , cv2.IMREAD_COLOR)
    img_name = "Received_JuanJoxe{}.png".format(img_counter)

    cv2.imwrite(os.path.join(uploads_dir, img_name), decode_img)

    #
    data10 = data*10
    print("\n\nReceived array (compressed size = "+\
          str(r.content_length)+"):\n"+str(data))
    resp, _, _ = compress_nparr(data)
    response = {'message': 'image received. size={}x{} name:{}'.format(decode_img.shape[1], decode_img.shape[0], img_name)} #this is json
    print('message image received. size={}x{} name:{}'.format(decode_img.shape[1], decode_img.shape[0], img_name))


    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)



