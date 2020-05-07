#!/usr/bin/env python

from sim_gaussian_profile import sim_gaussian_profile
import numpy as np

init = True
nsim = 100
total_counts = [100,200,400,800,1600,3200,6400]

def print_data(c, data):
    global init
    global nsim
    if init:
        print(f'nsim = {nsim}')
        print(f'{"Counts":>10s}{"MeanSum":>10s}{"R":>10s}'
              f'{"MeanFit":>10s}{"R":>10s}{"Std":>10s}{"R":>10s}')
        init = False
    
    peak, cent, width, ints, total = zip(*data)
    print(f'{c:10d}'
          f'{np.mean(total):10.1f}'
          f'{np.mean(total)/c:10.3f}'          
          f'{np.mean(ints):10.1f}'
          f'{np.mean(ints)/c:10.3f}'
          f'{np.std(ints):10.1f}'
          f'{np.std(ints)/np.sqrt(c):10.3f}')

def main(poisson=True):
    global init
    print(f' Poisson Likelihood = {poisson}')
    init = True
    for c in total_counts:
        data = []
        for n in range(nsim):
            o = sim_gaussian_profile(total_counts=c, poisson=poisson)
            data.append(o.sim['fit_poisson']['p'])
        print_data(c, data)


main(poisson=False)
main(poisson=True)
