# pilev2


## SLURM JOB

```
srun --partition=cpu128 --nodes=1  --ntasks-per-node=1 --cpus-per-task=128  --comment carper --pty bash -i
```


```
#!/bin/bash
#SBATCH --job-name=queue_worker
#SBATCH --output=queue_worker.out
#SBATCH --error=queue_worker.err
#SBATCH --time=01:00:00
#SBATCH --mem=4GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# load work items from queue
work_items=$(<path/to/queue)

# process each work item
for item in $work_items; do
    # replace this with the command to process the work item
    echo "Processing work item: $item"
done
``
