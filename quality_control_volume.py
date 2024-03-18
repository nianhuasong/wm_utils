import os
import matplotlib.pyplot as plt
import nibabel
import numpy as np
from PIL import Image


def get_slicer_from_nii(input_path, output_path):
    sub_files = os.listdir(input_path)
    input_file = None
    for sub_file in sub_files:
        # if sub_file.endswith('.nrrd'):
        #     input_file = os.path.join(input_path, sub_file)
        #     break
        # elif sub_file.endswith('.nhdr'):
        #     input_file = os.path.join(input_path, sub_file)
        if sub_file.endswith('.nii.gz'):
            input_file = os.path.join(input_path, sub_file)
    if input_file is None:
        ValueError('Error: Can nott find .nrrd or .nhdr')

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

    # use Image to cat all images
    widths = []
    heights = []
    for i in range(0, len(final_image_list)):
        heights.append(final_image_list[i].shape[0])
        widths.append(final_image_list[i].shape[1])

    new_width = np.sum(widths)
    new_height = np.max(heights)

    new_image = Image.new('L', (new_width, new_height))

    for i in range(0, len(final_image_list)):
        temp_width = int(np.sum(widths[:i]))
        new_image.paste(Image.fromarray(final_image_list[i]), (temp_width, 0))
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

    # test_image = final_image_list[4]
    # test_image = Image.fromarray(test_image)
    # test_image.save(os.path.join(output_path, input_file.split('/')[-1] + 'test.png'))


output_path = '/data05/weizhang_projects/ASD_301_preprocessing/qc'
os.makedirs(output_path, exist_ok=True)
input_path = '/data04/ASD_301_preprocessing/ASDN/sub-15001/ses-1/dwi/'
get_slicer_from_nii(input_path, output_path)

# import nibabel
# import os
# from PIL import Image
# import numpy as np
#
# file_list = os.listdir("./")
#
# for file in file_list:
#     if file[-2:] == "gz":
#         data = nibabel.load(file)
#         data = data.get_fdata()
#         print("data's shape:", data.shape)
#
#         final_image_list = []
#
#         for i in range(0, 3):
#             image_arr = data[:, :, int(data.shape[2] / 6 * (i + 2))] * 255
#             image_arr = image_arr.astype(np.uint8)
#
#             image_arr = image_arr.T
#             image_arr = np.flip(image_arr, axis=1)
#             # final_image = Image.fromarray(image_arr)
#             # final_image.save("./check_image/" + file[:10] + str(i) + "1.png")
#
#             final_image_list.append(image_arr)
#
#         for i in range(0, 3):
#             image_arr = data[:, int(data.shape[1] / 6 * (i + 2)), :] * 255
#             image_arr = image_arr.astype(np.uint8)
#
#             image_arr = image_arr.T
#             image_arr = np.flip(image_arr, axis=0)
#             temp_arr = np.zeros((int(128 - data.shape[2]), 128))
#             temp_arr = temp_arr.astype(np.uint8)
#             image_arr = np.concatenate((image_arr, temp_arr), axis=0)
#             # final_image = Image.fromarray(image_arr)
#             # final_image.save("./check_image/" + file[:10] + str(i) + "1.png")
#
#             final_image_list.append(image_arr)
#
#         for i in range(0, 3):
#             image_arr = data[int(data.shape[0] / 6 * (i + 2)), :, :] * 255
#             image_arr = image_arr.astype(np.uint8)
#
#             image_arr = image_arr.T
#             image_arr = np.flip(image_arr, axis=0)
#             temp_arr = np.zeros((int(128 - data.shape[2]), 128))
#             temp_arr = temp_arr.astype(np.uint8)
#             image_arr = np.concatenate((image_arr, temp_arr), axis=0)
#             # final_image = Image.fromarray(image_arr)
#             # final_image.save("./check_image/" + file[:10] + str(i) + "1.png")
#
#             final_image_list.append(image_arr)
#
#         final_image_arr = final_image_list[0]
#         for i in range(1, len(final_image_list)):
#             print(final_image_list[i].shape)
#             final_image_arr = np.concatenate(
#                 (final_image_arr, final_image_list[i]), axis=1
#             )
#
#         print("max:", final_image_arr.max())
#         print("min:", final_image_arr.min())
#         final_image = Image.fromarray(final_image_arr)
#         final_image = final_image.resize(
#             (final_image.size[0] * 3, final_image.size[1] * 3)
#         )
#         final_image.save("./check_image/" + file[:10] + ".png")
#
#         # break
