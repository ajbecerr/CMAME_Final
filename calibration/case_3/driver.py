#!/usr/bin/env python
import dakota.interfacing as di
from multiscale_new import *
import numpy as np
import pandas as pd
params, results = di.read_parameters_file()

#-----------------------------------------------------------------
Lv = params['Lv']*1E+05

E1 = 15500
E257 = 80000
E250 = 7000
b249 = 2.5
v = 8

#-----------------------------------------------------------------
train_files = glob.glob('PMMA*train.csv')

qoi = 'rdot' # 'rdot' or 'qtot'
j = 3 # 0, 1, 2, or 3
k = 1 # 1, or 2

Data = pd.read_csv(train_files[j%2])
Data = np.array(Data.values)

if qoi == 'rdot':
    Data = np.hstack((Data[:, 3:-1], Data[:, 1].reshape(-1, 1))).astype(float)
else:
    Data = np.hstack((Data[:, 3:-1], Data[:, 2].reshape(-1, 1))).astype(float)
    
max_cols = np.diag([1/max(Data[:, i]) for i in range(len(Data[0]))])

Cs = np.load(Cs[j])
sparse = np.load(sparse[j])
T = np.load(T[j])

#-----------------------------------------------------------------
d_height1 = np.array([0.1*i/200 for i in range(200)])
d_height = d_height1.astype(np.float)

def y(x):
    if x >= 0.026:
        return 0.0086
    else:
        return x - 0.0174

m_height = np.zeros_like(d_height)
for i, x in enumerate(d_height):
    m_height[i] = predict(np.matmul(np.array([[x, y(x), E1, E257, E250, b249, Lv, v]]), max_cols[:-1, :-1]), sparse, T, Cs)

#-----------------------------------------------------------------
for i, r in enumerate(results.responses()):
    r.function = m_height[i]
results.write()