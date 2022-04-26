import sys
sys.path.append('./Libs') 
import convert as C
#-----------------------------------------------------------------------------------------#
from imageio import imread
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
import glob
import os
#-----------------------------------------------------------------------------------------#

'''
step 1: 
'''
cmap_seis = 'gray_r' 
# packed_images = glob.glob('data/raw/visible_geo/*', recursive=True)
packed_images = glob.glob('data/raw/resized/*', recursive=True)
# packed_images = [images for images in os.listdir('data/raw/outcrop/') if images.endswith('.png')]
save_folder = f'data/raw/seismic/resized/'
print(packed_images)
cmap_pack = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu','RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

for i in packed_images:
	try:
		img = imread(i) / 255
		# print(img)
		# print('-------------------------')
		# print(imread(i))
		# print('-------------------------')
		# print(img.shape)
		w,h,d = img.shape
		print(w,h)
		_, smooth = C.convert2velocity(img, w, h, 4)
		seismic = C.reflectivity(smooth, 30)
		max_num, min_num = C.clip(seismic, 99)
		filename, file_extension = os.path.splitext(i)
		# file_name = os.path.basename(filename).replace('fault', 'seismic') + file_extension
		file_name = os.path.basename(filename).replace('fault', 'seismic') + file_extension
		save_image = os.path.join(save_folder, file_name.replace('JPG', 'png'))
		# for idx, cmap in enumerate(cmap_pack):
		# 	plt.imsave(fname=f'{save_image[:-4]}_{cmap}.png', arr=seismic, cmap=cmap, format='png', vmin=min_num, vmax=max_num)
		plt.imsave(fname=save_image, arr=seismic, cmap=cmap_seis, format='png', vmin=min_num, vmax=max_num)
		print(save_image)

	except:
		print('error {i}')
