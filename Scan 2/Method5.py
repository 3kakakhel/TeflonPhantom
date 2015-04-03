# This script is to use python and scipy to perform the smoothing analysis I did
# on the teflon phantom scans.

# Import various libraries.
import numpy, scipy, scipy.ndimage, scipy.optimize, scipy.stats, dicom
import matplotlib.pyplot, pylab

# Read in the slice.
SliceNum = 63
SlicePath = 'CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.' + \
            str(SliceNum) + '.dcm'
print SlicePath
SliceProfile = dicom.read_file(SlicePath)

# Grab the pixel array data for the slice. 
SliceArray = SliceProfile.pixel_array

# Display some sample pixel data.
#print SliceProfile
#print SliceArray[256,128]

# Show the slice profiles.
#pylab.imshow(SliceArray, cmap=pylab.cm.gray)
#pylab.show()

# Show a horizontal cross section of the slice profiles right through the 
# middle.
matplotlib.pyplot.plot(range(0,512), SliceArray[:,255], "r-")
#matplotlib.pyplot.xlim([0,512])
matplotlib.pyplot.show()

# Plot the slice in 3D.


# Create a histogram of the doses
SliceThresh = 1
SliceArrayMin = int(SliceThresh)
SliceArrayMax = int(SliceArray.max()) + 1
SliceArrayNum = len(range(SliceArrayMin, SliceArrayMax))
SliceHist = scipy.ndimage.measurements.histogram(SliceArray, \
		                                 SliceArrayMin, \
		                                 SliceArrayMax, \
				                 SliceArrayNum)

# Fit the peak representing teflon to a gaussian.
PixelValues = range(1522,2306)
def gauss(x, *p):
    A, mu, sigma = p
    return A*scipy.exp(-(x-mu)**2/(2.*sigma**2))

p0 = [700, 1914, 173] # Initial guess for the parameters
coeff, var_matrix = scipy.optimize.curve_fit(gauss, \
                                             PixelValues, \
                                             SliceHist[1522:], \
                                             p0=p0)
# Get the fitted gaussian.
hist_fit = gauss(PixelValues, *coeff)
print 'Fitted Mu    = ', coeff[1]
print 'Fitted Sigma = ', coeff[2]

# Plot the resulting histogram and fit function.
matplotlib.pyplot.plot(range(SliceArrayMin, SliceArrayMax), SliceHist, "b-")
matplotlib.pyplot.plot(PixelValues, hist_fit, "g-")
matplotlib.pyplot.xlim([1522,SliceArrayMax])
#matplotlib.pyplot.ylim([0,25])
matplotlib.pyplot.show()


#END
