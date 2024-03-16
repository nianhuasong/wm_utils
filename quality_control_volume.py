import os
import matplotlib

import nibabel
import numpy as np


def get_slicer_from_nii(input_path, output_path):
    sub_files = os.listdir(input_path)
    input_file = None
    for sub_file in sub_files:
        if sub_file.endswith('.nrrd'):
            input_file = os.path.join(input_path, sub_file)
            break
        elif sub_file.endswith('.nhdr'):
            input_file = os.path.join(input_path, sub_file)
    if input_file == None:
        ValueError('Error: Can nott find .nrrd or .nhdr')


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
