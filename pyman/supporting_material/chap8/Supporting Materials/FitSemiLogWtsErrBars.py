# Routine FitSemiLogWtsErrBars
import numpy as np
import matplotlib.pyplot as plt

def LineFitWt(x, y, sig):
    """ 
    Returns slope and y-intercept of weighted linear fit to
    (x,y) data set.
    Inputs: x and y data array and uncertainty array (unc)
            for y data set.
    Outputs: slope and y-intercept of best fit to data and
             uncertainties of slope & y-intercept.
    """
    sig2 = sig**2
    norm = (1./sig2).sum()
    xhat = (x/sig2).sum() / norm
    yhat = (y/sig2).sum() / norm
    slope = ((x-xhat)*y/sig2).sum()/((x-xhat)*x/sig2).sum()
    yint = yhat - slope*xhat
    sig2_slope = 1./((x-xhat)*x/sig2).sum()
    sig2_yint = sig2_slope * (x*x/sig2).sum() / norm
    return slope, yint, np.sqrt(sig2_slope), np.sqrt(sig2_yint)

def redchisq(x, y, dy, slope, yint):
    chisq = (((y-yint-slope*x)/dy)**2).sum()
    return chisq/float(x.size-2)

# Read data from data file
t, V, dV = np.loadtxt("RLcircuit.txt", skiprows=2, unpack=True)

########## Code to tranform & fit data starts here ##########

# Transform data and parameters to linear form: Y = A + A*X
X = t         # transform t data for fitting (not needed as X=t)
Y = np.log(V) # transform N data for fitting
dY = dV/V     # transform uncertainties for fitting

# Fit transformed data X, Y, dY to obtain fitting parameters
# B & A.  Also returns uncertainties dA & dB in B & A
B, A, dB, dA = LineFitWt(X, Y, dY)
# Return reduced chi-squared
redchisqr = redchisq(X, Y, dY, B, A)

# Determine fitting parameters for original exponential function
# N = N0 exp(-Gamma t) ...
V0fit = np.exp(A)
GammaFit = -B
# ... and their uncertainties
dV0fit = V0fit * dA
dGammaFit = dB

###### Code to plot transformed data and fit starts here ######

# Create line corresponding to fit using fitting parameters
# Only two points are needed to specify a straight line
Xfit = np.array([X.min(), X.max()]) # smallest & largest X points
Yfit = B*Xfit + A                   # generates Y from X data & 
                                    # fitting function
plt.errorbar(X, Y, dY, fmt="b^")
plt.plot(Xfit, Yfit, "c-", zorder=-1)
plt.title(r"$\mathrm{Fit\ to:}\ \ln V = -\Gamma t + \ln V_0$ or $Y = A + BX$")
plt.xlabel('time (ns)')
plt.ylabel('ln voltage (volts)')

plt.text(220, 1.5, u"A = ln V0 = {0:0.4f} \xb1 {1:0.4f}".format(B, dB))
plt.text(220, 1.1, u"B = -Gamma = {0:0.2f} \xb1 {1:0.2f} /ns".format(-A, dA))
plt.text(220, 0.7, "$\chi_r^2$ = {0:0.3f}".format(redchisqr))
plt.text(220, 0.3, u"V0 = {0:0.2f} \xb1 {1:0.2f} V".format(V0fit, dV0fit))
plt.text(220, -0.1,u"GammaFit = {0:0.4f} \xb1 {1:0.4f} /ns".format(GammaFit, dGammaFit))

plt.show()
plt.savefig("FitSemiLogWtsErrBars.pdf")