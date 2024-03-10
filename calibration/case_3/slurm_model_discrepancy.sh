#!/bin/bash
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --constraint=LEGACY
#SBATCH --job-name='model_dis_new'
#SBATCH --output=out_model_dis-%j.out
#SBATCH --error=error_model_dis-%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=72:00:00
#SBATCH --mail-user=ajbecerr@buffalo.edu
#SBATCH --mail-type=ALL

module load ccrsoft/legacy
module load intel/19.5 && \
module load intel-mpi/2019.5 && \
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so && \
module load mkl/2019.5 && \
source $MKL/bin/mklvars.sh intel64 && \
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/danialfa/software/dakota/dependencies/gsl/lib && \
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/academic/danialfa/software/dakota/dependencies/boost/1.49/lib && \
export DAK_INSTALL=/projects/academic/danialfa/software/dakota && \
export PATH=$DAK_INSTALL/bin:$DAK_INSTALL/share/dakota/test:$PATH && \
export PYTHONPATH=$DAK_INSTALL/share/dakota/Python:$PYTHONPATH

eval "$(/projects/academic/danialfa/software/anaconda3/bin/conda shell.bash hook)"
conda activate fenicsproject

srun dakota -i gravity.in