#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from fit_gaussian_profile import fit_gaussian_profile
from fit_gaussian_profile_p import fit_gaussian_profile_p

class sim_gaussian_profile:

    def __init__(self, total_counts=100, wave0=977.02, sigma0=86., dwave=37., nwave=32, \
                 display=False, poisson=False):
        self.sim = {} # store results here
        self.nwave = nwave # number of pixels in wavelength array
        self.dwave = dwave/1000. # dispersion in Angstroms
        self.wave0 = wave0 # centroid in Angstroms
        self.total_counts = total_counts # total counts we want in the profile
        self.sigma0 = sigma0/1000. # Gaussian width in Angstroms
        self.fit_status = False
        self.poisson = poisson

        self.calc_wave()
        self.calc_profile_model()
        self.calc_profile_poisson()
        self.fit_profile()
        if display:
            self.print_fit()
            self.plot_fit()

    def calc_wave(self):
        """
        Calculate the wavelength array, in Angstroms
        """
        wave = self.wave0 + self.dwave*(np.arange(0, self.nwave) - self.nwave/2)
        self.sim['wave'] = wave

    def calc_profile_model(self):
        """
        This is the model profile, in counts per pixel
        """
        wave = self.sim['wave']
        peak = self.total_counts/(self.sigma0*np.sqrt(2*np.pi))
        arg = ((wave-self.wave0)/self.sigma0)**2/2.0
        profile = self.dwave*peak*np.exp(-arg)
        profile = np.round(profile).astype('int')
        self.sim['model'] = profile

    def calc_profile_poisson(self):
        """
        Create a noisy realization of the profile
        """
        self.sim['poisson'] = np.random.poisson(self.sim['model'])

    def fit_profile(self):
        if self.poisson:
            self.sim['fit_poisson'] = fit_gaussian_profile_p(self.sim['wave'], self.sim['poisson'])
        else:
            self.sim['fit_poisson'] = fit_gaussian_profile(self.sim['wave'], self.sim['poisson'])
        self.fit_status = self.sim['fit_poisson']['converged']

    def print_fit(self):
        p = self.sim['fit_poisson']['p']
        print(f'{p[3]:10.1f}{p[1]:10.2f}{p[2]:10.3f}')

    def plot_fit(self):
        wave = self.sim['wave']        
        spec_model = self.sim['model']        
        spec_poisson = self.sim['poisson']        
        fit_poisson = self.sim['fit_poisson']['model']
        error = self.sim['fit_poisson']['error']
        fit_counts = self.sim['fit_poisson']['p'][3]
        sum_counts = self.sim['fit_poisson']['p'][4]
        title = f'Total Counts = {self.total_counts} | Sum Counts = {sum_counts:.1f} |'\
            f' Fit Counts = {fit_counts:.1f}'

        plt.errorbar(wave, spec_poisson, error, fmt='.', color='C0')
        plt.step(wave, spec_poisson, where='mid', label='Noisy', color='C0')        
        plt.plot(wave, spec_model, label='Model', color='C1', ls='--')
        plt.plot(wave, fit_poisson, label='Fit Noisy', color='C2', lw=2)
        plt.legend()
        plt.title(title, fontsize=10)
        plt.show()

if __name__ == '__main__':

    o = sim_gaussian_profile(display=True)

                            
