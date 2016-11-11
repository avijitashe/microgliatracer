from skimage.filters.rank import median, otsu
from skimage.morphology import disk
from skimage.filters import gaussian
from skimage import filters
import numpy as np
import skimage
import os


def contrast(imdata):

	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph


	#imdata=imdata.misc(gray=True)
	print 'Min: ', imdata.min()
	print 'Max: ', imdata.max()
	print 'Mean: ', imdata.mean()


	for i in range(nzx):
		for j in range(nph):
			for k in range(npw):
				if imdata[i,j,k]<20:
					imdata[i,j,k]=0
				elif imdata[i,j,k]>220:
					imdata[i,j,k]=255
				else:
					continue

	return imdata

def imgmedian(imdata):
	#find the median and remove salt and pepper noise from the 3D stack

	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph

	for i in range(nzx):
		#iterating over the slices over leadding dimension
		#print imdata[1].shape
		imdata[i] = median(imdata[i], disk(2))
	
	return imdata

def imggaussian(imdata, sig):
	#apply gaussian smoothing to prepare for edge detection
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph

	for i in range(nzx):
		imdata[i]=gaussian(imdata[i], sigma=sig, multichannel=None, mode='nearest')
	
	return imdata




def imgthresholdmin(imdata):
	#apply minimum thresholding above which the pixels are foregoround
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph

	for i in range(nzx):
		thr[i]=filters.threshold_minimum(imdata[i], bias='min', max_iter=10000)

	thr=np.mean(thr)
	imdata = imdata > thr #produces binary image
	return imdata




def imgthreshlocalotsu(imdata):
	#apply minimum thresholding below which the pixels are foregoround
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph
	thr=[]

	for i in range(nzx):
		thr_img = otsu(imdata[i], disk(2))
		imdata[i] = thr_img

	
	return imdata



def imgthreshglobalotsu(imdata, mode):
	#apply minimum thresholding below which the pixels are foregoround
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph
	thr_val=[]
	

	for i in range(nzx):
		thr_val.append(filters.threshold_otsu(imdata[i]))
		#print thr_val


	if mode == 1:
		val = np.mean(thr_val)
	elif mode == 2:
		val = np.max(thr_val)
	else:
		val = 155


	print 'Global thresolding value: ', val

	for i in range(nzx):
		for j in range(nph):
			for k in range(npw):

				if imdata[i,j,k] >= val:
					imdata[i,j,k]=255
				else:
					imdata[i,j,k]=0
				
		
	return imdata