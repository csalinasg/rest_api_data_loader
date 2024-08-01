from flask import Flask, render_template, json, jsonify, request
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
        file = form.file.data
        result = ingest_framework(file)
        return result
    return render_template('index.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'no file in the request'})
        resp.status_code = 400
        return resp
    else:
        resp = jsonify({'message' : 'request ok'})
        resp.status_code = 200
        file = request.files['file']
        result = ingest_framework(file)
        return jsonify({'message': result})

@app.route('/departments/quarter', methods=['GET'])
def query1():
    conn = get_connection()
    cur = conn.cursor()
    query = '''WITH temp_query as (
                SELECT "departament","job", count(*) as "employees",
                EXTRACT(QUARTER FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) as "quarter"
                FROM "hired_employees" as "he"
                INNER JOIN "departaments" as "d" on "d"."id" = "he"."departament_id"
                INNER JOIN "jobs" AS "j" on "j"."id" = "he"."job_id"
                where EXTRACT(YEAR FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
                group by "departament","job", EXTRACT(QUARTER FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"'))
                )
                SELECT *
                FROM temp_query
                PIVOT(SUM("employees") FOR "quarter" IN (ANY ORDER BY "quarter")DEFAULT ON NULL (0))
                AS p ("departament", "job", "Q1", "Q2", "Q3", "Q4")
                ORDER BY "departament";'''
    cur.execute(query)
    df = cur.fetch_pandas_all()
    results = df.to_dict(orient='records')
    return jsonify(results)

@app.route('/departments/top', methods=['GET'])
def query2():
    conn = get_connection()
    cur = conn.cursor()
    query = '''WITH c as (
                select "departament_id", count(*) as "q_employees" from "hired_employees" where EXTRACT(YEAR FROM TO_TIMESTAMP("datetime", 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
                group by "departament_id"
                )

                SELECT "d"."id" as "id_departament","d"."departament", count(*) as "employees"
                FROM "hired_employees" as "he"
                INNER JOIN "departaments" as "d" on "d"."id" = "he"."departament_id"
                INNER JOIN "jobs" AS "j" on "j"."id" = "he"."job_id"
                group by "d"."departament","d"."id"
                having count(*) > (select avg("q_employees") from c ) 
                order by count(*) desc;'''
    cur.execute(query)
    df = cur.fetch_pandas_all()
    results = df.to_dict(orient='records')
    return jsonify(results)


def ingest_framework(file):
    if allowed_file(file.filename) and allowed_names(file.filename):
            file_name, file_extension = os.path.splitext(file.filename)#se divide el archivo
            now = datetime.now()

            date_folder = now.strftime('%Y/%m/%d')
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], date_folder) #se crea ruta donde se guardan los archivos con formato yyyy/mm/dd
            
            os.makedirs(upload_folder, exist_ok=True)#se crea carpeta si no existe
    
            timestamp = now.strftime('%Y%m%d_%H%M%S%f')
            file_save = f"{file_name}_{timestamp}.csv"#ruta de archivo con timestamp para no duplicar archivos
            
            file_path = os.path.join(upload_folder, secure_filename(file_save))
            file.save(file_path)
            
            merge_data(file_name, file_path)
            return f"Archivo '{file.filename}' Cargado correctamente"
    else:
            return f"Archivo '{file.filename}' no permitido, solo se permiten archivos departments.csv, jobs.csv and hired_employees.csv"

def allowed_file(filename):
    file_name, file_extension = os.path.splitext(filename)#se divide el archivo
    
    for ext in allowed_file_types:
        if file_extension == ext:
            return True
    return False

def allowed_names(filename):
    file_name, file_extension = os.path.splitext(filename)

    config = files_configuration.get(file_name)

    if config:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)