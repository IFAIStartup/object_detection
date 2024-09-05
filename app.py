from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image
import torch
torch.cuda.empty_cache()

app = Flask(__name__)
app.secret_key = 'hf7TZttb5L'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PREDICT_FOLDER'] = 'static/'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PREDICT_FOLDER'], exist_ok=True)



model = YOLO('yolov5n.pt')
model.cpu

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def predict_img():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    f.save(filepath)
                    flash("Image uploaded successfully", 'success')
                    image=Image.open(filepath)
                    results = model.predict(image, save=True, project=app.config['PREDICT_FOLDER'], exist_ok=True)
                    predict_filename = 'predict/' + filename
                    counts={}
                    for results in results:
                        boxes =results.boxes.cpu().numpy()
                        for box in boxes:
                            cls=int(box.cls[0])
                            if not cls in counts.keys():
                                counts[cls]=1
                            else:
                                counts[cls]+=1
                        label=[]
                        count=[]
                        for key in counts.keys():
                            label.append(model.names[key])
                            count.append(str(counts[key]))

                    return render_template('index.html', filename=predict_filename,label=label,count=count)
                except Exception as e:
                    flash(f'Error occurred: {str(e)}', 'error')
                    return redirect(request.url)
            else:
                flash('Please upload a valid file!', 'error')
                return redirect(request.url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
    
