
from flask_socketio import SocketIO
from flask_socketio import send, emit

import cv2
import numpy as np
from PIL import Image

import re

from io import StringIO
from io import BytesIO
from PIL import Image
import base64

from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import os
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
model = load_model('covid19.model')
# summarize model.
#model.summary()
def predict(image):
    
    image = cv2.resize(image, (224,224) )
    image =image.reshape((1, 224, 224,3))
    image =image /255.0
    return model.predict(image)[0]  

  



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['SECRET_KEY'] = 'secret123456789'
socketio = SocketIO(app)


#run_with_ngrok(app)

@app.route('/', methods=['post', 'get'])
def login():
    
    message = ''
        
    return render_template('final.html')



@socketio.on('my event', namespace='/test')
def handle_message(data):
   

    image_b64 = data['data']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    #print(  data['data'] )
    
    im = Image.open(BytesIO(base64.b64decode(image_data)))

    im = im.convert("RGB")
    im=np.array(im)
    print(im.shape)
    positive,negative=predict(im)
    
    emit('log', dict(data=str(positive),d=str(negative)), broadcast=True)
    

##
##@socketio.on('my event', namespace='/test')
##def handle_message(data):
##    receive = data['data']
##    emit('log', payload, broadcast=True)



@app.route('/final', methods = ['GET', 'POST'])
def upload_file():
    

    positive="20"
    negative = "20"
    
    if request.method == 'POST':
        
        f = request.files['file']

        image = cv2.imdecode(np.frombuffer(f.stream.read() , np.uint8), -1)
        


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        positive,negative=predict(image)    
      


     
    #return render_template('predict.html',positive=positive,negative=negative,user_image="static/a.jpg")
    #return render_template('final.html')
    
socketio.run(app,debug=True)
