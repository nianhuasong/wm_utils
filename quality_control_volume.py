import os
import matplotlib.pyplot as plt
import nibabel
import numpy as np
from PIL import Image
from tqdm import tqdm


def get_slicer_from_nii(input_path, output_path):
    sub_files = os.listdir(input_path)
    input_file = None
    for sub_file in sub_files:
        # if sub_file.endswith('.nrrd'):
        #     input_file = os.path.join(input_path, sub_file)
        #     break
        # elif sub_file.endswith('.nhdr'):
        #     input_file = os.path.join(input_path, sub_file)
        if sub_file.endswith('dwi.nii.gz') or sub_file.endswith('dwi.nii'):
            input_file = os.path.join(input_path, sub_file)
    if input_file is None:
        print(input_path)
        return

    # load nii
    volume_data = nibabel.load(input_file).get_fdata()[:, :, :, 0]

    final_image_list = []
    # get index range volume_data.max-volume_data.min
    volume_data_range = np.max(volume_data) - np.min(volume_data)
    # get 3 images from axis=0
    for i in range(0, 3):
        image_arr = volume_data[:, :, int(volume_data.shape[2] / 6 * (i + 2))] / volume_data_range * 255
        image_arr = image_arr.astype(np.uint8)
        image_arr = image_arr.T
        image_arr = np.flip(image_arr, axis=1)

        final_image_list.append(image_arr)

    # get 3 image from axis=1
    for i in range(0, 3):
        image_arr = volume_data[:, int(volume_data.shape[1] / 6 * (i + 2)), :] / volume_data_range * 255
        image_arr = image_arr.astype(np.uint8)
        image_arr = image_arr.T
        image_arr = np.flip(image_arr, axis=0)

        final_image_list.append(image_arr)

    # get 3 image from axis=2
    for i in range(3):
        image_arr = volume_data[int(volume_data.shape[0] / 6 * (i + 2)), :, :] / volume_data_range * 255
        image_arr = image_arr.astype(np.uint8)
        image_arr = image_arr.T
        image_arr = np.flip(image_arr, axis=0)

        final_image_list.append(image_arr)

    # resize all images

    # use Image to cat all images
    # resize, get width height
    widths = []
    heights = []
    for i in range(0, len(final_image_list)):
        temp_height = final_image_list[i].shape[0] * 2
        temp_width = final_image_list[i].shape[1] * 2
        final_image_list[i] = Image.fromarray(final_image_list[i]).resize((temp_width, temp_height))
        heights.append(temp_height)
        widths.append(temp_width)

    # get final_big_image's size
    new_width = np.sum(widths)
    new_height = np.max(heights)

    new_image = Image.new('L', (new_width, new_height))

    for i in range(0, len(final_image_list)):
        temp_width = int(np.sum(widths[:i]))
        new_image.paste(final_image_list[i], (temp_width, 0))
    new_image.save(os.path.join(output_path, input_file.split('/')[-1] + '.png'))

    # # plot in matplot
    # fig, axes = plt.subplots(nrows=1, ncols=9, )
    #
    # for i in range(len(final_image_list)):
    #     axes[i].imshow(final_image_list[i], cmap='gray')
    #     axes[i].axis('off')
    #
    # fig.suptitle(input_file.split('/')[-1])
    # fig.tight_layout()
    # fig.savefig(os.path.join(output_path, input_file.split('/')[-1]) + '.png')

    # # for test
    # test_image = final_image_list[4]
    # test_image = Image.fromarray(test_image)
    # test_image.save(os.path.join(output_path, input_file.split('/')[-1] + 'test.png'))


output_path = '/data05/weizhang_projects/ASD_301_preprocessing/qc/image_output_final_nii'
os.makedirs(output_path, exist_ok=True)
input_roots = ['/data04/ASD_301_final_preprocess/site2_nii']
for input_root in input_roots:
    subjects = os.listdir(input_root)
    for i in tqdm(range(len(subjects))):
        input_path = os.path.join(input_root, subjects[i], 'ses-1/dwi/')
        get_slicer_from_nii(input_path, output_path)
