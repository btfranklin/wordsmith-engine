# Documentation Index

This directory is the repo-local system of record for agent-readable project
knowledge that does not belong in the public README.

## Core References

- [Behavioral Contract](../spec/BEHAVIOR.md): language-neutral component semantics and conformance rules.
- [Architecture](architecture.md): package layout, dependency direction, and generator design rules.
- [Exotic Character Assets](exotic-character-assets.md): Unicode sources,
  repertoire boundaries, and refresh guidance for exotic character sets.
- [Name Assets](name-assets.md): grouped given-name data source, license, refresh command, and curation rules.
- [Quality](quality.md): validation commands, public API checklist, and release workflow notes.

## Maintenance Rules

- Keep `AGENTS.md` short and route deeper guidance here.
- Add or update docs when a convention would otherwise live only in chat, memory,
  or a one-off PR comment.
- Prefer small focused docs over one large reference file.
