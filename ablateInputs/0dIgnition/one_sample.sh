#!/bin/sh
module load ccrsoft/legacy
module load intel/20.2
module load intel-mpi/2020.2
module load gcc/11.2.0
module load cmake/3.22.3
module load valgrind/3.14.0
module load gdb/7.8
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export PETSC_DIR=/projects/academic/chrest/ajbecerr/petscLegacy
export PETSC_ARCH=arch-ablate-opt
export PKG_CONFIG_PATH="${PETSC_DIR}/${PETSC_ARCH}/lib/pkgconfig:$PKG_CONFIG_PATH"
export HDF5_ROOT="${PETSC_DIR}/${PETSC_ARCH}"
# /projects/academic/chrest/ajbecerr/ablateOptLegacy/ablate --input /projects/academic/chrest/ajbecerr/CMAME_Final/ablateInputs/0dIgnition/ignitionDelayMMA.yaml
/projects/academic/chrest/ajbecerr/ablateOptLegacy/ablate --input /projects/academic/chrest/ajbecerr/CMAME_Final/ablateInputs/0dIgnition/ignitionDelay134.yaml