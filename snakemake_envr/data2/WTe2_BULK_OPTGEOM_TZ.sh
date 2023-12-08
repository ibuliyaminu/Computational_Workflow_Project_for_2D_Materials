#!/bin/bash
#SBATCH -J Te2W_BULK_OPTGEOM_TZ
#SBATCH -o Te2W_BULK_OPTGEOM_TZ-%J.o
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=32
#SBATCH -A mendoza_q
#SBATCH -N 1
#SBATCH -t 7-00:00:00
#SBATCH --mem-per-cpu=5G
export JOB=Te2W_BULK_OPTGEOM_TZ
export DIR=$SLURM_SUBMIT_DIR
export scratch=$SCRATCH/crys17

echo "submit directory: "
echo $SLURM_SUBMIT_DIR

ml -* CRYSTAL/17

mkdir  -p $scratch/$JOB
cp $DIR/$JOB.d12  $scratch/$JOB/INPUT
cd $scratch/$JOB

srun Pcrystal 2>&1 >& $DIR/${JOB}.out
cp fort.9 ${DIR}/${JOB}.f9
