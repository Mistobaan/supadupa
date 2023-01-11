# README

A distributed locality sensitivity hashing parallel script

## SLURM JOB

```bash
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


When datasets are created by scraping raw text from the Internet, this will often result in the same sequences being repeated multiple times (for example, we find a single 50 word sequence that is repeated in the C4 dataset 60,000 times). Training models on deduplicated datasets is faster (because they see fewer total examples) and experimentally results in models with similar or better perplexity to models trained on data that hasn't been deduplicated. Moreover, language models are less likely to exhibit memorization when their training data has been well-deduplicated.
