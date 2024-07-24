import dakota.interfacing as di
import numpy as np
import os
import subprocess

#-----------------------------------------------------------------
params, results = di.read_parameters_file()
A1=params['A1']*1E+13 # 4
b1=params['b1']*1E-01 # 4
E1=params['E1']*1E+01 # 4

#-----------------------------------------------------------------

# with open ('../mechs/MMA_Reduced.yaml', "r") as myfile:
#     inputfile = myfile.readlines()
#     inputfile[1307] = '  rate-constant: {A: '+str(A1)+', b: 0.0, Ea: '+str(E1)+'}\n'
#     inputfile[1908] = '  rate-constant: {A: '+str(A2)+', b: -'+str(b2)+', Ea: '+str(E2)+'}\n'
#     inputfile[1894] = '  rate-constant: {A: '+str(A3)+', b: 0.0, Ea: '+str(E3)+'}\n'
#     inputfile[1892] = '  rate-constant: {A: '+str(A4)+', b: '+str(b4)+', Ea: '+str(E4)+'}\n'    
#     np.savetxt('MMA_Reduced_temp.yaml', inputfile, fmt='%s', newline='')
    
with open ('../mechs/chem-MMA-134S1488R.yaml', "r") as myfile:
    inputfile = myfile.readlines()
    inputfile[2096] = '  rate-constant: {A: '+str(A1)+', b: -'+str(b1)+', Ea: '+str(E1)+'}\n'
    np.savetxt('MMA_temp.yaml', inputfile, fmt='%s', newline='')

#-----------------------------------------------------------------
command = 'bash CanteraIDT.sh' # one_sample.sh
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

(stdout, err) = p.communicate()

output = stdout.splitlines()

#-----------------------------------------------------------------
# with open ('_ignitionDelayMMA/ignitionDelayPeakYi.txt', "r") as myoutfile:
#     outfile = myoutfile.readlines()
#     QoI = float(outfile[0].split(': ')[1])
#     print(QoI)

with open ('ignitionDelay134.txt', "r") as myoutfile:
    outfile = myoutfile.readlines()
    QoI = float(outfile[0]) # float(outfile[0].split(': ')[1])
    print(QoI)

# os.remove('MMA_Reduced_temp.yaml')
# os.remove('_ignitionDelayMMA/ignitionDelayPeakYi.txt')

os.remove('MMA_temp.yaml')
os.remove('ignitionDelay134.txt')

#-----------------------------------------------------------------
for i, r in enumerate(results.responses()):
    r.function = QoI
results.write()
