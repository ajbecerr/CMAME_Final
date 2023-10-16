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
param_names = ['G', 'E1', 'E257', 'E250', 'b249']

n_params = len(param_names)


#Temperature ranges [melting to boiling in C]

G = np.linspace(5,20,N)
E1 = np.linspace(1.2,1.8, N)*10000  #12000 to 18000 for reaction 1
E257 =  np.linspace(6.4, 9.6, N)*10000        #64000 to 96000 "E2" for reaction 257
E250 =  np.linspace(5.6, 8.4, N)* 1000       # 5600 to 8400 "E3" for reaction 250
b249 = np.linspace(2.03,3.05, N)        #2.03 to 3.05 "b4" for reaction 249


# maximum and minimum values for all parameters

min_params = np.array([min(G), min(E1), min(E257), min(E250), min(b249)])
max_params = np.array([max(G), max(E1), max (E257), max(E250), max(b249)])


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
gas = ct.Solution('../ablateInputs/mechs/MMA_Reduced.yaml')

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
    inletMassFlowKgMin = lhs_scaled[i,5] * inletDensity  # kg/min
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


ablate_params = ['G', 'E1', 'E257', 'E250', 'b249','velFac']



import pandas as pd


pd.DataFrame(lhs_scaled, columns = ablate_params).to_csv('ablate_parameters_MMA.csv')
