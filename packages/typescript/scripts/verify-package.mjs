import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import {
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));
const packageMetadata = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8"),
);
const canonicalAssetRoot = new URL("../../../assets/", import.meta.url);
const temporaryDirectory = mkdtempSync(join(tmpdir(), "wordsmith-engine-npm-"));
const assetNames = readdirSync(canonicalAssetRoot)
  .filter((name) => name.endsWith(".json"))
  .sort();
assert.ok(assetNames.length > 0, "no canonical JSON assets were found");

function argumentValue(name) {
  const index = process.argv.indexOf(name);
  if (index === -1) {
    return undefined;
  }
  const value = process.argv[index + 1];
  assert.ok(value, `${name} requires a value`);
  return isAbsolute(value) ? value : resolve(process.cwd(), value);
}

function inspectArchive(packagePath) {
  const metadata = JSON.parse(
    execFileSync("tar", ["-xOf", packagePath, "package/package.json"], {
      encoding: "utf8",
    }),
  );
  const paths = new Set(
    execFileSync("tar", ["-tzf", packagePath], { encoding: "utf8" })
      .split("\n")
      .filter((path) => path.startsWith("package/") && !path.endsWith("/"))
      .map((path) => path.slice("package/".length)),
  );
  return { metadata, paths };
}

function packArchive(destination) {
  mkdirSync(destination, { recursive: true });
  const packOutput = execFileSync(
    "npm",
    ["pack", "--json", "--pack-destination", destination],
    { cwd: packageRoot, encoding: "utf8" },
  );
  const packMetadata = JSON.parse(packOutput);
  const packed = Array.isArray(packMetadata)
    ? packMetadata[0]
    : Object.values(packMetadata)[0];
  assert.ok(packed, "npm pack did not return package metadata");
  assert.equal(packed.name, "wordsmith-engine");
  assert.equal(packed.version, packageMetadata.version);
  return join(destination, packed.filename);
}

function selectArchive() {
  const requestedDestination = argumentValue("--pack-destination");
  const requestedPackage = argumentValue("--package");
  assert.ok(
    requestedDestination === undefined || requestedPackage === undefined,
    "--pack-destination and --package cannot be combined",
  );
  if (requestedPackage !== undefined) return requestedPackage;
  return packArchive(requestedDestination ?? temporaryDirectory);
}

function verifyArchiveShape(packagePath) {
  const { metadata, paths } = inspectArchive(packagePath);
  assert.equal(metadata.name, "wordsmith-engine");
  assert.equal(metadata.version, packageMetadata.version);

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
  return metadata.version;
}

function installArchive(packagePath) {
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
  return consumerDirectory;
}

function verifyRuntimeConsumer(consumerDirectory) {
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
}

function verifyDeclarationConsumer(consumerDirectory) {
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
}

function verifyBrowserConsumer(consumerDirectory) {
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
}

function verifyInstalledPackage(consumerDirectory) {
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
  for (const field of [
    "dependencies",
    "optionalDependencies",
    "peerDependencies",
    "bundledDependencies",
    "bundleDependencies",
  ]) {
    assert.equal(installed[field], undefined, `package declares ${field}`);
  }
  const sourceMap = JSON.parse(
    readFileSync(join(installedPackageRoot, "dist/index.js.map"), "utf8"),
  );
  assert.ok(
    Array.isArray(sourceMap.sourcesContent) &&
      sourceMap.sourcesContent.length === sourceMap.sources.length &&
      sourceMap.sourcesContent.every((source) => typeof source === "string"),
    "JavaScript source map does not embed its TypeScript sources",
  );
}

function reportVerification(packagePath, version) {
  process.stdout.write(`${JSON.stringify({ package: packagePath, version })}\n`);
}

try {
  const packagePath = selectArchive();
  const verifiedVersion = verifyArchiveShape(packagePath);
  const consumerDirectory = installArchive(packagePath);
  verifyRuntimeConsumer(consumerDirectory);
  verifyDeclarationConsumer(consumerDirectory);
  verifyBrowserConsumer(consumerDirectory);
  verifyInstalledPackage(consumerDirectory);
  reportVerification(packagePath, verifiedVersion);
} finally {
  rmSync(temporaryDirectory, { recursive: true, force: true });
}
