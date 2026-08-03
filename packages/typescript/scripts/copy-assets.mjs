import { copyFileSync, mkdirSync, readdirSync } from "node:fs";

const sourceRoot = new URL("../src/assets/", import.meta.url);
const destinationRoot = new URL("../dist/assets/", import.meta.url);
const assetNames = readdirSync(sourceRoot)
  .filter((name) => name.endsWith(".json"))
  .sort();

if (assetNames.length === 0) {
  throw new Error("No package JSON assets were found.");
}

mkdirSync(destinationRoot, { recursive: true });
for (const assetName of assetNames) {
  copyFileSync(new URL(assetName, sourceRoot), new URL(assetName, destinationRoot));
}
