#!/usr/bin/env npx -S tsx
import 'zx/globals';

let date = await $`date`;
await $`echo Current date is ${date}.`;

console.log(chalk.blue("Hello world!"));
const container_base_dir = "/app";

const sh = async (...args: any[]) => {
  // run a docker image
  console.log(args);
  try {
    const out =
      await $`docker run --rm -it -v ${process.env.PWD}:${container_base_dir} supadupa:latest ${args}`;
    return out.stdout;
  } catch (p) {
    console.log(chalk.red(p));
    console.log(`Exit code: ${p.exitCode}`);
    console.log(`Error: ${p.stderr}`);
  }
};

const job_name = "test-job";

await sh("ls", "-lah");
await sh(
  `${container_base_dir}/scripts/010_mk_lsh_spec.py`,
  "--ngram_size",
  5,
  "--num_perm",
  256,
  "--threshold",
  0.7,
  "--job-id",
  job_name,
  "--output",
  `${container_base_dir}/shared/${job_name}/${job_name}_lsh_spec.pkl`
);

interface DatasetSpec {
  name: string;
  num_of_documents: number;
  max_num_of_lines_per_document: number;
}

const basedir = '/app/shared'

const datasets: DatasetSpec[] = [{ "ArXiv", 5, 1}, { "PuMed", 1, 1}, { "Nature", 5, 1}]
datasets.map(async (ds) => {
  await $`mkdir -p ${path.join(basedir, 'input', job_name, ds.name)}`;
  await sh(
    "scripts/gen_dataset.py",
    ds.max_num_of_lines_per_document,
    ">",
    path.join(basedir, 'output', job_name, ds.name, "dataset.txt")
  );
});
