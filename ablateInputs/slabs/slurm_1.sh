#!/bin/sh
#SBATCH -N 1
#SBATCH -J 2dSlab
#SBATCH -t 24:00:00
#SBATCH -p pbatch
#SBATCH --mail-type=ALL
#SBATCH -A sunyb
#SBATCH --mail-user=ajbecerr@buffalo.edu
# module load python
# cd ../../preprocessing/
# python perturbMechs.py $1 $2
# python perturbSlabs.py $1 $2
# cd ../ablateInputs/slabs/
# module purge
module load gcc/10.3.1-magic 
module load cmake/3.25.2
export PETSC_DIR="/usr/workspace/ajbecerr/petsc" #UPDATE to the real path of petsc
export PETSC_ARCH="arch-ablate-opt-gcc"
export PKG_CONFIG_PATH="${PETSC_DIR}/${PETSC_ARCH}/lib/pkgconfig:$PKG_CONFIG_PATH"
export HDF5_ROOT="${PETSC_DIR}/${PETSC_ARCH}"  
export PATH="${PETSC_DIR}/${PETSC_ARCH}/bin:$PATH"
srun -n36 /usr/workspace/ajbecerr/ablateOpt/ablate --input /p/lustre2/ubchrest/CMAME_Final/ablateInputs/slabs/slabBurner.2D.pmma.1_soot.yaml
# srun -n36 /usr/workspace/ajbecerr/ablateOpt/ablate --input /p/lustre2/ubchrest/CMAME_Final/ablateInputs/slabs/slabBurner.2D.$1.$2.yaml
