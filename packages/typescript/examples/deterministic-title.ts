import { LiteraryTitle, seededRandom } from "../dist/index.js";

const first = new LiteraryTitle().render(seededRandom("example:title"));
const replayed = new LiteraryTitle().render(seededRandom("example:title"));

if (first !== replayed) {
  throw new Error("the seeded title did not replay exactly");
}

console.log(first);
