import os
import io
from flask import Flask, flash, jsonify, render_template, request, send_file, url_for, send_from_directory
import numpy as np
from dicom_utils import get_cts
from PIL import Image, ImageEnhance, ImageOps
import env
import json
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from skimage.io import imsave, imread
# import _tkinter
# from scipy import ndimage


output_path = env.OUTPUTDATA
db = env.PATIENTS_DATABASE
# images_url = 'http://127.0.0.1:5000/images'

SERVER_IP = env.SERVER_IP
SERVER_PORT = env.SERVER_PORT

images_url = 'http://%s:%s/images'%(SERVER_IP,SERVER_PORT)
KEYS = env.VALID_KEYS


def load_dicoms(patient_file_path, patient_file):
    # folder_path = r'C:\Users\FEPC-L389\Google Drive\1_PhDProject\Galenus\DICOMfortable\static\data\07-02-2003-p4-14571'
    # patient_image_path = r'/1.000000-P4P100S300I00003 Gated 0.0A-29193'
    # processedFiles = [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(output_path)]
    # print('processedFiles', processedFiles)
    # patient_filenames = [f for f in os.listdir(patient_file_path) if f not in processedFiles]
    # print('patient_filenames', patient_filenames)
    # patient_filenames = os.listdir(patient_file_path)
    patient_metadata = {}
    # for patient_file in patient_filenames:
    if not os.path.exists(os.path.join(patient_file_path, patient_file, 'XY')):
        os.makedirs(os.path.join(patient_file_path, patient_file, 'XY'))
        print ('ERROR: NO CT IMAGES FOR PATIENT %s' %patient_file)
    if not os.path.exists(os.path.join(patient_file_path, patient_file, 'XZ')):
        os.makedirs(os.path.join(patient_file_path, patient_file, 'XZ'))
    if not os.path.exists(os.path.join(patient_file_path, patient_file, 'YZ')):
        os.makedirs(os.path.join(patient_file_path, patient_file, 'YZ'))
    patient_metadata[patient_file] = {}
    ct_file = [os.path.join(patient_file_path, patient_file, 'XY', f) for f in os.listdir(os.path.join(patient_file_path, patient_file, 'XY'))]
    patient_metadata[patient_file]['xz_path'] = os.path.join(patient_file_path, patient_file, 'XZ')
    patient_metadata[patient_file]['yz_path'] = os.path.join(patient_file_path, patient_file, 'YZ')
    patient_metadata[patient_file]['xy_path'] =  os.path.join(patient_file_path, patient_file, 'XY') 
    patient_metadata[patient_file]['ct_array'], \
    patient_metadata[patient_file]['ct_array_hu'], \
    patient_metadata[patient_file]['ct_x'], \
    patient_metadata[patient_file]['ct_y'], \
    patient_metadata[patient_file]['ct_z'], \
    patient_metadata[patient_file]['ct_spacing'], \
    patient_metadata[patient_file]['ct_index'], = get_cts(ct_file)
    X = ['wadouri:%s/%s/XY/%s'%(images_url,patient_file,f) for f in os.listdir(os.path.join(patient_file_path, patient_file, 'XY'))]        
    Y = patient_metadata[patient_file]['ct_index']
    # print (patient_file, patient_metadata[patient_file]['ct_array'].shape, patient_metadata[patient_file]['ct_spacing'])
    Z = [x for _,x in sorted(zip(Y,X))]
    Z.reverse()
    patient_metadata[patient_file]['xy_file'] = Z
        # patient_metadata[patient_file]['xz_file'] = [os.path.join(patient_file_path, patient_file, 'XZ', f) for f in os.listdir(os.path.join(patient_file_path, patient_file, 'XZ'))]
        
    # print (patient_metadata[patient_filenames[0]])
    
    
    # ct_array_hu = window_image(ct_array_hu, 400,1000)
    # ct_array_hu = ndimage.zoom(ct_array_hu, [1*ct_spacing[2],2*ct_spacing[1],2*ct_spacing[0]])
    # print ('ct_spacing', ct_spacing, ct_array.shape, ct_array_hu.shape)
    # print (np.min(ct_array), np.min(ct_array_hu), np.max(ct_array), np.max(ct_array_hu))
    # if not os.path.exists('./static/images/%s'%(patientIndex)):
    #     os.makedirs('./static/images/%s'%(patientIndex))
    return patient_metadata

def window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max    
    return window_image

def savePoints(pid, points):
    np.savetxt('%s_points.out'%(pid), x, delimiter=',')

def load_pngs(patient_file_path, patient_metadata):
    for patient in patient_metadata:
        patient_metadata[patient]['xz_file'] = ['%s/%s/XZ/%s'%(images_url,patient,f) for f in sorted(os.listdir(os.path.join(patient_file_path, patient, 'XZ')))]
        patient_metadata[patient]['yz_file'] = ['%s/%s/YZ/%s'%(images_url,patient,f) for f in sorted(os.listdir(os.path.join(patient_file_path, patient, 'YZ')))]
        # patient_metadata[patient]['xz_file'] = os.listdir(os.path.join(patient_file_path, patient, 'XZ'))
        # patient_metadata[patient]['yz_file'] = os.listdir(os.path.join(patient_file_path, patient, 'YZ'))
    return patient_metadata


def updatePatientList(patient_file_path, directory):
    processedFiles = [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(directory)]
    # print('processedFiles: ', processedFiles)
    new_patient_filenames = [f for f in os.listdir(patient_file_path) if f not in processedFiles]
    # print('new_patient_filenames: ', new_patient_filenames)
    return new_patient_filenames



# print(patient_metadata[patient_filenames[0]]['xz_file'] )
# print("xy vvvvv")
# print(patient_metadata[patient_filenames[0]]['xy_file'] )

# ct_array_hu = patient_metadata[patient_filenames[0]]['ct_array_hu']
# ct_spacing = patient_metadata[patient_filenames[0]]['ct_spacing']
# print(patient_filenames[0], np.amin(patient_metadata[patient_filenames[0]]['ct_array_hu']), np.amax(patient_metadata[patient_filenames[0]]['ct_array_hu']))
# print(patient_filenames[0], np.amin(patient_metadata[patient_filenames[0]]['ct_array']), np.amax(patient_metadata[patient_filenames[0]]['ct_array']))


app = Flask(__name__)

# No caching at all for API endpoints.

# app.config["CLIENT_IMAGES"] = "./static/patients/09251/XZ"
# app.config["PATIENTS_XY_IMAGES"] = {}
# app.config["PATIENTS_XZ_IMAGES"] = {}
# app.config["PATIENTS_YZ_IMAGES"] = {}

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# patient_metadata = {}



@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.cache_control.max_age = 3
    return response

@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/images/<patient>/XY/<image_name>")
def get_patient_xy_image(patient, image_name):
    try:
        return send_from_directory(app.config["PATIENTS_DATA"][patient]['xy_path'], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/images/<patient>/YZ/<image_name>")
def get_patient_yz_image(patient, image_name):
    try:
        return send_from_directory(app.config["PATIENTS_DATA"][patient]['yz_path'], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/images/<patient>/XZ/<image_name>")
def get_patient_xz_image(patient, image_name):
    try:
        return send_from_directory(app.config["PATIENTS_DATA"][patient]['xz_path'], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/_load_patients')
def load_patients():
    access_key = request.args.get('key', 0, type=str)
    if access_key in KEYS: 
        directory = '%s/%s_%s/%s'%(output_path, access_key,KEYS[access_key][0],KEYS[access_key][1])
        if not os.path.exists(directory):
            os.makedirs(directory)

        patient_file_path = db[KEYS[access_key][1]]
        patients = updatePatientList(patient_file_path, directory)
        if len(patients) == 0:
            patients = ['DONE']
    else:
        patients = []

    return jsonify(patients = patients)

# print ('>>>> ', patient_metadata)
@app.route('/_load_patient_data')
def load_patient_data():
    access_key = request.args.get('key', 0, type=str)
    patientId = request.args.get('patientId', 0, type=str)

    patient_file_path = db[KEYS[access_key][1]]

    patient_metadata = load_dicoms(patient_file_path, patientId)
    patient_metadata = load_pngs(patient_file_path, patient_metadata)
    app.config["PATIENTS_DATA"] = patient_metadata
    xy_files = patient_metadata[patientId]['xy_file']
    xz_files = patient_metadata[patientId]['xz_file']
    yz_files = patient_metadata[patientId]['yz_file']
    ct_spacings = list(patient_metadata[patientId]['ct_spacing'])
    print (xy_files)
    print('ct_spacings')
    print(ct_spacings)
    return jsonify(xy_files = xy_files, 
                    xz_files = xz_files,
                    yz_files = yz_files,
                    ct_spacings = ct_spacings)



@app.route('/_post_points')
def post_points():
    
    patientId = request.args.get('patientId', 0, type=str)
    access_key = request.args.get('key', 0, type=str)
    ps = request.args.get('exportPoints', [])
    ps = np.fromstring(ps, dtype=int, sep=',')

    # print(len(ps), ps)
    # # wordlist = request.args.get('wordlist', [])
    patient_points = [[ps[i*3],ps[i*3+1], ps[i*3+2] ] for i in range(int(len(ps)/3))]
    print(patient_points)

    directory = '%s/%s_%s/%s'%(output_path, access_key,KEYS[access_key][0],KEYS[access_key][1])    
    np.savetxt('%s/%s.out'%(directory,patientId), patient_points, delimiter=',', fmt='%i')

    return jsonify(results = "DONE")




# @app.route('/_get_xy_image')
# def get_xy_slice():
#     z_val = request.args.get('z_val', 0, type=int)
#     xy_arr = ct_array_hu[z_val,:,:]
#     xy_arr_min, xy_arr_max = np.min(xy_arr), np.max(xy_arr)
#     xy_arr = 255*(xy_arr-xy_arr_min)/(xy_arr_max-xy_arr_min)
#     xy_img = Image.fromarray(xy_arr.astype('uint8'))
#     xy_imagePath = './static/images/%s/xy_%s.png'%(patientIndex,z_val)
#     xy_img.save(xy_imagePath)
#     return jsonify(xy_result = url_for('static',
#         filename='images/%s/xy_%s.png'%(patientIndex,z_val))
#     )

# @app.route('/_get_xz_image')
# def get_xz_slice():
#     y_val = request.args.get('y_val', 0, type=int)
#     xz_arr = ct_array_hu[:,y_val,:]
#     xz_arr_min, xz_arr_max = np.min(xz_arr), np.max(xz_arr)
#     xz_arr = 255*(xz_arr-xz_arr_min)/(xz_arr_max-xz_arr_min)
#     xz_img = Image.fromarray(xz_arr.astype('uint8'))
#     xz_img = ImageOps.flip(xz_img)
#     # xz_img = ImageOps.mirror(xz_img)
#     # print ('xz_arr', xz_arr.shape)
#     aspect_ratio = ct_spacing[0]/ct_spacing[2]
#     if aspect_ratio < 1:
#         newsize = ( xz_arr.shape[1], int(xz_arr.shape[0]/aspect_ratio))
#         xz_img = xz_img.resize(newsize) 
#     else:
#         newsize = (int(xz_arr.shape[1]*aspect_ratio), xz_arr.shape[0],) 
#         xz_img = xz_img.resize(newsize) 
#     # print ('xz_img', newsize)
#     xz_imagePath = './static/images/%s/xz_%s.png'%(patientIndex,y_val)
#     xz_img.save(xz_imagePath)
#     return jsonify(
#     xz_result = url_for('static',
#         filename='images/%s/xz_%s.png'%(patientIndex,y_val))
#     )

# @app.route('/_get_yz_image')
# def get_yz_slice():
#     x_val = request.args.get('x_val', 0, type=int)
#     yz_arr = ct_array_hu[:,:,x_val]
#     yz_arr_min, yz_arr_max = np.min(yz_arr), np.max(yz_arr)
#     yz_arr = 255*(yz_arr-yz_arr_min)/(yz_arr_max-yz_arr_min)
#     yz_img = Image.fromarray(yz_arr.astype('uint8'))
#     yz_img = ImageOps.flip(yz_img)
#     # yz_img = ImageOps.mirror(yz_img)
#     aspect_ratio = ct_spacing[1]/ct_spacing[2]
#     if aspect_ratio < 1:
#         newsize = (yz_arr.shape[1], int(yz_arr.shape[0]/aspect_ratio))
#         yz_img = yz_img.resize(newsize) 
#     else:
#         newsize = (int(yz_arr.shape[1]*aspect_ratio), yz_arr.shape[0]) 
#         yz_img = yz_img.resize(newsize) 
#     yz_imagePath = './static/images/%s/yz_%s.png'%(patientIndex,x_val)
#     yz_img.save(yz_imagePath)
#     return jsonify(
#     yz_result = url_for('static',
#         filename='images/%s/yz_%s.png'%(patientIndex,x_val))
#     )


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host=SERVER_IP, port=SERVER_PORT)
    