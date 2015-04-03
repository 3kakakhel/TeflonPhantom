# This script is an attempt to implement my matlab averaging script but using
# python. I also try to be more slick by using actual image processing methods
# rather than something I cobble together.


import numpy, scipy, scipy.ndimage, scipy.signal, dicom
import matplotlib.pyplot, pylab
import skimage.filter


# Read in a slice of the phantom.
SlicePath = 'Scan 2/CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.63.dcm'
SliceProfile = dicom.read_file(SlicePath)
print 'File opened for analysis: ' + SlicePath

# Grab the pixel array for the phantom slice. Data is given as 6 digit 
# integers giving the dose in units of 10^-5 Gy.
SliceArray = SliceProfile.pixel_array

# Show the slice. This is the "before" image.
pylab.imshow(SliceArray, cmap=pylab.cm.gray)
pylab.show()

# Reduce the noise in the image by applying a gaussian filter.
SliceFiltered = skimage.filter.gaussian_filter(SliceArray, sigma=3.0)

# Apply a Sobel filter.
SliceFiltered = skimage.filter.sobel(SliceArray)

# Show a horizontal cros-section through the phantom.
matplotlib.pyplot.plot(range(1,513), SliceFiltered[275,:], "b-")
matplotlib.pyplot.xlim([0,512])
matplotlib.pyplot.show()

# Show the slice again. This is the "after" image.
pylab.imshow(SliceFiltered, cmap=pylab.cm.gray)
pylab.show()
