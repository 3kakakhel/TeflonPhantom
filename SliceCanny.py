"""
This script is an attempt to implement my matlab averaging script but using
python. I also try to be more slick by using actual image processing methods
rather than something I cobbled together.

Author:  Ali Kakakhel (alikakakhel@yahoo.com)
License: BSD 3-Clause License
"""

import dicom, numpy, scipy, scipy.ndimage, scipy.signal, skimage.filter
import matplotlib.pyplot, pylab


# Read in a slice of the phantom.
SlicePath = 'Scan 2/CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.63.dcm'
SliceProfile = dicom.read_file(SlicePath)
print 'File opened for analysis: ' + SlicePath

# Grab the pixel array for the phantom slice. Data is given as uint16 
# integers giving the dose in units of 10^-5 Gy.
SliceArray = SliceProfile.pixel_array
print SliceArray.dtype

# Show the slice. This is the "before" image.
pylab.imshow(SliceArray, cmap=pylab.cm.gray)
pylab.show()

# Apply a Canny filter. Data is given as bools.
SliceFiltered = skimage.filter.canny(SliceArray, sigma=3.0,
                                     low_threshold=4, high_threshold=400)
print SliceFiltered.dtype

### Show a horizontal cros-section through the phantom.
##matplotlib.pyplot.plot(range(1,513), SliceFiltered[275,:], "b-")
##matplotlib.pyplot.xlim([0,512])
##matplotlib.pyplot.show()

# Show the slice again. This is the "after" image.
pylab.imshow(SliceFiltered, cmap=pylab.cm.gray)
print SliceFiltered.dtype
pylab.show()
Rows, Cols = SliceFiltered.shape

# Fix issue with multiple neighboring pixels for the same edge.
SliceFixed = SliceFiltered
for row in range(Rows-1):
    for col in range(Cols-1):
        if SliceFiltered[row,col] & SliceFiltered[row,col+1]:
            SliceFixed[row,col]=False
##        elif SliceFiltered[row,col] & SliceFiltered[row+1,col]:
##            SliceFixed[row,col]=False

# Show the slice again. This is the "fixed" image.
pylab.imshow(SliceFixed, cmap=pylab.cm.gray)
print SliceFixed.dtype
pylab.show()

# Determine which pixels are inside the phantom and which are outside.
SliceMask = numpy.zeros(SliceFiltered.shape, dtype=int)
for row in range(Rows-1):
    for col in range(Cols-1):
        h_sum_l = sum(SliceFixed[row, 0:col])
        h_sum_r = sum(SliceFixed[row, col:Cols])
        v_sum_u = sum(SliceFixed[0:row, col])
        v_sum_b = sum(SliceFixed[row:Rows, col])

        isBorder = SliceFiltered[row-1, col-1] + SliceFiltered[row-1, col] + SliceFiltered[row-1, col+1] + \
                   SliceFiltered[row,   col-1] +                             SliceFiltered[row,   col+1] + \
                   SliceFiltered[row+1, col-1] + SliceFiltered[row+1, col] + SliceFiltered[row+1, col+1]

        isBorder = True if isBorder > 0 else False

        isInside = (((h_sum_l % 2) == 1) & ((h_sum_r % 2) == 1))

        SliceMask[row,col] = 1 if isInside else 0
    print 'row: ', row, '    =', 100.0*row/Rows, '%'

# Show the slice again. This is the "masked" image.
pylab.imshow(SliceMask, cmap=pylab.cm.gray)
print SliceMask.dtype
pylab.show()

