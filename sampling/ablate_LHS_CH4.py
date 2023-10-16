# lhsmdu for Latin hypercube sampling,
# numpy for matrix manipulation
# pandas for csv storage
# os for file management

import lhsmdu
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit


N = 32 #number of sims


#Independent params
param_names = ['G', 'E155', 'E38', 'b53']

n_params = len(param_names)


#Temperature ranges [melting to boiling in C]

G = np.linspace(5,20,N)
E155 = np.linspace(27432.0,33528.0, N)  #3.048e+04 +- 10%
E38 =  np.linspace(15430, 15790, N)        #15610 +/- 180
b53 = np.linspace(1.296,1.944, N)        #1.62 +/- 0.324


# maximum and minimum values for all parameters

min_params = np.array([min(G), min(E155), min(E38), min(b53)])
max_params = np.array([max(G), max(E155), max (E38), max(b53)])


# number of simulations

n_sims = N

# Latin hypercube samples, values in [0, 1]
# lhs.shape = (n_params, n_sims)

lhs = lhsmdu.sample(n_params, n_sims)

# scaled samples
# lhs_scaled.shape = (n_sims, n_params)

lhs_scaled = (min_params + (max_params - min_params) * np.array(lhs).T)

#G to m^3/min flow

Flow = lhs_scaled[:,0]*(60*(0.0254*0.0254-0.02498*0.00875))/1.331
Flow = Flow[..., None]
lhs_scaled = np.concatenate((lhs_scaled, Flow), 1)

#Calc vel factor

import sympy
from sympy import *
import cantera as ct

print('Runnning Cantera version: ' + ct.__version__)

# matplotlib notebook
import matplotlib.pyplot as plt

# determine the density of gas at the inlet
# # Load in the cti mech file
gas = ct.Solution('../ablateInputs/mechs/gri30.yaml')

# Define inlet density
inletTemperature = 300  # Kelvin
inletPressure = 101325  # Pascals
inletYi = {'O2': 1.0}
gas.TPY = inletTemperature, inletPressure, inletYi
inletDensity = gas.density

# define the geometry
yo = 0.0;
yh = 0.0254
dia = (yh - yo)
yc = (yo + yh) * 0.5

velFactors = np.zeros(32)

for i in range(0,np.size(Flow, 0)):
    inletMassFlowKgMin = lhs_scaled[i,4] * inletDensity  # kg/min
    inletMassFlow = inletMassFlowKgMin / 60.0
    
    # setup symbols
    y = Symbol('y')
    r = Symbol('r', positive=True)
    f = Symbol('f')
    m = Symbol('m')
    frac = sympy.Rational
    
    # compute the mass flux function
    # for laminar (https://www.kau.edu.sa/Files/0057863/Subjects/Chapter%208.pdf 8-17)
    # velocityProfile = f*(1-(r**2)/((dia**2)/4))
    # for turbulent
    velocityProfile = f * (1 - (r / (dia / 2))) ** frac('1/7')
    
    # for turblent flow
    # int_0..2Pi int_0_dia/2 density*vel*r dr dtheta (note the extra r for integration)
    massFluxProfile = velocityProfile * inletDensity * r * 2 * pi
    
    # this equation does nto change in theta, so scale by 2*pi
    massFlow = integrate(massFluxProfile, (r, 0.0, (dia / 2)-1E-10))
    
    # Solver for f
    conserved = Eq(massFlow, m)
    fSolution = solve(conserved, f)[0]
    print("VelocityFactor: ", fSolution)
    print("VelocityFactor for ", inletMassFlow, " kg/s is ", fSolution.subs(m, inletMassFlow))
    
    velFactors[i] = fSolution.subs(m, inletMassFlow)


velFactors = velFactors[..., None]
lhs_scaled = np.concatenate((lhs_scaled, velFactors), 1)

lhs_scaled = np.delete(lhs_scaled, 4, axis = 1)


ablate_params = ['G', 'E155', 'E38', 'b53', 'velFac']



import pandas as pd


pd.DataFrame(lhs_scaled, columns = ablate_params).to_csv('ablate_parameters_CH4.csv')
