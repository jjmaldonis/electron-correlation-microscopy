#!/bin/sh

#SBATCH --job-name=g4                  # job name
#SBATCH --partition=pre                # default "univ" if not specified
#SBATCH --error=job.%J.err              # error file
#SBATCH --output=job.%J.out             # output file

#SBATCH --time=1-00:00:00               # run time in days-hh:mm:ss

#SBATCH --nodes=1                      # number of nodes requested (n)
#SBATCH --ntasks=1                    # required number of CPUs (n)
#SBATCH --ntasks-per-node=1             # default 16 (Set to 1 for OMP)
#SBATCH --cpus-per-task=1              # default 1 (Set to 16 for OMP)

#SBATCH --mem=12288
#SBATCH --mem-per-cpu=12288

source activate structopt3 && module load compile/intel mpi/intel/openmpi-1.10.2

echo "Date:"
date
echo "Github has:"
git rev-parse --verify HEAD
echo "Using ACI / HCP / Slurm cluster."
echo "JobID = $SLURM_JOB_ID"
echo "Using $SLURM_NNODES nodes"
echo "Using $SLURM_NODELIST nodes."
echo "Number of cores per node: $SLURM_TASKS_PER_NODE"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo ""
cat $@

# Executable
./run_on_aci.sh $1

echo "Finished on:"
date
