#It reads life sciences image formats using python module "tifffile"
#available at anaconda using: conda install tifffile -c conda-forge  

import sys
import os


import numpy as np 
import tifffile as TF
from matplotlib import pyplot as plt, cm


if len(sys.argv) < 1:
	print 'Usage: read_tifffile <imagefile.tif>'
	sys.exit(1)


#used to extract pages in the file
def getfilepages(imagepath):
	#img=imread(imagepath)
	with TF.TiffFile(imagepath) as tif:
		images=tif.asarray()
		for page in tif:
			for tag in page.tags.values():
				t = tag.name, tag.value
				image = page.asarray()
				print type(image), image.shape


def getfile(imagepath):
	with TF.TiffFile(imagepath) as tif:
		imdata=tif.asarray()
		print 'Type: ', type(imdata)
		print 'Format: ', imdata.dtype
		print 'Shape: ', imdata.shape
		print 'Pixels: ', imdata.shape[2]*imdata.shape[1]
		print 'Slices: ', imdata.shape[0]

	return imdata



def imageplot(imdata):
	np=imdata.shape[2]*imdata.shape[1]
	nz=imdata.shape[0]
	#for i in range(np):
	
	for j in range(nz):
		plt.imshow(imdata[j,:,:], cmap=cm.gray)
		#plt.pause(.1)
		plt.show()

def imagesave(imdata, name_str):
	TF.imsave(name_str,imdata)
	print 'Data saved in', name_str



def tiffwriter(imdata, name_str):
	with TF.TiffWriter(name_str) as tif:
		for i in range(imdata.shape[0]):
			tif.save(imdata[i])



#reading the file path and file 
folder='/home/avijit/Desktop/Python/bioformats'

if os.path.exists(folder) and os.path.isdir(folder):
	print 'Folder exists. Proceeding ...'
	imagefile=sys.argv[1]
	imagepath=os.path.join(folder, imagefile)
	if os.path.exists(imagepath):
		#print 'Running getfilepages ...'
		#getfilepages(imagepath)
		print 'Running getfile() ...'
		imdata=getfile(imagepath)
		
		print 'File found successfully.'

		#print 'Plotting image ...'
		#imageplot(imdata)
	else:
		print 'File not found. Quitting!'
		sys.exit(1)
else:
	print 'Folder does not exist. Quitting!'
	sys.exit(1)


############################################################################
import filterImages




print 'Removing Salt-Pepper noise ...'
filt_imdata=filterImages.imgmedian(imdata)
#imageplot(filt_imdata)
#imagesave(filt_imdata, 'filt_single-cell2.tif') #NOT NOW
print 'Filtered image saved successfuly!'



print 'Smooting using Gaussian ...'
#gaus_imdata=filterImages.imggaussian(imdata, 1.5)
#imagesave(gaus_imdata, 'gaus_single-cell2.tif')
print 'Smoothed image saved successfully!'



print 'Thresholding and binarizing foreground ...'
bin_imdata = filterImages.imgthreshglobalotsu(imdata,1)
print 'Type: ', bin_imdata.dtype, ' : ', bin_imdata.shape
#imagesave(bin_imdata, 'bin_single-cell2.tif') #NOT NOW

print 'Binarized image saved successfully!'

"""
print 'Thresholding and binarizing foreground ...'
erd_imdata = filterImages.imgthreshglobalotsu(imdata,2)
print erd_imdata.dtype
imagesave(erd_imdata, 'erd_single-cell2.tif')

print 'Erodeded processes image saved successfully!'




import segImages
print 'Segmenting images ...'
#slcs=segImages.imgsegment(imdata, 1, 1)
#imageplot(slcs)
"""

############################################################################	
import segImages


print 'Labelling disctinct objects ...'
labl_imdata, num_obj = segImages.imglabelobj(imdata, bin_imdata)
print 'Label: ', type(labl_imdata), ' : ', labl_imdata.dtype, ' : ', labl_imdata.shape
print  'Num: ', type(num_obj), ' : ', num_obj
imagesave(labl_imdata, 'labl_single-cell2.tif') 

print 'Labels generated and saved successfully!'
imageplot(labl_imdata)