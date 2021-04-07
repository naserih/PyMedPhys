from flask import Flask, Response, render_template
import os

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
app.run()