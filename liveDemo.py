# import psycopg2
import os
import pydicom

RT_dose_path = './SAMPLE_DICOM/RTdose'
RT_struct_path = './SAMPLE_DICOM/RTstruct'
CT_files_path = './SAMPLE_DICOM/CT/'


CT_files = [os.path.join(CT_files_path, f) for f in os.listdir(CT_files_path)]
slices = {}
for ct_file in CT_files:
    ds = pydicom.read_file(ct_file)
    # print(ds.SOPClassUID)
    slices[ds.ImagePositionPatient[2]] = ds.pixel_array

image_position = ds.ImagePositionPatient

z = slices.keys()
z = sorted(z)
ct_z = np.array(z)

# print(ds.dir())