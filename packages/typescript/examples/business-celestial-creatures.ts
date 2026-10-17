import {
  BusinessName,
  CelestialBodyName,
  CreatureName,
  seededRandom,
} from "../dist/index.js";

for (const Generator of [BusinessName, CelestialBodyName, CreatureName]) {
  const rng = seededRandom(5343);
  const generator = new Generator();
  console.log(`${Generator.name}:`);
  for (let index = 0; index < 10; index += 1) {
    console.log(generator.render(rng));
  }
  console.log();
}
