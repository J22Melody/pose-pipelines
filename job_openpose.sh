#!/bin/bash
#
#
### comment lines start with ## or #+space
### slurm option lines start with #SBATCH


#SBATCH --job-name=baseline  	## job name
#SBATCH --time=0-01:00:00       ## days-hours:minutes:seconds
#BATCH --mem=4000             ##   3GB ram (hardware ratio is < 4GB/core)

### SBATCH --output=job.out	## standard out file
#SBATCH --ntasks=1            ## Ntasks.  default is 1.
#SBATCH --cpus-per-task=1	## Ncores per task.  Use greater than 1 for multi-threaded jobs.  default is 1.
###BATCH --partition=volta  ##  can specify partition here, but it is pre-empted by what module is loaded
#SBATCH --account=iict-sp2.volk.cl.uzh    ## only need to specify if you belong to multiple tenants on ScienceCluster
#SBATCH --gres gpu:1
###SBATCH --constraint=GPUMEM32GB

VIDEO=${1:-'~/pose-pipelines/example.mp4'}
OUTPUT=${2:-'~/pose-pipelines/example.openpose/'}

module load t4
module load singularityce
module load cudnn/7.6.5.32-10.2

srun singularity exec \
-B /data -B /scratch \
-B /net/cephfs/data \
-B /net/cephfs/scratch \
--nv \
--pwd /openpose/ \
~/data/openpose_latest \
./build/examples/openpose/openpose.bin --video $VIDEO --write_json $OUTPUT --display 0 --face --hand --render_pose 0
# ./build/examples/openpose/openpose.bin --video ~/pose-pipelines/example.mp4 --write_json ~/pose-pipelines/example.openpose/ --write_video ~/pose-pipelines/example.openpose.avi --display 0 --face --hand --render_pose 1