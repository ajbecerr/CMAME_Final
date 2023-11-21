#!/bin/bash
#### See https://hpc.llnl.gov/training/tutorials/slurm-and-moab#LC

##### These lines are for Slurm
#SBATCH -N 64
#SBATCH -J gMsh_arrhenius
#SBATCH -t 24:00:00
#SBATCH -p pbatch
#SBATCH --mail-type=ALL
#SBATCH -A sunyb
#SBATCH --mail-user=kolosret@buffalo.edu

##### Load Required modules
# gcc
module load clang/14.0.6-magic
module load cmake/3.25.2

# Load PETSC ENV
export PETSC_DIR="/usr/workspace/kolosret/petsc"
export PETSC_ARCH="arch-ablate-opt" # arch-ablate-debug or arch-ablate-opt
export PKG_CONFIG_PATH="${PETSC_DIR}/${PETSC_ARCH}/lib/pkgconfig:$PKG_CONFIG_PATH"
export HDF5_ROOT="${PETSC_DIR}/${PETSC_ARCH}"  
# Include the bin directory to access mpi commands
export PATH="${PETSC_DIR}/${PETSC_ARCH}/bin:$PATH"

# Make a temp directory so that tchem has a place to vomit its files
mkdir tmp_$SLURM_JOBID
cd tmp_$SLURM_JOBID

export DM_REFINE=0
export TITLE=results_lowG-dm$DM_REFINE-pmma-cfl-$SLURM_JOBID
export FILE=/p/lustre2/ubchrest/ablateInputs/gmshSlabBurner.pmma.3D/slab_lowG_1011_arrhenius.yaml




##### Launch parallel job using srun
srun -n2304 /usr/workspace/kolosret/ablateOpt/ablate \
   --input $FILE \
   -yaml::environment::title $TITLE \
   -yaml::timestepper::domain::options::dm_refine $DM_REFINE -build_twosided redscatter

echo 'Done'
