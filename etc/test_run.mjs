#!/usr/bin/env zx

// import "zx/globals";

let date = await $`date`;
await $`echo Current date is ${date}.`;

console.log(chalk.blue("Hello world!"));

const docker = async (...args) => {
  // run a docker image
  try {
    const cmdline =
      `docker run --rm -it -v $PWD:/app supadupa:latest python3` +
      args.map((e) => e.toString()).join(" ");
    console.log(chalk.blue("running", cmdline));
    return $`${cmdline}`;
  } catch (p) {
    console.log(chalk.red(p));
    console.log(`Exit code: ${p.exitCode}`);
    console.log(`Error: ${p.stderr}`);
  }
};

const job_name = "test-job";

await docker(
  "scripts/mk_lsh_spec.py",
  "--ngram_size",
  5,
  "--num_perm",
  256,
  "--threshold",
  0.7,
  "--job-id",
  job_name,
  "--output",
  `/app/shared/${job_name}/${job_name}_lsh_spec.pkl`
);

// interface DatasetSpec {
//   name: string;
//   num_of_documents: number;
//   max_num_of_lines_per_document: number;
// }

// function make_ds(
//   name: string,
//   num_of_documents: number,
//   max_num_of_lines_per_document: number
// ): DatasetSpec {
//   return { name, num_of_documents, max_num_of_lines_per_document };
// }

// const datasets = [("ArXiv", 5, 1), ("PuMed", 1, 1), ("Nature", 5, 1)].map(
//   make_ds
// );

// datasets.map(async (ds_name) => {
//   await $`mkdir -p ${os.path.join(basedir, job_name, ds_name)}`;
//   await docker(
//     "scripts/gen_dataset.py",
//     num_of_rows,
//     ">",
//     os.path.join(basedir, job_name, ds_name, "dataset.txt")
//   );
// });
