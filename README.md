
* Monte Carlo simulation of fits to Gaussian profiles with Poisson noise 

Why isn't R closer to 1 for low count rates?

```
> sim.py
  nsim = 10000
    Counts   MeanSum         R   MeanFit         R       Std         R
       100     101.1     1.011      94.4     0.944      10.9     1.093
       200     197.8     0.989     191.2     0.956      14.9     1.056
       400     401.0     1.003     392.2     0.981      20.7     1.033
       800     799.1     0.999     790.1     0.988      28.9     1.021
      1600    1599.5     1.000    1587.8     0.992      40.1     1.002
      3200    3199.1     1.000    3187.9     0.996      56.7     1.002
      6400    6402.8     1.000    6388.8     0.998      80.9     1.012
```	  
