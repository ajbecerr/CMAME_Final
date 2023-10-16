# Table of Contents

A brief description of some key files and their dependencies is provided below:

- LHS sampling: ``python sampling/ablate_LHS.py``
  - Produces ``sampling/ablate_parameters.csv``
  - 32 samples from a joint distriubtion of ``E_38``, ``E_53``, ``E_155``, and ``velFac``

- ABLATE ensemble: ``bash ablateInputs/slabs/slurm_all.sh``
  - Will ``sbatch`` 32 simulations, 1 for each forward sample
  - Produces raw HDF5 output: ``ablateInputs/slabs/_2dSlab*/domain/*.hdf5``
  - Automatically creates temporary files from templates
  - Template SLURM script: ``ablateInputs/slabs/slurm_1.sh``
  - Template ABLATE input (YAML) file: ``ablateInputs/slabs/slabBurner.2D.yaml``
  - Temporary ABLATE YAML file creation: ``preprocessing/perturbSlabs.py``
  - Template reaction mechanism file: ``ablateInputs/mechs/gri30.yaml``
  - Temporary mechanism file creation: ``preprocessing/perturbMechs.py``

- CHREST format: ``bash postprocessing/tempField_all.sh``
  - Will ``sbatch`` 32 postprocessing jobs, 1 for each sample
  - Converts raw HDF5 output to CHREST format: ``ablateInputs/slabs/_2dSlab*/domain/*.chrest``
  - Only postprocesses time steps from 2000 - end
  - Template SLURM script: ``postprocessing/tempField_1.sh``

- NumPy arrays: ``bash postprocessing/chrest2npy_all.sh``
  - Will ``sbatch`` 32 additional jobs, 1 for each sample
  - Produces 1 NumPy array per sample: ``ablateOutputs/domain_*.py``
  - Extracts spatiotemporal temperature data from CHREST format
  - Template SLURM script: ``postprocessing/chrest2npy_1.sh``
  - Template Python script: ``postprocessing/chrest2npy.py``

- Get QoIs: ``sbatch ablateOutputs/getQoIs.sh``
  - Produces 1 NumPy array per sample: ``ablateOutputs/domain_*_B.py``
  - Extracts max and mean temperature (over all post-processed timesteps) at each grid point
  
- Training: ``cd surrogates/``
  - GPR: ``cd surrogates/GPR/``  
  - HMS: ``bash surrogates/HMS/sparseRep_all.sh`` 
    - Will ``sbatch`` multiple jobs with different hyperparameters
    - Matches input parameters to simulation output from: ``sampling/ablate_parameters.csv``
    - Produces 1 PDF plot per set of hyperparameters (i.e.: per job)
    - Template SLURM script: ``surrogates/HMS/sparseRep_1.sh``
    - Template Python script: ``surrogates/HMS/sparseRep_1.py``
