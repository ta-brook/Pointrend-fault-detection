from skimage.color import rgb2gray
from skimage.transform import resize
from scipy.ndimage import gaussian_filter
import numpy as np
from scipy import signal
import cv2

def scaling_velocity(y, lowest_value, highest_value):
	y = (y - y.min()) / (y.max() - y.min())
	return y * (highest_value - lowest_value) + lowest_value

def convert2velocity(img, nx, nz, filter_sigma):
	img    = rgb2gray(img)
	model  = scaling_velocity(img, 2.0, 4.5)
	model  = resize(model, (nx, nz), anti_aliasing=True)
	smooth = gaussian_filter(model, sigma=filter_sigma)
	return model, smooth

def ricker(frequency, length=0.128, dt=0.004): # bug here exaggerate frequency
	# http://subsurfwiki.org/wiki/Ricker_wavelet   	
	time = np.arange(-length/2, (length-dt)/2, dt)
	wiggle = (1.0 - 2.0*(np.pi**2)*(frequency**2)*(time**2)) * np.exp(-(np.pi**2)*(frequency**2)*(time**2))
	return wiggle

def clip(model, perc):
	(ROWs, COLs) = model.shape
	reshape2D_1D = model.reshape(ROWs*COLs)
	reshape2D_1D = np.sort(reshape2D_1D)
	if perc != 100:
		min_num = reshape2D_1D[ round(ROWs*COLs*(1-perc/100)) ]
		max_num = reshape2D_1D[ round((ROWs*COLs*perc)/100) ]
	elif perc == 100:
		min_num = min(model.flatten())
		max_num = max(model.flatten())
	if min_num > max_num:
		dummy = max_num
		max_num = min_num
		min_num = dummy
	return max_num, min_num 

def reflectivity(vp, frequency):
	wiggle = ricker(frequency)
	(ROWs, COLs) = vp.shape
	reflectivity = np.zeros_like(vp, dtype='float')
	conv = np.zeros_like(vp, dtype='float')
	rho = 2700
	for col in range (0, COLs):
		for row in range (0, ROWs-1):
			reflectivity[row, col] = (vp[row+1, col]*rho - vp[row, col]*rho) / (vp[row+1, col]*rho + vp[row, col]*rho)
		# flip polarity
		conv[:, col] = signal.convolve((reflectivity[:, col]*-1), wiggle, mode='same') / sum(wiggle)
	laplacian = cv2.Laplacian(conv, cv2.CV_64F)
	return laplacian