import { execFileSync } from "node:child_process";

for (const example of ["composition.js", "deterministic-title.js"]) {
  execFileSync("node", [`.example-dist/${example}`], { stdio: "pipe" });
}
