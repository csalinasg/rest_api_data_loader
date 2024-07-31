from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from datetime import datetime
from config import *
from ingestion import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'challenge'
app.config['UPLOAD_FOLDER'] = 'data'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        print(form) #validar la salida del formulairo
        file = form.file.data
        if allowed_file(file.filename):
            file_name, file_extension = os.path.splitext(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
            file_save = f"{file_name}_{timestamp}.csv"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_save)))
            merge_data(file_name, f"data/{file_save}")
            return f"Archivo '{file.filename}' Cargado correctamente"
        else:
            return "Archivo no permitido, solo se permiten CSV"
    
    return render_template('index.html', form=form)

def allowed_file(filename):
    file_extension = filename.lower().rsplit('.', 1)[-1]
    
    for ext in allowed_file_types:
        if file_extension == ext.strip('.'):
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)