from flask import Flask, request, render_template 
import json 
from werkzeug.utils import secure_filename 
from flask_cors import CORS, cross_origin 
import os 
import flask 
import io 
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
from keras.models import Model
from keras.models import load_model as keras_load_model 
import numpy as np
from flask import request
from flask import jsonify
from flask import Flask
import datetime

 
 
 
 
UPLOAD_FOLDER = 'E:/Projects/Python-Flask/ImageUploadAPI/UploadedImages/' 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 
 
 
app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['CORS_HEADERS'] = 'Content-Type' 
data = {} 
 
 
model = None 
 
 
def get_model(): 
    global model 
    model = keras_load_model('cancer_model_weights.hdf5') 
    model._make_predict_function() 
    print("* Keras ModelS Loaded!") 
 
 
get_model() 
 
 
def prepare_image(image, target): 
    image = image.resize(target) 
    return image 
 
 
 
@app.route("/",methods=["GET"]) 
def Home(): 
    return render_template('UploadImage.html') 
 
 
 
@app.route("/UploadImage",methods=['POST']) 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization']) 
def UploadImage(): 
    categories=['Benignant','Malignant'] 
    if(request.method == "POST"):    
        file = request.files["image"] 
        if file and allowed_file(file.filename): 
            current_timestamp = datetime.datetime.now().timestamp()
            filename = secure_filename(file.filename) 
            pathToSave = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(pathToSave) 
 
 
            image = request.files["image"]
            image = Image.open(pathToSave)
            #image = Image.open(pathToSave) 
            image = prepare_image(image, target=(112, 150)) 
            images_to_predict=np.array(image).reshape(-1,112,150,3)/255 
            preds = model.predict(images_to_predict) 
            predclass = categories[model.predict_classes(images_to_predict)[0][0]] 
 
 
            data["output"] = predclass 
            json_data=json.dumps(data) 
 
 
            return json_data 
 
 
 
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
 
 
app.run() 