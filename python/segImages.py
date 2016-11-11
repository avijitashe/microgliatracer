from skimage import segmentation
from skimage.measure import label
from skimage import img_as_uint
from skimage.color import label2rgb
from skimage.segmentation import clear_border
import numpy as np 


def imgsegment(imdata, xx, zz):
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph

	slcs = segmentation.slic(imdata, spacing=[zz, xx, xx], sigma=0, multichannel=False, max_iter=5, n_segments=int(0.1*npx))
	print type(slcs), slcs.shape

	return slcs



#def imglabel(imdata):




#def imgboundary(imdata):




def imgsurface(imdata, xx, zz):
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph


def imglabelobj(imdata, bin_imdata):
	#imdata is the 3D image in ndarray
	#bin_imdata is the binarized thresholded rescaled intensity 3D ndarray of imdata
	nzx=imdata.shape[0]
	nph=imdata.shape[1]
	npw=imdata.shape[2]
	npx=npw*nph
	clr_imdata=bin_imdata #making a non-shallow copy

	for i in range(nzx):
		clr_imdata[i] = clear_border(bin_imdata[i])

	label_img, nums = label(clr_imdata, return_num=True)
	borders = np.logical_xor(bin_imdata, clr_imdata)
	label_img[borders] = -1
	print label_img.shape, imdata.shape
	#image_label_overlay = label2rgb(label_img, image=imdata)
	

	return label_img, nums
