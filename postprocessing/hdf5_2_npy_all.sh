#!/bin/sh
for i in {1..32}
do
  sbatch hdf5_2_npy_1.sh paraffin $i
  sbatch hdf5_2_npy_1.sh pmma $i
done
