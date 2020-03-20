#pydicom
import os
import pydicom
# from pydicom.filereader import read_dicomdir
import numpy as np
import scipy
# import cv2
import csv
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt




def get_rt_structure(RT_struct_path):
    files = [os.path.join(RT_struct_path, f) for f in os.listdir(RT_struct_path)]
    if len(files) == 1:
        RT_struct_file = files[0]
    else:
        print('Error')
    ds = pydicom.read_file(RT_struct_file)
    print(ds.Modality)
    print (dir(ds))
    print("----------------------------------")
    dose_refs = []
    dose_ref = ds.StructureSetROISequence
    print(dir(dose_ref[0]))
    print(dose_ref[0].ROIName)
    for dose in dose_ref:
        # print dose.dir()
        if 'DoseReferencePointCoordinates' in dose.dir():
            dose_refs.append(dose.ROIName)
    # print '------>', dose_refs
    return dose_refs

def convert_dose(RT_dose_path):
    files = [os.path.join(RT_dose_path, f) for f in os.listdir(RT_dose_path)]
    if len(files) == 1:
        RT_dose_file = files[0]
    else:
        print('Error')
    ds = pydicom.read_file(RT_dose_file)
    # print ds.dir()
    dose_pixel = ds.pixel_array
    # print len(ds.PixelData)
    # print dose_pixel.shape

    rows = ds.Rows
    columns = ds.Columns
    pixel_spacing = ds.PixelSpacing
    image_position = ds.ImagePositionPatient
    # print 'DS', image_position
    x = np.arange(columns)*pixel_spacing[0] + image_position[0]
    y = np.arange(rows)*pixel_spacing[1] + image_position[1]
    z = np.array(ds.GridFrameOffsetVector) + image_position[2]
    beam_center = (np.argmin(abs(x)),np.argmin(abs(y)),np.argmin(abs(z)))
    return dose_pixel, x,y,z, pixel_spacing

def get_cts(CT_files_path):
    CT_files = [os.path.join(CT_files_path, f) for f in os.listdir(CT_files_path)]
    slices = {}
    for ct_file in CT_files:
        ds = pydicom.read_file(ct_file)

        # Check to see if it is an image file.
        # print ds.SOPClassUID
        if ds.SOPClassUID == '1.2.840.10008.5.1.4.1.1.2':
            #
            # Add the image to the slices dictionary based on its z coordinate position.
            #
            slices[ds.ImagePositionPatient[2]] = ds.pixel_array
        else:
            pass

    # The ImagePositionPatient tag gives you the x,y,z coordinates of the center of
    # the first pixel. The slices are randomly accessed so we don't know which one
    # we have after looping through the CT slice so we will set the z position after
    # sorting the z coordinates below.
    image_position = ds.ImagePositionPatient
    # print 'CT', image_position
    # Construct the z coordinate array from the image index.
    z = slices.keys()
    z = sorted(z)
    ct_z = np.array(z)

    image_position[2] = ct_z[0]

    # The pixel spacing or planar resolution in the x and y directions.
    ct_pixel_spacing = ds.PixelSpacing

    # Verify z dimension spacing
    b = ct_z[1:] - ct_z[0:-1]
    # z_spacing = 2.5 # Typical spacing for our institution
    if b.min() == b.max():
         z_spacing = b.max()
    else:
        print ('Error z spacing in not uniform')
        z_spacing = 0

    # print z_spacing

    # Append z spacing so you have x,y,z spacing for the array.
    ct_pixel_spacing.append(z_spacing)

    # Build the z ordered 3D CT dataset array.
    ct_array = np.array([slices[i] for i in z])

    print(ct_array.shape)    
    # plt.imshow(ct_array[50,:,:], origin='lower')
    plt.imshow(ct_array[:,255,:], origin='lower')
    # plt.imshow(ct_array[:,:,255], origin='lower')
    plt.show()
    # Now construct the coordinate arrays
    # print ct_pixel_spacing, image_position
    x = np.arange(ct_array.shape[2])*ct_pixel_spacing[0] + image_position[0]
    y = np.arange(ct_array.shape[1])*ct_pixel_spacing[1] + image_position[1]
    z = np.arange(ct_array.shape[0])*z_spacing + image_position[2]
    # print x
    # print image_position[0], image_position[1], image_position[2]
    # print ct_pixel_spacing[0], ct_pixel_spacing[1], ct_pixel_spacing[2]
    # print x, y
    # print (len(x), len(y))
    # # The coordinate of the first pixel in the numpy array for the ct is then  (x[0], y[0], z[0])
    return ct_array, x,y,z, ct_pixel_spacing

def main():
    RT_dose_path = './SAMPLE_DICOM/RTdose'
    RT_struct_path = './SAMPLE_DICOM/RTstruct'
    CT_files_path = './SAMPLE_DICOM/CT/'
    get_cts(CT_files_path)
    # print(convert_dose(RT_dose_path))
    # get_rt_structure(RT_struct_path)
if __name__ == "__main__":
    main()