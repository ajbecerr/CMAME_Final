#!/bin/sh
# sbatch sparseRep_1.sh 12 0.05
# sbatch sparseRep_1.sh 12 0.005
# sbatch sparseRep_1.sh 12 0.0005

# sbatch sparseRep_1.sh 12 0.05 rdot CH4
# sbatch sparseRep_1.sh 12 0.005 rdot CH4
# sbatch sparseRep_1.sh 12 0.0005 rdot CH4

# sbatch sparseRep_1.sh 12 0.05 qrad CH4
# sbatch sparseRep_1.sh 12 0.005 qrad CH4
# sbatch sparseRep_1.sh 12 0.0005 qrad CH4

sbatch sparseRep_1.sh 12 0.05 rdot MMA
sbatch sparseRep_1.sh 12 0.005 rdot MMA
sbatch sparseRep_1.sh 12 0.0005 rdot MMA

sbatch sparseRep_1.sh 12 0.05 qtot MMA
sbatch sparseRep_1.sh 12 0.005 qtot MMA
sbatch sparseRep_1.sh 12 0.0005 qtot MMA