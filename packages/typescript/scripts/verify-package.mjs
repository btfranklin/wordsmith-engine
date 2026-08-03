import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));
const packageMetadata = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8"),
);
const canonicalAssetRoot = new URL("../../../assets/", import.meta.url);
const temporaryDirectory = mkdtempSync(join(tmpdir(), "wordsmith-engine-npm-"));
const assetNames = [
  "Adjectives.json",
  "Adverbs.json",
  "Chemical Compound Names.json",
  "Common Surnames.json",
  "Exotic Character Sets.json",
  "Given Names.json",
  "Nouns.json",
  "Verbs.json",
];

function argumentValue(name) {
  const index = process.argv.indexOf(name);
  if (index === -1) {
    return undefined;
  }
  const value = process.argv[index + 1];
  assert.ok(value, `${name} requires a value`);
  return isAbsolute(value) ? value : resolve(process.cwd(), value);
}

try {
  const requestedDestination = argumentValue("--pack-destination");
  const requestedPackage = argumentValue("--package");
  assert.ok(
    requestedDestination === undefined || requestedPackage === undefined,
    "--pack-destination and --package cannot be combined",
  );

  let packagePath;
  let verifiedVersion;
  let paths;
  if (requestedPackage !== undefined) {
    packagePath = requestedPackage;
    const archiveMetadata = JSON.parse(
      execFileSync("tar", ["-xOf", packagePath, "package/package.json"], {
        encoding: "utf8",
      }),
    );
    assert.equal(archiveMetadata.name, "wordsmith-engine");
    assert.equal(archiveMetadata.version, packageMetadata.version);
    verifiedVersion = archiveMetadata.version;
    paths = new Set(
      execFileSync("tar", ["-tzf", packagePath], { encoding: "utf8" })
        .split("\n")
        .filter((path) => path.startsWith("package/") && !path.endsWith("/"))
        .map((path) => path.slice("package/".length)),
    );
  } else {
    const packDestination = requestedDestination ?? temporaryDirectory;
    mkdirSync(packDestination, { recursive: true });
    const packOutput = execFileSync(
      "npm",
      ["pack", "--json", "--pack-destination", packDestination],
      { cwd: packageRoot, encoding: "utf8" },
    );
    const packMetadata = JSON.parse(packOutput);
    const packed = Array.isArray(packMetadata)
      ? packMetadata[0]
      : Object.values(packMetadata)[0];
    assert.ok(packed, "npm pack did not return package metadata");
    assert.equal(packed.name, "wordsmith-engine");
    assert.equal(packed.version, packageMetadata.version);
    verifiedVersion = packed.version;
    paths = new Set(packed.files.map(({ path }) => path));
    packagePath = join(packDestination, packed.filename);
  }

  for (const required of [
    "LICENSE",
    "README.md",
    "dist/index.js",
    "dist/index.js.map",
    "dist/index.d.ts",
    "package.json",
    ...assetNames.map((name) => `dist/assets/${name}`),
  ]) {
    assert.ok(paths.has(required), `package is missing ${required}`);
  }
  assert.ok(
    [...paths].every(
      (path) =>
        path === "LICENSE" ||
        path === "README.md" ||
        path === "package.json" ||
        path.startsWith("dist/"),
    ),
    "package contains an unexpected file",
  );
  assert.ok(
    [...paths].every((path) => !path.endsWith(".d.ts.map")),
    "package contains an unusable declaration map",
  );

  const consumerDirectory = join(temporaryDirectory, "consumer");
  mkdirSync(consumerDirectory);
  writeFileSync(
    join(consumerDirectory, "package.json"),
    JSON.stringify({ private: true, type: "module" }),
  );
  execFileSync("npm", ["install", "--ignore-scripts", packagePath], {
    cwd: consumerDirectory,
    stdio: "pipe",
  });
  writeFileSync(
    join(consumerDirectory, "check.mjs"),
    `
      import { LiteraryTitle, Noun, seededRandom } from "wordsmith-engine";
      const rng = seededRandom("package-smoke-test");
      if (!new Noun().render(rng)) process.exit(1);
      if (!new LiteraryTitle().render(rng)) process.exit(1);
    `,
  );
  execFileSync("node", ["check.mjs"], {
    cwd: consumerDirectory,
    stdio: "pipe",
  });
  writeFileSync(
    join(consumerDirectory, "check.ts"),
    `
      import { LiteraryTitle, seededRandom } from "wordsmith-engine";
      new LiteraryTitle().render(seededRandom("type-smoke-test"));
    `,
  );
  writeFileSync(
    join(consumerDirectory, "tsconfig.json"),
    JSON.stringify({
      compilerOptions: {
        target: "ES2022",
        module: "NodeNext",
        moduleResolution: "NodeNext",
        lib: ["ES2022"],
        types: [],
        strict: true,
        noEmit: true,
      },
      include: ["check.ts"],
    }),
  );
  execFileSync(
    join(packageRoot, "node_modules", ".bin", "tsc6"),
    ["-p", "tsconfig.json"],
    { cwd: consumerDirectory, stdio: "pipe" },
  );

  writeFileSync(
    join(consumerDirectory, "browser-entry.js"),
    `
      import { Noun, seededRandom } from "wordsmith-engine";
      if (!new Noun().render(seededRandom("browser-smoke-test"))) {
        throw new Error("unexpected empty noun");
      }
    `,
  );
  const browserBundle = join(consumerDirectory, "browser-bundle.mjs");
  execFileSync(
    join(packageRoot, "node_modules", ".bin", "esbuild"),
    [
      "browser-entry.js",
      "--bundle",
      "--platform=browser",
      "--format=esm",
      `--outfile=${browserBundle}`,
    ],
    { cwd: consumerDirectory, stdio: "pipe" },
  );
  execFileSync("node", [browserBundle], { stdio: "pipe" });

  const installedPackageRoot = join(consumerDirectory, "node_modules/wordsmith-engine");
  for (const assetName of assetNames) {
    assert.deepEqual(
      readFileSync(join(installedPackageRoot, "dist/assets", assetName)),
      readFileSync(new URL(assetName, canonicalAssetRoot)),
      `packed asset bytes differ for ${assetName}`,
    );
  }
  const installed = JSON.parse(
    readFileSync(join(installedPackageRoot, "package.json"), "utf8"),
  );
  assert.equal(installed.dependencies, undefined);
  const sourceMap = JSON.parse(
    readFileSync(join(installedPackageRoot, "dist/index.js.map"), "utf8"),
  );
  assert.ok(
    Array.isArray(sourceMap.sourcesContent) &&
      sourceMap.sourcesContent.length === sourceMap.sources.length &&
      sourceMap.sourcesContent.every((source) => typeof source === "string"),
    "JavaScript source map does not embed its TypeScript sources",
  );

  process.stdout.write(
    `${JSON.stringify({ package: packagePath, version: verifiedVersion })}\n`,
  );
} finally {
  rmSync(temporaryDirectory, { recursive: true, force: true });
}
