#!/bin/bash
#
#
### comment lines start with ## or #+space
### slurm option lines start with #SBATCH


#SBATCH --job-name=baseline  	## job name
#SBATCH --time=0-01:00:00       ## days-hours:minutes:seconds
###SBATCH --mem=4000M             ##   3GB ram (hardware ratio is < 4GB/core)

### SBATCH --output=job.out	## standard out file
#SBATCH --ntasks=1            ## Ntasks.  default is 1.
#SBATCH --cpus-per-task=1	## Ncores per task.  Use greater than 1 for multi-threaded jobs.  default is 1.
###SBATCH --partition=generic  ##  can specify partition here, but it is pre-empted by what module is loaded
###SBATCH --account=your_tenant_name    ## only need to specify if you belong to multiple tenants on ScienceCluster
#SBATCH --gres gpu:1
###SBATCH --gres gpu:Tesla-V100-32GB:1

module load vesta singularity
module load nvidia/cuda10-cudnn7

srun singularity exec \
-B /data -B /scratch \
-B /net/cephfs/data \
-B /net/cephfs/scratch \
--nv \
--pwd /openpose/ \
~/data/openpose_latest \
./build/examples/openpose/openpose.bin --video ~/pose-pipelines/example.mp4 --write_json ~/pose-pipelines/example.openpose/ --write_video ~/pose-pipelines/example.openpose.avi --display 0 --face --hand --render_pose 1