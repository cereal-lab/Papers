trap exit SIGINT;
SLURM_ARRAY_JOB_ID=0
for SLURM_ARRAY_TASK_ID in {0..62}
do     
    echo "Starting job: $SLURM_ARRAY_TASK_ID"
    source ./exp0.sh
    cd ..
done 