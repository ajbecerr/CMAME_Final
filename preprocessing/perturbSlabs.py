import numpy as np
import sys

if str(sys.argv[1]) == 'pmma':
    arr = np.loadtxt('../sampling/ablate_parameters_MMA.csv', delimiter=',', dtype=str)
    params = arr[int(sys.argv[2])]
    
    x1 = params[7]
    x2 = params[6]
    
    with open ('../ablateInputs/slabs/slabBurner.2D.pmma.1_soot.yaml', "r") as myfile:
        inputfile = myfile.readlines()
        inputfile[4] = '  title: _2dSlabPMMA_'+str(sys.argv[2])+'\n'
        inputfile[81] = '          mechFile: ../mechs/MMA_Reduced_'+str(sys.argv[2])+'.yaml\n'
        inputfile[212] = '                velFac: '+str(x1)+'\n'
        inputfile[280] = '                latentHeatOfFusion: '+str(x2)+'\n'
        np.savetxt('../ablateInputs/slabs/slabBurner.2D.pmma.'+str(sys.argv[2])+'.yaml', inputfile, fmt='%s', newline='')
    
else:
    arr = np.loadtxt('../sampling/ablate_parameters_CH4.csv', delimiter=',', dtype=str)
    params = arr[int(sys.argv[2])]
    
    x1 = params[5]
    
    with open ('../ablateInputs/slabs/slabBurner.2D.paraffin.yaml', "r") as myfile:
        inputfile = myfile.readlines()
        inputfile[4] = '  title: _2dSlabParaffin_'+str(sys.argv[2])+'\n'
        inputfile[81] = '          mechFile: ../mechs/gri30_'+str(sys.argv[2])+'.yaml\n'
        inputfile[206] = '                velFac: '+str(x1)+'\n'
        np.savetxt('../ablateInputs/slabs/slabBurner.2D.paraffin.'+str(sys.argv[2])+'.yaml', inputfile, fmt='%s', newline='')
