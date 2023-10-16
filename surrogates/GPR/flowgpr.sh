#!/bin/sh
#SBATCH -J Flow_GPR #job name
#SBATCH --time=01-00:00:00  #requested time (DD-HH:MM:SS)
#SBATCH -p patralab    #running on "mpi" partition/queue
#SBATCH -c 40  
#SBATCH --mem=400g  
#SBATCH --output=MyJob.%j.out  #saving standard output to file, %j=JOBID,%N=NodeName
#SBATCH --error=MyJob.%j.err   #saving standard error to file, %j=JOBID,%N=NodeName
#SBATCH --mail-type=ALL    #email optitions
#SBATCH --mail-user=georgios.georgalis@tufts.edu

# run python
python3 flow_gpr.py
