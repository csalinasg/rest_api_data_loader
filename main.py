from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

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
        #print("Form data:", form.data) validar la salida del formulairo
        file = form.file.data
        if allowed_file(file.filename):    
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return f"Archivo '{file.filename}' Cargado correctamente"
        else:
            return "Archivo no permitido, solo se permiten CSV"
    
    return render_template('index.html', form=form)

def allowed_file(filename):
    return filename.lower().endswith('.csv')

if __name__ == '__main__':
    app.run(debug=True)