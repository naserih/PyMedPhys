from flask import Flask, render_template
from flask import  request, Response
import psycopg2
import os
import io
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

DATABASE = "my_db"
USER = "postgres"
PASSWORD = "sarOtah"
HOST = "127.0.0.1"
PORT = "5432"

ORGAN_FOLDER = os.path.join('static')

app = Flask(__name__, template_folder='templates')
app.config['ORGAN_FOLDER'] = ORGAN_FOLDER
app.config["DEBUG"] = True


@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html", user_image = 'none', 
                                        title='Patient List',
                                        column_names = [],
                                        rows=[])
@app.route('/home', methods=['POST'])
def patient_form_post():
    p_id = request.form['p_id']
    p_name = request.form['p_name']
    p_age = request.form['p_age']
    p_weight = request.form['p_weight']
    p_treatment = request.form['p_treatment']


    query = "SELECT * FROM PATIENT WHERE"
    to_filter = []

    if p_id != '':
        query += ' patientid=%s AND'
        to_filter.append(p_id)
    if p_name != '':
        query += ' name=%s AND'
        to_filter.append(p_name)
    if p_age != '':
        query += ' age=%s AND'
        to_filter.append(p_age)
    if p_weight != '':
        query += ' weight=%s AND'
        to_filter.append(p_weight)
    if p_treatment != '':
        query += ' treatment=%s AND'
        to_filter.append(p_treatment)


    query = query[:-4] + ';'
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute(query, to_filter)
    colms = [desc[0] for desc in cur.description]
    results = cur.fetchall()

    return render_template("home.html", user_image = 'none', 
                                        title='Patient List',
                                        column_names = colms,
                                        rows=results)

@app.route('/image', methods=['GET'])
def show_list():
    p_id = 0
    full_filename = os.path.join(app.config['ORGAN_FOLDER'], 'test.png')
    return render_template("image.html", user_image = full_filename, p_id = p_id)

@app.route('/image', methods=['POST'])
def load_patient():
    p_id = request.form['p_id']
    if p_id != "": 
        query = """SELECT IMAGE.IMAGEID, IMAGE.NAME, IMAGE.FULLPATH FROM IMAGE 
            INNER JOIN PATIENT_IMAGE ON IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID 
            WHERE PATIENT_IMAGE.PATIENTID=%s"""%(p_id)
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        cur.execute(query)
        colms = [desc[0] for desc in cur.description]
        results = cur.fetchall()
    else:
        results = []
    if request.form.get('images'):
        select_image = request.form.get('images')
    else:
        select_image = ''
    full_filename = os.path.join(app.config['ORGAN_FOLDER'], select_image)
    return render_template("image.html", user_image = full_filename
                                        , rows = results,
                                        p_id = p_id,
                                        select_image = select_image
                                        )

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = np.arange(100)
    ys = np.sin(xs/10) 
    axis.plot(xs, ys)
    return fig

@app.route('/plot', methods=['POST', 'GET'])
def show_plot():
    return render_template("plot.html")

app.run()