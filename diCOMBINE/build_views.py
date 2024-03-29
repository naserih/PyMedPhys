
import os
import io
import numpy as np
from dicom_utils import get_cts
from PIL import Image, ImageEnhance, ImageOps
import env
import json
import shutil

ROOT = ['TEST','MET', 'CTRL'][0]
# aria_database = env.ARIA_DATABASE[ROOT]
download_path = env.DOWNLOAD_DATABASE
patient_file_path = env.PATIENTS_DATABASE[ROOT]

def transfer_files():
    CT_tag = ''
    if not os.path.exists(patient_file_path):
        os.makedirs(patient_file_path)

    transfered_patients = os.listdir(patient_file_path)
    downloaded_patients = os.listdir(download_path)

    N = len(downloaded_patients)
    n = 0
    for patient_file in downloaded_patients:
        n +=  1 
        print ("%s: %s/%s"%(patient_file,n,N))
        if patient_file  in transfered_patients:
            shutil.rmtree(os.path.join(patient_file_path, patient_file)) 
        os.makedirs(os.path.join(patient_file_path, patient_file))
        os.makedirs(os.path.join(patient_file_path, patient_file, 'XY'))
        ct_files = [f  for f in os.listdir(os.path.join(download_path,patient_file)) if CT_tag in f]
        for f in ct_files:
            src = os.path.join(download_path,patient_file, f)
            dist = os.path.join(patient_file_path, patient_file, 'XY', f)
            shutil.copyfile(src, dist)

def load_dicoms(patient_file):
    patient_metadata = {}
    if not os.path.exists(os.path.join(patient_file_path, patient_file, 'XY')):
        os.makedirs(os.path.join(patient_file_path, patient_file, 'XY'))
        print ('ERROR: NO CT IMAGES FOR PATIENT %s' %patient_file)

    if os.path.exists(os.path.join(patient_file_path, patient_file, 'XZ')):
        shutil.rmtree(os.path.join(patient_file_path, patient_file, 'XZ'))
    if os.path.exists(os.path.join(patient_file_path, patient_file, 'YZ')):
        shutil.rmtree(os.path.join(patient_file_path, patient_file, 'YZ'))
    
    os.makedirs(os.path.join(patient_file_path, patient_file, 'XZ'))
    os.makedirs(os.path.join(patient_file_path, patient_file, 'YZ'))

    patient_metadata[patient_file] = {}
    ct_file = [os.path.join(patient_file_path, patient_file, 'XY', f) for f in os.listdir(os.path.join(patient_file_path, patient_file, 'XY'))]
    patient_metadata[patient_file]['ct_array'], \
    patient_metadata[patient_file]['ct_array_hu'], \
    patient_metadata[patient_file]['ct_x'], \
    patient_metadata[patient_file]['ct_y'], \
    patient_metadata[patient_file]['ct_z'], \
    patient_metadata[patient_file]['ct_spacing'], \
    patient_metadata[patient_file]['ct_index'] = get_cts(ct_file)

    return patient_metadata

def generate_XZ_YZ_views(patient, patient_metadata):
    ct_array = patient_metadata[patient]['ct_array_hu']
    ct_spacing = patient_metadata[patient]['ct_spacing']
    # print(patient, ct_array.shape, ct_spacing)
    arr_min, arr_max = np.min(ct_array), np.max(ct_array)
    for y_val in range(ct_array.shape[1]):
        xz_arr = ct_array[:,y_val,:]
        xz_arr = 255*(xz_arr-arr_min)/(arr_max-arr_min)
        xz_img = Image.fromarray(xz_arr.astype('uint8'))
        xz_img = ImageOps.flip(xz_img)
        aspect_ratio = ct_spacing[0]/ct_spacing[2]
        if aspect_ratio < 1:
            newsize = ( xz_arr.shape[1], int(xz_arr.shape[0]/aspect_ratio))
            xz_img = xz_img.resize(newsize) 
        else:
            newsize = (int(xz_arr.shape[1]*aspect_ratio), xz_arr.shape[0],) 
            xz_img = xz_img.resize(newsize) 
        xz_imagePath = os.path.join(patient_file_path, patient, 'XZ', '%s.png'%(str(y_val).zfill(4)))
        xz_img.save(xz_imagePath)

    for x_val in range(ct_array.shape[2]):
        yz_arr = ct_array[:,:,x_val]
        yz_arr = 255*(yz_arr-arr_min)/(arr_max-arr_min)
        yz_img = Image.fromarray(yz_arr.astype('uint8'))
        yz_img = ImageOps.flip(yz_img)
        aspect_ratio = ct_spacing[1]/ct_spacing[2]
        if aspect_ratio < 1:
            newsize = ( yz_arr.shape[1], int(yz_arr.shape[0]/aspect_ratio))
            yz_img = yz_img.resize(newsize) 
        else:
            newsize = (int(yz_arr.shape[1]*aspect_ratio), yz_arr.shape[0],) 
            yz_img = yz_img.resize(newsize) 
        yz_imagePath = os.path.join(patient_file_path, patient, 'YZ', '%s.png'%(str(x_val).zfill(4)))
        yz_img.save(yz_imagePath)

def main():
    # print('YES')
    transfer_files()
    patient_filenames = os.listdir(patient_file_path)
    N = len(patient_filenames)
    n = 0
    for patient in patient_filenames:
        patient_metadata = load_dicoms(patient)
        n += 1
        print("%s: %s/%s"%(patient,n,N))
        generate_XZ_YZ_views(patient, patient_metadata)



if __name__ == "__main__":
    main()