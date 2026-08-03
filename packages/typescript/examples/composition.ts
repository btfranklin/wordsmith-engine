import { Adjective, join, Noun, seededRandom, ws } from "../dist/index.js";

const rng = seededRandom("example:composition");
const subject = join([new Adjective(), new Noun()], " ").titleCase();
const sentence = ws`${subject}!`;

console.log(sentence.render(rng));
