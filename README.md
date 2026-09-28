# Ducoro Plugins

Official plugins for [Ducoro](https://ducoro.ai), maintained independently of the application.

**English** | [简体中文](README.zh-CN.md)

Each plugin packages agent skills in the marketplace format supported by Ducoro. The catalog lives in [`marketplace.json`](marketplace.json); each plugin has its own manifest and skill instructions.

## Available plugins

| Plugin | What it helps with | Connector dependency |
| --- | --- | --- |
| [Docs Lookup](plugins/docs-lookup) | Answer library and framework questions using current documentation | Context7 |
| [Repo Research](plugins/repo-research) | Understand public GitHub repositories through their documentation | DeepWiki |
| [Git Workflows](plugins/git-workflows) | Write clear commit messages and pull request descriptions | None |

Connectors are configured separately in Ducoro. The skills explain which connector they need and how to add it.

## Use in Ducoro

Ducoro registers this repository automatically as its permanent official source. Open **Plugins → Discover → Official**, review a plugin's contents and license, then install it.

With the Ducoro CLI:

```sh
ducoro-cli plugin browse --marketplace ducoro-official --json
```

The source name is reserved as `ducoro-official`. Ask an agent to install a plugin after you have reviewed its contents and license; installation uses the review token returned by the current browse response.

To check for updates now:

```sh
ducoro-cli plugin marketplace refresh ducoro-official
```

## Updates

Ducoro reads the repository's default branch. A successful source sync makes newly added plugins discoverable and updates plugins already installed from that source. New plugins remain optional installations. The installed record retains the source commit for traceability.

Plugin updates can be published here without releasing a new Ducoro application version. Clients receive them when they next sync, either on the application's schedule or through an explicit sync. A declared license change requires renewed review before an installed plugin follows it.

## Repository layout

```text
marketplace.json
plugins/
  <plugin-name>/
    LICENSE
    .codex-plugin/plugin.json
    skills/
      <skill-name>/
        SKILL.md
        agents/openai.yaml
```

Marketplace entry paths resolve from the repository root. Plugins declare connector dependencies in their skill metadata; this repository distributes skills.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for the plugin format, local validation, and update process. Bug reports and proposals are welcome through [GitHub issues](https://github.com/ducoro/plugins/issues). Please use [private vulnerability reporting](https://github.com/ducoro/plugins/security/advisories/new) for security concerns; see [SECURITY.md](SECURITY.md).

## License

[Apache License 2.0](LICENSE). Third-party services and their documentation remain governed by their respective terms.
