
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template, request


import cv2
import numpy as np
from PIL import Image

import re
from io import BytesIO
from PIL import Image
import base64

from tensorflow.keras.models import load_model

model = load_model('covid19.model')

def predict(image):
    image = cv2.resize(image, (224,224) )
    image =image.reshape((1, 224, 224,3))
    image =image /255.0
    return model.predict(image)[0]  

  



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@app.route('/', methods=['post', 'get'])
def login():
        
    return render_template('final.html')



@socketio.on('my event', namespace='/test')
def handle_message(data):   
    image_b64 = data['data']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im = im.convert("RGB")
    im=np.array(im)
    
    positive,negative=predict(im)
    
    emit('log', dict(data=str(positive),d=str(negative)), broadcast=True)
    






    
socketio.run(app,debug=True )

