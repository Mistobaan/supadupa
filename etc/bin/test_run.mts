#!/usr/bin/env npx -S tsx
import 'zx/globals';

let date = await $`date`;
await $`echo Current date is ${date}.`;

console.log(chalk.blue("Hello world!"));
const container_base_dir = "/app";

const sh = async (cmd: string = 'bash', ...args: any[]) => {
  // run a docker image
  console.log(args);
  try {
    const out =
      await $`docker run \
        --rm -it \
        -v ${process.env.PWD}:${container_base_dir} \
        -w ${container_base_dir} \
        --entrypoint ${cmd} \
        supadupa:latest ${args}`;
    return out.stdout;
  } catch (p) {
    console.log(chalk.red(p));
    console.log(`Exit code: ${p.exitCode}`);
    console.log(`Error: ${p.stderr}`);
    throw p
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

const datasets: DatasetSpec[] = [{
  name: "test-dataset",
  num_of_documents: 10,
  max_num_of_lines_per_document: 1
}]

const ds = datasets[0]
await sh("mkdir", "-p", path.join(container_base_dir, 'shared', 'input', job_name, ds.name));
await sh(
  `python3`,
  'scripts/015_gen_dataset.py',
  ds.name,
  ds.max_num_of_lines_per_document,
  ds.num_of_documents,
  path.join('shared', 'output', job_name, ds.name)
);
