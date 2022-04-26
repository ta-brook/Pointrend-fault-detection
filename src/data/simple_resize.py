from PIL import Image
import os
import albumentations as A
import cv2

outcrop_path ='data/raw/visible_geo/'
save_path = 'data/raw/resized/'
size = (512, 512)
H,W = size

# # TODO access to annotation
# outcrop_data_path = [file for file in os.listdir(outcrop_path) if file.endswith('.png')]

# for pic in outcrop_data_path:
#     image = Image.open(outcrop_path + pic)
#     print(image.size)
#     image.resize(size, Image.ANTIALIAS)
#     print(image.size)
#     image.save(save_path + pic)
#     print(save_path+pic)

from PIL import Image
import numpy as np

# transform = A.Compose([A.Resize(height =H,width=W)], keypoint_params=A.KeypointParams(format='xy'))
# pillow_image = Image.open("image.jpg")
# image = np.array(pillow_image)
# transformed = transform(image=image)
# transformed_image = transformed["image"]

outcrop_data_path = [file for file in os.listdir(outcrop_path) if file.endswith(('.png', 'JPG'))]
for pic in outcrop_data_path:
    print('A')
    transform = A.Compose([A.Resize(height =H,width=W)])
    image = cv2.imread(outcrop_path + pic)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    transformed = transform(image = image)
    trans_image = transformed["image"]
    trans_image = cv2.cvtColor(trans_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path + f"{pic.replace('fault_', 'vg_fault_').replace('JPG','png')}",trans_image)
    print(save_path + pic)