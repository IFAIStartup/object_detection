from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.utils import secure_filename
import uuid
import os
from ultralytics import YOLO






app = Flask(__name__)
app.secret_key = 'hf7TZttb5L'
app.config['UPLOAD_FOLDER']= 'static/uploads/'



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png' ,'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def predict_img():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            if f and allowed_file(f.filename):
                filename="image.png"
                filepath=(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                f.save(filepath)
                print("upload folder:",filepath)
                if filename=='image.png':
                    flash("Image upload sucessfully",'success')
                model=YOLO('best.pt')
                model.predict('static/uploads/image.png',save='True', project='static', exist_ok=True)
                filename='predict'+'/'+filename
            
                
                              
                         
                return render_template('index.html',filename=filename)
                
            else:
                flash('please upload file !','error')   
            redirect(request.url)
    return render_template("index.html")


if __name__=="__main__":
    app.run(port=10000,debug=True)
              
