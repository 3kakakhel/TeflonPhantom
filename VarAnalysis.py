# This script compares the local variance to mean ratios between the images.

# Import various libraries.
import numpy, scipy, scipy.ndimage, scipy.signal, scipy.stats
import dicom
import matplotlib.pyplot, pylab

def savitzky_golay(y, window_size, order, deriv=0):
    try:
        window_size = numpy.abs(numpy.int(window_size))
        order = numpy.abs(numpy.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = numpy.mat([[k**i for i in order_range] for k in range(-half_window, \
	  	                                               half_window+1)])
    m = numpy.linalg.pinv(b).A[deriv]
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - numpy.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + numpy.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = numpy.concatenate((firstvals, y, lastvals))
    return numpy.convolve( m, y, mode='valid')


# Read in the dose profiles using the Cheese and Teflon Phantoms, respectively.
#CheesePath = "Alford,Louis_800013095/Ali_LA_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Alford,Louis_800013095/Ali_LA_RA_Teflon_TPS.dcm"
#CheesePath = "Charles,John_366241460/Ali_JC_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Charles,John_366241460/Ali_JC_RA_Teflon_TPS.dcm"
#CheesePath = "Davis,Adlai_957042695/Ali_AD_RA_HalfCheese_TPS.dcm" 
#TeflonPath = "Davis,Adlai_957042695/Ali_AD_RA_Teflon_TPS.dcm"
#CheesePath = "Perryman,Deola_957043663/Ali_DP_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Perryman,Deola_957043663/Ali_DP_RA_Teflon_TPS.dcm"
CheesePath = "Sturges,John_20020682/Ali_JS_RA_HalfCheese_TPS.dcm"
TeflonPath = "Sturges,John_20020682/Ali_JS_RA_Teflon_TPS.dcm"
#CheesePath = "Walker,Pauline_957044312/Ali_PW_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Walker,Pauline_957044312/Ali_PW_RA_Teflon_TPS.dcm"
CheeseProfile = dicom.read_file(CheesePath)
TeflonProfile = dicom.read_file(TeflonPath)
print "Files compared are:"
print CheesePath
print TeflonPath
print


# Grab the pixel array data for both phantom profiles. Data is given integers 
# giving the dose in units of 10^-5 Gy.
CheeseArray = CheeseProfile.pixel_array
TeflonArray = TeflonProfile.pixel_array

# Convert to units of cGy and into floats.
CheeseArray = CheeseArray/1000.
TeflonArray = TeflonArray/1000.

# Change zero values by just a small amount
CheeseArray = CheeseArray + 1e-20*(CheeseArray == 0)
TeflonArray = TeflonArray + 1e-20*(TeflonArray == 0)

# Show the dose profiles.
pylab.imshow(CheeseArray, cmap=pylab.cm.gray)
pylab.show()
pylab.imshow(TeflonArray, cmap=pylab.cm.gray)
pylab.show()

# Compute the local variance to mean ratios for both phantom images.
K = scipy.ones((3,3))
CheeseEM2 = scipy.ndimage.convolve(CheeseArray*CheeseArray, K)/9.
CheeseEM  = scipy.ndimage.convolve(CheeseArray, K)/9.
CheeseE2M = CheeseEM*CheeseEM
CheeseVMR = (CheeseEM2-CheeseE2M)/CheeseEM
TeflonEM2 = scipy.ndimage.convolve(TeflonArray*TeflonArray, K)/9.
TeflonEM  = scipy.ndimage.convolve(TeflonArray, K)/9.
TeflonE2M = TeflonEM*TeflonEM
TeflonVMR = (TeflonEM2-TeflonE2M)/TeflonEM

# Show the VMR profiles.
pylab.imshow(CheeseVMR, cmap=pylab.cm.gray)
pylab.show()
pylab.imshow(TeflonVMR, cmap=pylab.cm.gray)
pylab.show()

# Create histograms of the VMRs for the two phantoms.
CheeseThresh = 10
TeflonThresh = 10
CheeseVMRMin = int(CheeseThresh)
TeflonVMRMin = int(TeflonThresh)
CheeseVMRMax = int(CheeseVMR.max()) + 1
TeflonVMRMax = int(TeflonVMR.max()) + 1
CheeseVMRNum = len(range(CheeseVMRMin,CheeseVMRMax))
TeflonVMRNum = len(range(TeflonVMRMin,TeflonVMRMax))
CheeseHist = scipy.ndimage.measurements.histogram(CheeseVMR, \
		                                  CheeseVMRMin, \
		                                  CheeseVMRMax, \
				                  CheeseVMRNum)
TeflonHist = scipy.ndimage.measurements.histogram(TeflonVMR, \
		                                  TeflonVMRMin, \
		                                  TeflonVMRMax, \
				                  TeflonVMRNum)

# De-noise the histogram.  **Look for something better**
#CheeseHist = scipy.ndimage.uniform_filter1d(CheeseHist, 3)
#TeflonHist = scipy.ndimage.uniform_filter1d(TeflonHist, 3)
#CheeseHist = scipy.ndimage.gaussian_filter1d(CheeseHist, 3)
#TeflonHist = scipy.ndimage.gaussian_filter1d(TeflonHist, 3)
#CheeseHist = savitzky_golay(CheeseHist, 199, 4)
#TeflonHist = savitzky_golay(TeflonHist, 67, 4)
#CheeseHist = scipy.ndimage.spline_filter1d(CheeseHist)
#TeflonHist = scipy.ndimage.spline_filter1d(TeflonHist)

# Show the resulting histograms. The Cheese phantom's histogram data is plotted
# in red while the Teflon phantom's histogram data is plotted in blue.
matplotlib.pyplot.plot(range(CheeseVMRMin,CheeseVMRMax), CheeseHist, "r-", \
		       label="Cheese")
matplotlib.pyplot.plot(range(TeflonVMRMin,TeflonVMRMax), TeflonHist, "b-", \
		       label="Teflon")
matplotlib.pyplot.xlim([TeflonVMRMin,CheeseVMRMax])
matplotlib.pyplot.ylim([0,25])
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

print CheeseHist.sum(),TeflonHist.sum()



"""
# Show a horizontal cross section of the dose profiles right through the 
# middle before the denoising.
matplotlib.pyplot.plot(range(1,513), CheeseArray[255,:], "ro", \
		       label="Cheese Original")
matplotlib.pyplot.plot(range(1,513), TeflonArray[255,:], "bo", \
		       label="Teflon Original")


# Show a horizontal cross section of the gradient profiles right through the 
# middle after the denoising.
matplotlib.pyplot.plot(range(1,513), CheeseArray[255,:], "r-", \
		       label="Cheese Denoised")
matplotlib.pyplot.plot(range(1,513), TeflonArray[255,:], "b-", \
		       label="Teflon Denoised")
matplotlib.pyplot.xlim([0,512])
matplotlib.pyplot.legend()
matplotlib.pyplot.show()


# Show some cross sections of the gradient profiles.
#   -Through the middle horizontally
#   -Through the middle vertically
#   -Through the high gradient edge at the bottom horizontally
matplotlib.pyplot.plot(range(1,513), CheeseGrad[255,:], "ro", \
		       label="Horizontal")
matplotlib.pyplot.plot(range(1,513), CheeseGrad[:,250], "bo", \
		       label="Vertical")
matplotlib.pyplot.plot(range(1,513), CheeseGrad[301,:], "go", \
		       label="High Grad")
matplotlib.pyplot.xlim([0,512])
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
matplotlib.pyplot.plot(range(1,513), TeflonGrad[255,:], "ro", \
		       label="Horizontal")
matplotlib.pyplot.plot(range(1,513), TeflonGrad[:,250], "bo", \
		       label="Vertical")
matplotlib.pyplot.plot(range(1,513), TeflonGrad[301,:], "go", \
		       label="High Grad")
matplotlib.pyplot.xlim([0,512])
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
"""

#End
