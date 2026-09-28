# Contributing

Thank you for helping improve the official Ducoro plugins.

## Propose a change

Open an issue for a new plugin or a substantial behavior change. Explain the task it supports, when an agent should use it, required tools, and how you will verify the result. Small corrections can go directly to a pull request.

## Plugin contract

1. Create `plugins/<name>/.codex-plugin/plugin.json` with a stable lowercase, hyphenated name, a semantic version, a description, `license: "Apache-2.0"`, and `skills: "./skills/"`.
2. Put each skill in `skills/<skill-name>/SKILL.md`. Its YAML frontmatter declares `name` and `description`. Explain prerequisites, the workflow, observable completion, and failure handling in English.
3. Put discovery metadata in `skills/<skill-name>/agents/openai.yaml`. Declare required connectors under `dependencies.tools`. Keep secrets and machine-specific paths out of the bundle.
4. Add a local entry to the root `marketplace.json`, using `./plugins/<name>` as its source path. Keep the marketplace entry name and plugin manifest name identical.
5. Update both README catalogs when adding, removing, or materially changing a plugin. English is the default documentation language; the root README links to Simplified Chinese.

Each plugin bundle must include an unchanged copy of the root `LICENSE`, so separately installed copies retain the license text.

Only contribute material you have the right to distribute under the repository's Apache-2.0 license. Keep third-party attributions and license notices with any permitted third-party material. Report provenance in the pull request.

## Validate locally

Python 3.11 or newer is sufficient; the checks use only the standard library.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Validation checks the catalog, plugin identities, versions, package paths, skill frontmatter, README catalog coverage, and the repository's skills-only distribution boundary. It complements manual review: verify the changed skill with its declared tools and include the result in your pull request. A structural check cannot prove that an instruction produces a useful result.

## Publish updates

Open a pull request against `main`. Keep each change focused and describe the behavior, validation, and any new tool dependency. Increment a plugin's version when changing its distributed content; use semantic versioning to communicate compatibility. Describe breaking behavior changes prominently.

The default branch is the delivery source. Once a reviewed change lands on `main`, clients can receive it on their next successful sync; an application release is not needed. Installation provenance records the commit. To undo a published change, submit a revert commit so the history remains auditable.
