import {
  LandmarkName,
  OrganizationName,
  seededRandom,
  TavernName,
} from "../dist/index.js";

for (const Generator of [TavernName, LandmarkName, OrganizationName]) {
  const rng = seededRandom(5343);
  const generator = new Generator();
  console.log(`${Generator.name}:`);
  for (let index = 0; index < 10; index += 1) {
    console.log(generator.render(rng));
  }
  console.log();
}
