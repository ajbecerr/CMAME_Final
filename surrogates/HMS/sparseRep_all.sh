#!/bin/sh
# sbatch sparseRep_1.sh 12 0.005 rdot MMA location
# sbatch sparseRep_1.sh 12 0.005 rdot MMA sample

# sbatch sparseRep_1.sh 12 0.005 qtot MMA location
# sbatch sparseRep_1.sh 12 0.005 qtot MMA sample

sbatch sparseRep_1.sh 6 0.00005 rdot MMA location
sbatch sparseRep_1.sh 6 0.00005 rdot MMA sample

sbatch sparseRep_1.sh 6 0.00005 qtot MMA location
sbatch sparseRep_1.sh 6 0.00005 qtot MMA sample