import numpy as np
import sys

if str(sys.argv[1]) == 'pmma':
    arr = np.loadtxt('../sampling/ablate_parameters_MMA.csv', delimiter=',', dtype=str)
    params = arr[int(sys.argv[2])]

    x1 = params[2]
    x2 = params[3]
    x3 = params[4]
    x4 = params[5]
    
    with open ('../ablateInputs/mechs/MMAReduced.soot.yml', "r") as myfile:
        inputfile = myfile.readlines()
        inputfile[1325] = '  rate-constant: {A: 2.65e+16, b: -0.6707, Ea: '+str(x1)+'}\n'
        inputfile[1926] = '  rate-constant: {A: 6.42e+15, b: -0.351, Ea: '+str(x2)+'}\n'
        inputfile[1912] = '  rate-constant: {A: 1.0e+12, b: 0.0, Ea: '+str(x3)+'}\n'
        inputfile[1920] = '  rate-constant: {A: 1.86e+05, b: '+str(x4)+', Ea: 2786.81}\n'   
        np.savetxt('../ablateInputs/mechs/MMA_Reduced_'+str(sys.argv[2])+'.yaml', inputfile, fmt='%s', newline='')
    
else:
    arr = np.loadtxt('../sampling/ablate_parameters_CH4.csv', delimiter=',', dtype=str)
    params = arr[int(sys.argv[2])]

    x1 = params[3]
    x2 = params[4]
    x3 = params[2]
    
    with open ('../ablateInputs/mechs/gri30.yaml', "r") as myfile:
        inputfile = myfile.readlines()
        inputfile[1041] = '    rate-constant: {A: 1.12e+14, b: 0.0, Ea: '+str(x1)+'}\n'
        inputfile[1085] = '    rate-constant: {A: 6.6e+08, b: '+str(x2)+', Ea: 1.084e+04}\n'
        inputfile[1368] = '    rate-constant: {A: 3.56e+13, b: 0.0, Ea: '+str(x3)+'}\n'
        np.savetxt('../ablateInputs/mechs/gri30_'+str(sys.argv[2])+'.yaml', inputfile, fmt='%s', newline='')
