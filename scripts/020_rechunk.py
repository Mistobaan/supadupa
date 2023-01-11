import argparse
import logging
import os

import datasets
from tqdm.auto import tqdm

logging.basicConfig(level=logging.INFO)


def main(op, datasets_fullpath_list):
    dataset_description_collection = {}

    total = 0
    if op == "count":
        for dataset_path in tqdm(datasets_fullpath_list, desc="loading datasets"):
            dataset_name = os.path.basename(dataset_path)
            ds = datasets.load_from_disk(dataset_path, fs=None, keep_in_memory=None)
            dataset_description_collection[dataset_name] = ds
            total += len(ds)
        print(f"Total number of examples: {total}")
        return

    if op == "split":
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    op = parser.add_argument("operation", choices=["split", "count"])
    ds_path_list = parser.add_argument(
        "path", nargs="+", help="list of path to `datasets` Dataset directories"
    )
    args = parser.parse_args()
    main(parser.op, args.ds_path_list)
