#!/bin/sh
module load intel/20.2
module load intel-mpi/2020.2
module load gcc/11.2.0
module load cmake/3.22.3
module load valgrind/3.14.0
module load gdb/7.8
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export PETSC_DIR=/projects/academic/chrest/ajbecerr/petsc  
export PETSC_ARCH=arch-ablate-opt
export PKG_CONFIG_PATH="${PETSC_DIR}/${PETSC_ARCH}/lib/pkgconfig:$PKG_CONFIG_PATH"
export HDF5_ROOT="${PETSC_DIR}/${PETSC_ARCH}"
# /projects/academic/chrest/ajbecerr/ablateOpt/ablate --input /projects/academic/chrest/ajbecerr/ABLATE_CMAME/ablateInputs/0dIgnition/ignitionDelayMMA.yaml
/projects/academic/chrest/ajbecerr/ablateOpt/ablate --input /projects/academic/chrest/ajbecerr/ABLATE_CMAME/ablateInputs/0dIgnition/ignitionDelayPentane.yaml