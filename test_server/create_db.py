import psycopg2

DATABASE = "my_db"
USER = "postgres"
PASSWORD = "sarOtah"
HOST = "127.0.0.1"
PORT = "5432"

def create_table_database(cur):
    cur.execute("DROP TABLE IF EXISTS PATIENT")
    cur.execute('''CREATE TABLE PATIENT
          (PATIENTID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          AGE            INT     NOT NULL,
          WEIGHT        INT,
          TREATMENT        CHAR(1));''')

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
    patients_list = [
            [1, 'A', 38, 68, 'x'],
            [2, 'C', 52, 87, 'x'],
            [3, 'G', 87, 75, 'y'],
            [4, 'D', 32, 60, 'z'],
            [5, 'L', 15, 91, 'x'],
            [6, 'J', 32, 93, 'y'],
            [7, 'P', 45, 78, 'z'],
            [8, 'I', 32, 87, 'z'],
            [9, 'E', 79, 54, 'y'],
            [10, 'N', 31, 43, 'y'],
            [11, 'B', 90, 79, 'x'],
            [12, 'M', 22, 90, 'y'],
            [13, 'O', 15, 86, 'z'],
            [14, 'F', 8, 72, 'z'],
            [15, 'K', 63, 73, 'x']
        ]

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
    # try:
    #     for row in patients_list:
    #         cur.execute("INSERT INTO PATIENT (PATIENTID,NAME,AGE,WEIGHT,TREATMENT) \
    #             VALUES (%i, '%s', %i, %i, '%s')"%(row[0],row[1],row[2], row[3], row[4]))
    # except Exception as e:
    #     print (e)
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
    # this function is to test that your database is created correctly
    # read_db(cur, 'IMAGE')
if __name__ == "__main__":
    main()