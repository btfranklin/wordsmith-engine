import {
  Adjective,
  join,
  literal,
  maybe,
  Noun,
  seededRandom,
  ws,
} from "../dist/index.js";

const rng = seededRandom("example:composition");
const subject = join([new Adjective(), new Noun()], " ").titleCase();
const sentence = ws`${subject}!`;

console.log(sentence.render(rng));
console.log(literal("123hello world").titleCase().render(rng));

const options = { probability: 1, label: "always included" };
console.log(maybe("included", options).render(rng));
