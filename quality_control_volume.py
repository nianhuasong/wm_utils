import os 
import matplotlib

import nibabel
import numpy as np

def get_slicer_from_nii(input_path,output_path):
    sub_files=os.listdir(input_path)
    input_file=None
    for sub_file in sub_files:
        if sub_file.endswith('.nrrd'):
            input_file=os.path.join(input_path,sub_file)
            break
        elif sub_file.endswith('.nhdr'):
            input_file=os.path.join(input_path,sub_file)
    if input_file==None:
        ValueError('Error: Can nott find .nrrd or .nhdr')
    
    