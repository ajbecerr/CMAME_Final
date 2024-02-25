#!/bin/sh
sbatch sparseRep_1.sh 12 0.005 rdot MMA location
sbatch sparseRep_1.sh 12 0.005 rdot MMA sample

sbatch sparseRep_1.sh 12 0.005 qtot MMA location
sbatch sparseRep_1.sh 12 0.005 qtot MMA sample