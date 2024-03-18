import dakota.interfacing as di
import numpy as np
import os
import subprocess

#-----------------------------------------------------------------
params, results = di.read_parameters_file()
E1 = params['E1']*1E+04
E257 = params['E257']*1E+04
E250 = params['E250']*1E+03
b249 = params['b249']*1E+00
Lv = params['Lv']*1E+05
v = params['v']*1E+00

#-----------------------------------------------------------------
command = 'bash one_sample.sh '+str(E1)+' '+str(E257)+' '+str(E250)+' '+str(b249)+' '+str(Lv)+' '+str(v)
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

(stdout, err) = p.communicate()

output = stdout.splitlines()

#-----------------------------------------------------------------
with open ('predict.txt', "r") as myoutfile:
    outfile = myoutfile.readlines()
    QoI = float(outfile[0])
    print(QoI)

os.remove('predict.txt')

#-----------------------------------------------------------------
for i, r in enumerate(results.responses()):
    r.function = QoI
results.write()