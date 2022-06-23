for SLURM_ARRAY_TASK_ID in {0..62}
do 
    SLURM_ARRAY_JOB_ID=$SLURM_ARRAY_TASK_ID
    echo "Starting job: $SLURM_ARRAY_JOB_ID"
    ./exp0.sh
done 