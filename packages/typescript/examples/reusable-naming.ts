import {
  BusinessAnimal,
  BusinessColor,
  BusinessTrade,
  CompoundCreatureName,
  CompoundLandmarkName,
  HeraldicSymbol,
  join,
  NaturalNameRoot,
  seededRandom,
} from "../dist/index.js";

const rng = seededRandom(5343);
for (const component of [
  join(
    [new BusinessColor(), new BusinessAnimal(), new BusinessTrade()],
    " ",
  ).titleCase(),
  new CompoundCreatureName(),
  new CompoundLandmarkName(),
  new HeraldicSymbol(),
  new NaturalNameRoot({ context: "landmark" }),
  new NaturalNameRoot({ context: "creature" }),
]) {
  console.log(component.render(rng));
}
