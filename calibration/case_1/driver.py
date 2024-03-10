#!/usr/bin/env python
# from __future__ import print_function
import dakota.interfacing as di
import numpy as np
params, results = di.read_parameters_file()
#-----------------------------------------------------------------

from master_model import forward_model





g = params['x1']

#d_height = np.loadtxt( 'gdata_height.dat' )
d_height1 = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140 ])
d_height = d_height1.astype(np.float)


m_height = np.zeros_like(d_height)
for i,h in enumerate(d_height):
    m_height[i] = forward_model(h,g)













#-----------------------------------------------------------------
for i, r in enumerate(results.responses()):
    r.function = m_height[i]
results.write()
