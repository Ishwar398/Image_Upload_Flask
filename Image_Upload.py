from flask import Flask, request, render_template
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os

UPLOAD_FOLDER = 'E:/Projects/Python-Flask/ImageUploadAPI/UploadedImages/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
data = {}


@app.route("/",methods=["GET"])
def Home():
    return render_template('UploadImage.html')


@app.route("/UploadImage",methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def UploadImage():
    if(request.method == "POST"):   
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pathToSave = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pathToSave)

            data["output"] = "Successfully Saved the Image"
            data["ImageName"] = secure_filename(file.filename)
            data["SavePath"] = pathToSave
            json_data=json.dumps(data)

            return json_data


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.run()
        
        
