# Python for Medical Physicists
## Introduction:
Welcome to the "Python for Medical Physicists" course, a comprehensive learning journey designed by Dr. Hossein Naseri at the McGill Medical Physics Unit. This repository serves as a crucial component of the course materials, providing you with the resources needed to delve into the exciting realm of Python programming tailored specifically for medical physicists.

Throughout this course, you will embark on a learning adventure that covers the fundamentals of Python programming, equipping you with essential skills to navigate the world of coding with confidence. From grasping the basics of Python syntax to exploring advanced concepts, you will gain a solid foundation that forms the backbone of your programming proficiency.

But that's not all. Our curriculum extends beyond conventional programming. You'll discover how to design and create web applications, unlocking the potential to develop interactive and user-friendly interfaces. Dive into the intricacies of database interaction, gaining valuable insights into managing and manipulating data for your medical physics endeavors.

As a medical physicist, understanding and working with DICOM images is paramount. In this course, we dedicate a significant portion of the curriculum to guide you through the intricacies of handling DICOM images using Python, empowering you to leverage this knowledge in your medical imaging projects.

Venture into the realm of machine learning with Python, where you'll explore the basics of this transformative technology. Gain hands-on experience in implementing machine learning algorithms, allowing you to harness the power of data-driven insights in your medical physics applications.

Additionally, we recognize the importance of version control, writing test cases, and project deployment in a professional programming environment. You'll master these essential skills, ensuring that your code is robust, error-free, and ready for deployment in real-world scenarios.

Embark on this enriching learning experience, where the fusion of Python programming and medical physics opens up a world of possibilities. Get ready to transform your understanding of coding and apply it to the dynamic and innovative field of medical physics. Let's code for a healthier future!

# Creating Web Applications Using Python, Flask, and Postgres

## Requirements:
### Python virtual environment
Install and activate python virtual environment

```
pip install virtualenv
mkdir our_server
virtualenv env
source env/bin/activate
```

### Postgress Database
Use this link to install and run the Postgress database


### Test psql function
Make sure that your `psql` command is working. If not you need to add `psql` path to your system path.
Add to path `C:\Program Files\PostgreSQL\12\bin`
```
psql -U postgres
CREATE DATABASE my_db;
```

## Add patient table to database
We need to create three sample TABLES in database. Script `create_db.py` is generated to create postgress tables.

## Start Web Server
use pip3 to install Flask
```
pip3 install Flask
```

# Flask web form
This tutorial we will start building interactable web form using Flask and postgres.
We will start by creating a relational table for images of the patients:

- open your application directory (or create an empty folder in your drive if want to start from scratch.)
- create an empty folder in your application directory names static this will include your static objects like images 
- create another folder called templates in your application directory this will contain template HTML pages for your application
- download some sample images into your static folder. You can use the one from github 

We create a relational table in our Postgres DB. Using the `create_db.py` we created three tables for some sample patients.

Open your **pgAdmin 4** and make sure that your PATIENT table has been created under 
*Servers > postgreSQL > Databases > postgres > Schemas > tables*

I want to review the `create_db.py` to show how we created `IMAGE `table with `imageID`, `image name` and `image path` and  `patient_image` table relating `patientid` 
from `PATIENT` table to `imageid` from `IMAGE` table.

```
import psycopg2

DATABASE = "my_db"
USER = "postgres"
PASSWORD = "<>"
HOST = "127.0.0.1"
PORT = "5432"

def create_table_database(cur):
    cur.execute("DROP TABLE IF EXISTS IMAGE")
    cur.execute('''CREATE TABLE IMAGE
          (IMAGEID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          FULLPATH            TEXT     NOT NULL);''')
    cur.execute("DROP TABLE IF EXISTS PATIENT_IMAGE")
    cur.execute('''CREATE TABLE PATIENT_IMAGE (
                PATIENTID INTEGER NOT NULL,
                IMAGEID INTEGER NOT NULL,
                PRIMARY KEY (PATIENTID , IMAGEID),
                FOREIGN KEY (PATIENTID)
                    REFERENCES PATIENT (PATIENTID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (IMAGEID)
                    REFERENCES IMAGE (IMAGEID)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        ''')

def insert_to_database(cur):
     Image_list = [
            [1, 'bladder','p1_images/bladder.png'],
            [2, 'brain', 'p1_images/brain.png'],
            [3, 'heart', 'p1_images/heart.png'],
            [4, 'kidney','p1_images/kidney.png'],
            [5, 'liver', 'p1_images/liver.png'],
            [6, 'lung', 'p1_images/lung.png'],
            [7, 'stomach','p1_images/stomach.png'],
            [8, 'bladder','p2_images/bladder.png'],
            [9, 'brain', 'p2_images/brain.png'],
            [10, 'heart', 'p2_images/heart.png'],
            [11, 'kidney','p2_images/kidney.png'],
            [12, 'liver', 'p2_images/liver.png'],
            [13, 'lung', 'p2_images/lung.png'],
            [14, 'stomach','p2_images/stomach.png']
        ]
    patient_image = [
            [1,1],
            [1,2],
            [1,3],
            [1,4],
            [1,5],
            [1,6],
            [1,7],
            [2,8],
            [2,9],
            [2,10],
            [2,11],
            [2,12],
            [2,13],
            [2,14]
        ]

    try:
        for row in Image_list:
            cur.execute("INSERT INTO IMAGE (IMAGEID,NAME,FULLPATH) \
                VALUES (%i, '%s', '%s')"%(row[0],row[1],row[2]))
            # cur.execute("UPDATE IMAGE SET FULLPATH = '%s' \
            #     WHERE IMAGEID = %i"%(row[2],row[0]))
    except Exception as e:
        print (e)
    try:
        for row in patient_image:
            cur.execute("INSERT INTO PATIENT_IMAGE (PATIENTID,IMAGEID) \
                VALUES (%i, %i)"%(row[0],row[1]))
    except Exception as e:
        print (e)


def read_db(cur, table):
    cur.execute('SELECT * FROM %s'%table)
    rows = cur.fetchall()
    for row in rows:
        print (row)

def main():
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    print("Database opened successfully")
    cur = con.cursor()
    create_table_database(cur)
    insert_to_database(cur)
    con.commit()
    # following function is to test that your database is created correctly
    # read_db(cur, 'IMAGE')
if __name__ == "__main__":
    main()
```
Once your created tables you can use `read_db(cur, 'IMAGE')` to make sure that your tables are crated correctly. In this example `'IMAGE'` is the 
name of the `IMAGE` table.

We are going to start creating a new web app based on what we learned last week. Open a new 
Make a python script named test_app.py (you can choose any name that you want)
Add the scripts to your `test_app.py` and save it.

```
from flask import Flask, Response, render_template
import os

DATABASE = "my_db"
USER = "postgres"
PASSWORD = "<>"
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
 

Inside templates folder create home.html and add the following HTML to create table, text box and submit botton.
 <table style="width:40%" border="1">
    <caption>{{title}}</caption>
  <tr> 
  <form method="POST">
   <th>Patient ID <input name="p_id"> </th>
    <th>Name<input name="p_name"></th>
    <th>Age <input name="p_age"></th>
    <th>Weight <input name="p_weight"></th>
    <th>Treatment<input name="p_treatment"></th>
    <td>
    <input type="submit">
</td>
</form>
</table>
```
Run `test_app.py`
You should get this message:
```
 * Serving Flask app "test_app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 104-284-776
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Check home http://127.0.0.1:5000/home


`@app.route('/home', methods=['GET'])` is decorator to create `/home` page with the get `method.Render_template`
is rendering template `home.html` file with following arguments `user_image = 'none'`, `title='Patient List'`, 
`column_names = []`, `rows=[]`
We will use these arguments inside `html`. In `home.html` passed argument using `{{}}` like  `{{title}}`.

Now add the post decorator to `test_app.py` to upload data from the database.

```
from flask import Flask, render_template
from flask import  request, Response
import psycopg2
import os

DATABASE = "my_db"
USER = "postgres"
PASSWORD = "<>"
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

app.run()
```
Make sure that `app.run()` command is always at the end of your script. 
Update your `home.html` file to write rows from the database into the table
```
 <table style="width:40%" border="1">
    <caption>{{title}}</caption>
  <tr> 
  <form method="POST">
   <th>Patient ID <input name="p_id"> </th>
    <th>Name<input name="p_name"></th>
    <th>Age <input name="p_age"></th>
    <th>Weight <input name="p_weight"></th>
    <th>Treatment<input name="p_treatment"></th>
    <td>
    <input type="submit">
</td>
</form>
</tr>
  {% for row in rows %}
 <tr> 
    {% for element in row %}
    <td>{{ element }}</td>
    {% endfor %}
</tr>
    {% endfor %}
</table>
```
In `test_app.py`;  `Request.form[<id>]` is function to request argument from HTML file and 
creates query based on the requested arguments. In `home.html`;
```
{% for row in rows %} <tr> </tr> {% endfor %}
Is for loop ittrates over rows.and
{% for element in row %} <td>{{ element }}</td> {% endfor %} 
Is for loop to ittrates over elements on objects (columns) of each row.
```

Running `test_app.py` you can query database. For example, if I search for patients with treatment z, I get

Now, let’s add another page to interact with images. Add the two buttons to your home.html to be able to switch between pages

```
<form method="get">
<button name="homeBtn" formaction="/home" type="submit">Home</button>
<button name="imageBtn" formaction="/image" type="submit">Image</button>
</form>
<table style="width:40%" border="1">
    <caption>{{title}}</caption>
  <tr> 
  <form method="POST">
   <th>Patient ID <input name="p_id"> </th>
    <th>Name<input name="p_name"></th>
    <th>Age <input name="p_age"></th>
    <th>Weight <input name="p_weight"></th>
    <th>Treatment<input name="p_treatment"></th>
    <td>
    <input type="submit">
</td>
</form>
</tr>
  {% for row in rows %}
 <tr> 
    {% for element in row %}
    <td>{{ element }}</td>
    {% endfor %}
</tr>
    {% endfor %}
</table>
```


Now we can add a decorator to create an image page. 
Make sure your static folder is created and you have following folders and objects in it.

Inside templates folder create `image.html` and add the following HTML to create a home button and a sow test image.
```
<form method="get">
<button name="homeBtn" formaction="/home" type="submit">Home</button>
</form>

<body>
    <img src="{{ user_image }}" alt="User Image">
</body>
</html>
```

Now add a decorator to your test_app.py to render `image.html` and pass test image.
Click on the image button on the home page to open the image page. You should see this.

Press on the *home* button to return to the home page.

Now we want to add function to read patients’ image tables from the database and browse the list of the images.

In test_app.py add the POST decorator to end of your script to read database
```
# . . . 

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

app.run()
```
This might a bit complicated to follow but I will try to explain every step. 
But before that let’s make sure that our web app functioning correctly. So, In `image.html` 
add the following HTML code to create a text box and a drop-down menu and handle arguments passed by the decorator.
```
<form method="get">
<button name="homeBtn" formaction="/home" type="submit">Home</button>
</form>

Patient ID: 
<!--  {{user_image}}  -->
<form method="POST">
    <input value={{p_id}} name="p_id">
    <input type="submit">
<label for="images">Choose Image:</label>
<select id="images" name="images" method="POST"> 

{% for row in rows %} 
    {% if row[2] == select_image %}
        <option value="{{ row[2] }}" SELECTED>{{ row[1] }}* </option>;
    {% else %}
        <option value="{{ row[2] }}">{{ row[1] }} </option>;
    {% endif %}
{% endfor %}

</select>
<button type="load" class="btn btn-default">Go</button>
</form>

<body>
    <img src="{{ user_image }}" alt="User Image">
</body>
</html>
```
Go to the image page and you should see the following.

In the Patient ID text box insert 1 and press submit you should see the list of the patient’s images. 
Then select an image from the dropdown menu and press go images of the selected organ from a selected patient will be browsed. 

Let me go through some of the functions in both test_app.py and `image.html`.
`image.html` has 3 parts

```
<form method="POST">
    <input value={{p_id}} name="p_id">
    <input type="submit">
</form>
```
Is an input text box and submit button to collect and post/update user input  `p_id`. 

```
<label for="images">Choose Image:</label>
<select id="images" name="images" method="POST"> 
{% for row in rows %} 
    {% if row[2] == select_image %}
        <option value="{{ row[2] }}" SELECTED>{{ row[1] }}* </option>;
    {% else %}
        <option value="{{ row[2] }}">{{ row[1] }} </option>;
    {% endif %}
{% endfor %}
<button type="load" class="btn btn-default">Go</button>
```
Is creating a drop-down menu based on the provided rows from the database. 
Value `row[1]` is the name of the organ used for label and `row[2]` is an image path used to browse image from folder. 
If the statement is there to keep the user-selected option as default and Go button is po post user-selected option. 
Finally,  last part is the html frame to show broswed image

```
<body>
    <img src="{{ user_image }}" alt="User Image">
</body>
```
Load_patient function in test_app.py has a quite complicated query for joining two tables.
```
query = """SELECT IMAGE.IMAGEID, IMAGE.NAME, IMAGE.FULLPATH FROM IMAGE 
            INNER JOIN PATIENT_IMAGE ON IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID 
            WHERE PATIENT_IMAGE.PATIENTID=%s"""%(p_id)
```
We have `PATIENTID` which is not stored in `IMAGE` table so we need to query `PATIENT_IMAGE` table to get `IMAGEID`s 
assigned to the selected `PATIENTID` and use those `IMAGEID`S to query `IMAGE` table. 
Therefore, we query an image name and image path from the `IMAGE` table. 
To get the image id we joined this table to `PATIENT_IMAGE` considering that `IMAGEID`s are common between two tables 
(`IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID`) and we can filter user-selected patient id from `PATIENT_IMAGE`. 
```
select_image = request.form.get('images')
```
Gets the path of the user-selected organ and finally, it renders the image.html with data from database and path to the image.

```
    full_filename = os.path.join(app.config['ORGAN_FOLDER'], select_image)
    return render_template("image.html", user_image = full_filename
                                        , rows = results,
                                        p_id = p_id,
                                        select_image = select_image
                                        )
app.run()
```
The last thing that I think might be useful is to know how to make plots and publish them on your webpage.

In your templates folder create `plot.html`
```
<form method="get">
<button name="homeBtn" formaction="/home" type="submit">Home</button>
</form>
<img src="/plot.png" alt="my plot">
```
Now we need to add function to for the plots and a decorator to create and to publis it. Add requred packages to the top of your script (this is a common practice to keep all requred packages on the top of the script) and following secton to the end of your python script.
```
import io
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# . . . 

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
```
`plot_png` calls `create_figure` to generate plot canvas.
`show_plot` renderers `plot.html` to publish created plot. Running `test_app.py`  you should get sample sine function in the page.
http://127.0.0.1:5000/plot


# Conclusion
In this tutorial, I was hoping to help you to set up a web app with Flask and Postgres and design a simple user interface 
to interact with data. Some of you might need to create interactive graphs for this purpose you might need to use `javascript`
based plotting tools such as `mpld3`, `plotly` or `Bokeh`. 
The complete tutorial is in the test_server directory in the following repository: 
```
git clone git@github.com:hn617/pythonTutorials.git
``` 
Please let me know if you need any specific functions in your application. 



