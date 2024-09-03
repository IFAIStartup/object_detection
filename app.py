from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)
app.secret_key = 'hf7TZttb5L'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PREDICT_FOLDER'] = 'static/predict/'

# Ensure upload and prediction folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PREDICT_FOLDER'], exist_ok=True)

# Load the model once at startup
model = YOLO('best.pt')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def predict_img():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            if f and allowed_file(f.filename):
                filename = secure_filename('image.png')
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    f.save(filepath)
                    flash("Image uploaded successfully", 'success')

                    # Perform prediction
                    results = model.predict(filepath, save=True, project=app.config['PREDICT_FOLDER'], exist_ok=True)

                    # Update filename for display
                    filename = 'predict/' + filename

                    return render_template('index.html', filename=filename)
                except Exception as e:
                    flash(f'Error occurred: {str(e)}', 'error')
                    return redirect(request.url)
            else:
                flash('Please upload a valid file!', 'error')
                return redirect(request.url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
    
