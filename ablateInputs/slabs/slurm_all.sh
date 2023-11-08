#!/bin/sh
for i in {1..64}
do
  # sbatch slurm_1.sh paraffin $i
  sbatch slurm_1.sh pmma $i
done
