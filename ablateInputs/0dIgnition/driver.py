import dakota.interfacing as di
import numpy as np
import os
import subprocess

#-----------------------------------------------------------------
params, results = di.read_parameters_file()
# A1=params['A1']*1E+14 # 1
# A2=params['A2']*1E+15 # 257
# A3=params['A3']*1E+12 # 250
# A4=params['A4']*1E+05 # 249
# b2=params['b2']*1E-01 # 257
# b4=params['b4']*1E+00 # 249
# E1=params['E1']*1E+04 # 1
# E2=params['E2']*1E+04 # 257
# E3=params['E3']*1E+03 # 250
# E4=params['E4']*1E+03 # 249
E2=params['E2']*1E-01
E3=params['E3']*1E-01
E4=params['E4']*1E+01
E5=params['E5']*1E-01
A2=params['A2']*1E+10
A3=params['A3']*1E+07
A4=params['A4']*1E+05
A5=params['A5']*1E+09
b2=params['b2']*1E+00
b3=params['b3']*1E+00
b4=params['b4']*1E+00
b5=params['b5']*1E+00

#-----------------------------------------------------------------

# with open ('../mechs/MMA_Reduced.yaml', "r") as myfile:
#     inputfile = myfile.readlines()
#     inputfile[1307] = '  rate-constant: {A: '+str(A1)+', b: 0.0, Ea: '+str(E1)+'}\n'
#     inputfile[1908] = '  rate-constant: {A: '+str(A2)+', b: -'+str(b2)+', Ea: '+str(E2)+'}\n'
#     inputfile[1894] = '  rate-constant: {A: '+str(A3)+', b: 0.0, Ea: '+str(E3)+'}\n'
#     inputfile[1892] = '  rate-constant: {A: '+str(A4)+', b: '+str(b4)+', Ea: '+str(E4)+'}\n'    
#     np.savetxt('MMA_Reduced_temp.yaml', inputfile, fmt='%s', newline='')

with open ('../mechs/pentane.yaml', "r") as myfile:
    inputfile = myfile.readlines()
    # inputfile[1853] = ''
    inputfile[1900] = '  rate-constant: {A: 1.411e+10, b: 0.935, Ea: '+str(E2)+'}\n'
    inputfile[1923] = '  rate-constant: {A: 2.732e+07, b: 1.813, Ea: '+str(E3)+'}\n'
    inputfile[1975] = '  rate-constant: {A: 2.03e+05, b: 2.745, Ea: '+str(E4)+'}\n'
    inputfile[2629] = '  - {P: 10.0 atm, A: 1.07e+09, b: 1.33, Ea: -'+str(E5)+'}\n'
    np.savetxt('pentane_temp.yaml', inputfile, fmt='%s', newline='')

#-----------------------------------------------------------------
command = 'bash one_sample.sh'
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

(stdout, err) = p.communicate()

output = stdout.splitlines()

#-----------------------------------------------------------------
# with open ('_ignitionDelayMMA/ignitionDelayPeakYi.txt', "r") as myoutfile:
with open ('_ignitionDelayPentane/ignitionDelayPeakYi.txt', "r") as myoutfile:
    outfile = myoutfile.readlines()
    QoI = float(outfile[0].split(': ')[1])
    print(QoI)

# os.remove('MMA_Reduced_temp.yaml')
# os.remove('_ignitionDelayMMA/ignitionDelayPeakYi.txt')
os.remove('pentane_temp.yaml')
os.remove('_ignitionDelayPentane/ignitionDelayPeakYi.txt')

#-----------------------------------------------------------------
for i, r in enumerate(results.responses()):
    r.function = QoI
results.write()
