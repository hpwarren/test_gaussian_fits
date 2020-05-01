
from scipy.optimize import curve_fit
import numpy as np

def gaussian_funct(wave, peak, cent, sigma):
    """
    Single Gaussian 
    """
    arg = ((wave-cent)/sigma)**2/2
    return peak*np.exp(-arg) 

def guess_param(wave, profile):
    """
    Guess all fit parameters
    """
    peak = np.max(profile)
    ints = np.sum(profile)
    cent = np.sum(wave*profile)/ints
    sigma = 0.1 # (wave[1]-wave[0])*ints/(peak*np.sqrt(2*np.pi))
    return [peak, cent, sigma]

def fit_gaussian_profile(wave, profile):
    """
    Use curve_fit to fit the Gaussian to the data
    """
    
    # handle problem data . . . what should we really do here?
    #bad, = np.where(profile < 0) # this shouldn't happen
    #profile[bad] = 0
    #error = np.sqrt(profile)
    #bad, = np.where(error <= 0) # this does happen
    #error[bad] = 1

    # only fit non-zero pixels
    error = np.sqrt(profile)    
    g, = np.where(profile > 0)

    try:
        p0 = guess_param(wave, profile)
        p, perr = curve_fit(gaussian_funct, wave[g], profile[g], p0=p0, sigma=error[g])
        model = gaussian_funct(wave,  *p)
        converged = True
        # compute the total counts implied by the fit
        dwave = wave[1]-wave[0]
        ints = p[0]*(p[2]/dwave)*np.sqrt(2*np.pi)
        p = np.append(p, ints)
        # sum the counts in the profile
        total = np.sum(profile[g])
        p = np.append(p, total)
    except:
        # something went wrong, but don't crash
        p = 0
        perr = 0
        model = 0
        converged = False

    output = {
        'p' : p,
        'perr': perr,
        'model': model,
        'error': error,
        'converged': converged,
        }

    return output
