# This script is an attempt to implement my matlab averaging script but using
# python. I also try to be more slick by using actual image processing methods
# rather than something I cobble together.


import numpy, scipy, scipy.ndimage, scipy.signal, dicom
import matplotlib.pyplot, pylab
import skimage.filter, skimage.util


# Read in a slice of the phantom.
SlicePath = 'Scan 2/CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.63.dcm'
SliceProfile = dicom.read_file(SlicePath)
print 'File opened for analysis: ' + SlicePath

# Grab the pixel array for the phantom slice. Data is given as 6 digit 
# integers giving the dose in units of 10^-5 Gy.
SliceArray = SliceProfile.pixel_array
print "Original Slice Image dtype: " + str(SliceArray.dtype)

### Show the slice. This is the "before" image.
##pylab.imshow(SliceArray, cmap=pylab.cm.gray)
##pylab.show()

# Show a histogram of the slice / "before" image.
SliceMin = 0   
SliceMax = 3000
SliceNum = len(range(SliceMin,SliceMax))
SliceHist = scipy.ndimage.measurements.histogram(SliceArray, \
		                                 SliceMin, \
		                                 SliceMax, \
				                 SliceNum)
matplotlib.pyplot.plot(range(SliceMin,SliceMax), SliceHist)
matplotlib.pyplot.xlim([0,3000])
matplotlib.pyplot.ylim([0,1000])
matplotlib.pyplot.show()

# Reduce the noise in the image by applying a gaussian filter.
SliceFiltered = skimage.filter.gaussian_filter(SliceArray, sigma=3.0)
print "Smoothed Slice Image dtype: " + str(SliceFiltered.dtype)
SliceFiltered = skimage.util.img_as_uint(SliceFiltered)
print "Smoothed Slice Image dtype: " + str(SliceFiltered.dtype)


# Show the slice. This is the "after" image.
pylab.imshow(SliceFiltered, cmap=pylab.cm.gray)
pylab.show()

# Show a histogram of the slice / "after" image.
SliceMin = 0   
SliceMax = 3000
SliceNum = SliceMax-SliceMin
SliceHist = scipy.ndimage.measurements.histogram(SliceFiltered, \
		                                 SliceMin, \
		                                 SliceMax, \
				                 SliceNum)
matplotlib.pyplot.plot(range(SliceMin,SliceMax), SliceHist)
matplotlib.pyplot.xlim([0,3000])
matplotlib.pyplot.ylim([0,2000])
matplotlib.pyplot.show()

# Apply a Sobel filter.
SliceFiltered = skimage.filter.sobel(SliceArray)
print "Sobel'ed Slice Image dtype: " + str(SliceArray.dtype)

### Show a horizontal cros-section through the phantom.
##matplotlib.pyplot.plot(range(1,513), SliceFiltered[275,:])
##matplotlib.pyplot.xlim([0,512])
##matplotlib.pyplot.show()

### Show a histogram of the filtered slice.
##SliceMin = 0   
##SliceMax = 3000
##SliceNum = len(range(SliceMin,SliceMax))
##SliceHist = scipy.ndimage.measurements.histogram(SliceFiltered, \
##		                                 SliceMin, \
##		                                 SliceMax, \
##				                 SliceNum)
##matplotlib.pyplot.plot(range(SliceMin,SliceMax), SliceHist)
##matplotlib.pyplot.ylim([min(SliceHist),max(SliceHist)])
##matplotlib.pyplot.show()


### Show the slice again. This is the "after" image.
##pylab.imshow(SliceFiltered, cmap=pylab.cm.gray)
##pylab.show()
