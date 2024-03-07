#!/bin/sh
#SBATCH -N 1
#SBATCH -J 2dSlab
#SBATCH -t 24:00:00
#SBATCH -p patralab
#SBATCH --gres=gpu:0
#SBATCH --mem=1000g
#SBATCH --mail-type=ALL
##SBATCH -A sunyb
#SBATCH --mail-user=alejandro.becerra@tufts.edu
module load anaconda/2021.05
pip install cantera
python CanteraIDT.py
