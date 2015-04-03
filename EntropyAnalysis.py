# -*- coding: utf-8 -*-
# This script compares the entropy of the patient dicom images.

# Import various libraries.
import scipy, scipy.ndimage, scipy.stats
import matplotlib.pyplot, pylab
import dicom


# Read in the dose profiles using the Cheese and Teflon Phantoms, respectively
#CheesePath = "Perryman,Deola_957043663/Ali_DP_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Perryman,Deola_957043663/Ali_DP_RA_Teflon_TPS.dcm"
#CheesePath = "Sturges,John_20020682/Ali_JS_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Sturges,John_20020682/Ali_JS_RA_Teflon_TPS.dcm"
#CheesePath = "Davis,Adlai_957042695/Ali_AD_RA_HalfCheese_TPS.dcm" 
#TeflonPath = "Davis,Adlai_957042695/Ali_AD_RA_Teflon_TPS.dcm"
#CheesePath = "Walker,Pauline_957044312/Ali_PW_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Walker,Pauline_957044312/Ali_PW_RA_Teflon_TPS.dcm"
#CheesePath = "Charles,John_366241460/Ali_JC_RA_HalfCheese_TPS.dcm"
#TeflonPath = "Charles,John_366241460/Ali_JC_RA_Teflon_TPS.dcm"
CheesePath = "Alford,Louis_800013095/Ali_LA_RA_HalfCheese_TPS.dcm"
TeflonPath = "Alford,Louis_800013095/Ali_LA_RA_Teflon_TPS.dcm"
CheeseProfile = dicom.read_file(CheesePath)
TeflonProfile = dicom.read_file(TeflonPath)
print "Files compared:"
print CheesePath
print TeflonPath
print


# Grab the pixel array data for both phantom profiles. Data is given as
# integers...
CheeseArray = CheeseProfile.pixel_array
TeflonArray = TeflonProfile.pixel_array
#CheeseConvF = float(CheeseProfile.DoseGridScaling)
#TeflonConvF = float(TeflonProfile.DoseGridScaling)
#CheeseArray = scipy.uint16(CheeseArray*CheeseConvF*100)
#TeflonArray = scipy.uint16(TeflonArray*TeflonConvF*100)

"""
# Show the dose profiles.
pylab.imshow(CheeseArray, cmap=pylab.cm.gray)
pylab.show()
pylab.imshow(TeflonArray, cmap=pylab.cm.gray)
pylab.show()
"""

# Keep doses greater than x% of the max dose (KeepThresh) and use those in
# calculating the histograms and entropies.
CheeseMax = CheeseArray.max()
TeflonMax = TeflonArray.max()
KeepThresh = 0.9
for r in range(0, 512):
    for c in range(0, 512):
        if CheeseArray[r,c] < CheeseMax*KeepThresh: CheeseArray[r,c] = 0
        if TeflonArray[r,c] < TeflonMax*KeepThresh: TeflonArray[r,c] = 0

# Create histograms of the images for the two phantoms.
CheeseArrayNum = 256
TeflonArrayNum = 256
CheeseHist = scipy.ndimage.measurements.histogram(CheeseArray, \
		                                  0, \
                                                  CheeseArray.max() + 1, \
                                                  CheeseArrayNum)
TeflonHist = scipy.ndimage.measurements.histogram(TeflonArray, \
		                                  0, \
                                                  TeflonArray.max() + 1, \
                                                  TeflonArrayNum)


# Show the resulting histograms. The Cheese phantom's histogram data is plotted
# in red while the Teflon phantom's histogram data is plotted in blue.
#matplotlib.pyplot.plot(range(0, CheeseArrayNum, 1), \
#                      CheeseHist, "r-", label="Cheese")
#matplotlib.pyplot.plot(range(0, TeflonArrayNum, 1), \
#                      TeflonHist, "b-", label="Teflon")
matplotlib.pyplot.step(range(0, CheeseArrayNum, 1), \
                       CheeseHist, where='post', color='r', label='Cheese')
matplotlib.pyplot.step(range(0, TeflonArrayNum, 1), \
                       TeflonHist, where='post', color='b', label='Teflon')
matplotlib.pyplot.xlim([0,255])
matplotlib.pyplot.ylim([0,2048])
matplotlib.pyplot.legend()
matplotlib.pyplot.show()


# Calculate and print out the entropies of the images using both phantoms.
CheeseMin = 10#18
TeflonMin = 10#24
CheeseEntropy = scipy.stats.entropy(CheeseHist[CheeseMin:])
TeflonEntropy = scipy.stats.entropy(TeflonHist[TeflonMin:])
print 'Entropies:'
print CheeseEntropy, TeflonEntropy
print

"""
# Calculate and print out the chi-squared test between both hitograms.
print ' 2'
print 'x  statistic, p-value:'
print scipy.stats.chisquare(TeflonHist[CheeseMin:], \
                            CheeseHist[CheeseMin:])
print

# Output the histogram and trimmed histogram data to a file.
scipy.savetxt('Cheese_256_Hist.txt', CheeseHist.astype(int), '%d')
scipy.savetxt('Teflon_256_Hist.txt', TeflonHist.astype(int), '%d')
scipy.savetxt('Cheese_256_TrimmedHist.txt', \
              CheeseHist[CheeseMin:].astype(int), '%d')
scipy.savetxt('Teflon_256_TrimmedHist.txt', \
              TeflonHist[CheeseMin:].astype(int), '%d')
"""


#End
