import argparse
import glob
import os
import pathlib

import pandas as pd


def main(path_list, output_path):
    for dataset_folder in path_list:
        all_documents = []
        dataset_name = os.path.split(dataset_folder[-1])

        for document in glob.glob(os.path.join(dataset_folder, "*")):
            with open(document) as fd:
                rows = fd.readlines()
                df = pd.DataFrame({"text": rows, "idx": range(1, len(rows) + 1)})
                all_documents.append(df)

        df.aggregate(all_documents).to_parquet(
            os.path.join(output_path, dataset_name), partition_cols=["idx"]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument(
        "path", nargs="+", help="list of path to `datasets` Dataset directories"
    )
    args = parser.parse_args()
    main(args.ds_path_list, args.output_path)
