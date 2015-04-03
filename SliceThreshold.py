# Use some method to threshold the pixels for in or out of phantom.

# clean up the code and commenting.

import dicom
import numpy, scipy, scipy.ndimage, scipy.ndimage.filters, scipy.optimize, scipy.stats
import matplotlib.pyplot, pylab


# Read in a slice of the phantom.
SlicePath = 'Scan 2/CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.65.dcm'
SliceProfile = dicom.read_file(SlicePath)
print 'File opened for analysis: \n./' + SlicePath

# check if there is a (0028,1054) tag. If not, then I know the dicom file's
# pixel array numbers are to be converted to HU.
try:
    isHU = True if SliceProfile[0x0028,0x1054].value == 'HU' else False
except:
    isHU = True

if isHU:
    # The slope of the line to convert from a raw data value to a HU value.
    CalibrationSlope = SliceProfile.RescaleSlope
    # The intercept of the line to convert from a raw data value to a HU value.
    CalibrationIntercept = SliceProfile.RescaleIntercept

    print
    print 'Calibration Slope     = %9.1f' % (CalibrationSlope)
    print 'Calibration Intercept = %9.1f' % (CalibrationIntercept)
    print
else:
    print 'no calibration from raw pixel data values to HU values.'

# Grab the pixel array for the phantom slice. Data is given as 6 digit integers.
# The relationship between the raw data and HU values is given as follows.
# HU = CalibrationSlope * Raw + CalibrationIntercept
SliceArray = SliceProfile.pixel_array

# Show the slice. This is the original, "before", image.
pylab.imshow(SliceArray, cmap=pylab.cm.gray)
pylab.show()

# Compute a histogram of the slice image and fit it to a sum of gaussians.
# The first peak represents the background.
# The second peak represents the teflon phantom.
hist = scipy.ndimage.measurements.histogram(SliceArray, 1, 3000, 3000)

fitfunc = lambda p,x: p[0]*numpy.exp(-0.5*((x-p[1])/p[2])**2) + \
                      p[3]*numpy.exp(-0.5*((x-p[4])/p[5])**2) + \
                      p[6]
errfunc = lambda p,x,y: (y - fitfunc(p, x))

# Set range of x values.
xdata = range(3000)

# Set y values to fit against.
ydata = hist

# Set initial guesses for the parameters. Guesses come from the catphan manual.
# http://www.phantomlab.com/library/pdf/catphan504manual.pdf
# Air    = -1046 --> -986 (min  --> max) HU
#        = -1016 +/- 60   (mean +/- std) HU
# Teflon =   941 --> 1060 (min  --> max) HU
#        =  1001 +/- 119  (mean +/- std) HU
# The amplitudes of the gaussians are just guessed to be 500.
init = [500,
        CalibrationSlope * (-1016 - CalibrationIntercept),
        60,
        500,
        CalibrationSlope * ( 1001 - CalibrationIntercept),
        119,
        0]

# Perform the fitting and capture the fitted parameter values.
fitted_data   = scipy.optimize.leastsq(errfunc, init, args=(xdata,ydata))
fitted_params = fitted_data[0]

# Print out the fitted parameter values.
print 'peak 1 height   = ', fitted_params[0]
print 'peak 1 location = ', fitted_params[1]
print 'peak 1 std dev  = ', fitted_params[2]
print
print 'peak 2 height   = ', fitted_params[3]
print 'peak 2 location = ', fitted_params[4]
print 'peak 2 std dev  = ', fitted_params[5]
print
print 'background      = ', fitted_params[6]

# Store the fitted histogram.
hist_fitted = fitfunc(fitted_params, xdata)

# Apply a thresholding at four standard deviations below the location of the
# second peak to capture all the teflon phantom pixels.
# Also display the threshold value.
val = fitted_params[4] - 4*fitted_params[5]
print
print 'threshold       = ', val
SliceMasked = SliceArray > val

# Plot the original histogram, fitted histogram, and threshold value.
matplotlib.pyplot.step(xdata, hist)
matplotlib.pyplot.plot(xdata, hist_fitted)
matplotlib.pyplot.axvline(val, linestyle='--', color='#AA0000')
matplotlib.pyplot.show()

# Show the slice again. This is the masked, "after", image.
pylab.imshow(SliceMasked, cmap=pylab.cm.gray)
pylab.show()

# Find the "smoothed" teflon HU value after removing noise and artifacts,
# ie just read of the second peak location.
# The (unconverted) fitted raw data value.
TeflonRaw = fitted_params[4]
# Convert the fitted raw data value for teflon to the corresponding HU value.
TeflonHU  = TeflonRaw * CalibrationSlope + CalibrationIntercept
# Print out the smoothed Teflon HU value.
print
print '>>> Smoothed Teflon HU = ', TeflonHU
