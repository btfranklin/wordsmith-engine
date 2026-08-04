import { execFileSync } from "node:child_process";
import { readdirSync } from "node:fs";
import { join } from "node:path";

const exampleRoot = ".example-dist";

function findExamples(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) return findExamples(path);
    return entry.isFile() && entry.name.endsWith(".js") ? [path] : [];
  });
}

const examples = findExamples(exampleRoot).sort();
if (examples.length === 0) {
  throw new Error(`No compiled examples found under ${exampleRoot}.`);
}

for (const example of examples) {
  const output = execFileSync("node", [example], { encoding: "utf8" });
  if (output.trim().length === 0) {
    throw new Error(`Example produced no output: ${example}`);
  }
}

process.stdout.write(`Executed ${examples.length} TypeScript examples.\n`);
