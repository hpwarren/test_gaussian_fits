
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import scipy.special as sc
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

def fit_gaussian_profile_p(wave, profile):
    """
    Use curve_fit to fit the Gaussian to the data
    """

    def ln_likelihood(p):
        model = gaussian_funct(wave, *p)
        l = -profile*np.log(model[g]) + model + sc.gammaln(profile+1)
        return np.sum(l)

    bounds = []
    for n in range(3): bounds.append((0,None))
    bounds[2] = (0.05,None)

    try:
        p0 = guess_param(wave, profile)
        res = minimize(ln_likelihood, p0, method='L-BFGS-B', bounds=bounds)
        p = np.array(res.x)
        perr = np.zeros(p.shape)
        error = np.sqrt(profile)
        model = gaussian_funct(wave,  *p)
        converged = True
        # compute the total counts implied by the fit
        dwave = wave[1]-wave[0]
        ints = p[0]*(p[2]/dwave)*np.sqrt(2*np.pi)
        p = np.append(p, ints)
        # sum the counts in the profile
        total = np.sum(profile)
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

    
