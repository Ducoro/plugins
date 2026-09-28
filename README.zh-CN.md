# Ducoro 插件

[Ducoro](https://ducoro.ai) 官方插件仓库，独立于应用维护与更新。

[English](README.md) | **简体中文**

每个插件按照 Ducoro 支持的插件仓库格式打包 Agent 技能。[`marketplace.json`](marketplace.json) 是插件目录，每个插件都有自己的清单和技能说明。

## 现有插件

| 插件 | 用途 | 依赖的连接器 |
| --- | --- | --- |
| [Docs Lookup](plugins/docs-lookup) | 根据最新文档回答库与框架相关问题 | Context7 |
| [Repo Research](plugins/repo-research) | 通过文档理解公开 GitHub 仓库 | DeepWiki |
| [Git Workflows](plugins/git-workflows) | 编写清楚的提交信息和 Pull Request 描述 | 无 |

连接器在 Ducoro 中单独配置。技能说明会告诉 Agent 需要哪个连接器，以及如何添加。

## 在 Ducoro 中使用

把 `ducoro/plugins` 添加为 GitHub 插件来源。在「插件 → 发现」中打开该来源，核对插件内容与许可证后安装。

也可以使用 Ducoro CLI：

```sh
ducoro-cli plugin marketplace add ducoro/plugins --slug ducoro-official
ducoro-cli plugin browse --marketplace ducoro-official --json
```

如果该来源已经登记，请通过 `ducoro-cli plugin marketplace list --json` 查出已有的 slug 并使用它。核对插件内容和许可证后，可以让 Agent 安装；安装使用本次浏览结果返回的 review token。

立即检查更新：

```sh
ducoro-cli plugin marketplace refresh ducoro-official
```

## 更新方式

Ducoro 读取仓库的默认分支。来源同步成功后，新增插件会出现在发现列表中，从该来源安装的已有插件会跟随更新。新增插件由用户选择安装，已安装记录保留来源 commit，便于追溯。

在这个仓库发布插件更新，无须发布新的 Ducoro 应用版本。客户端会在下一次定时同步或主动同步时收到更新。插件声明的许可证发生变化时，已有安装需要重新核对后才能继续跟随。

## 仓库结构

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

插件目录中的路径以仓库根目录为基准。本仓库分发技能，连接器依赖通过技能元数据声明。

## 参与贡献

插件格式、本地检查和更新流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。问题和建议可以提交到 [GitHub Issues](https://github.com/ducoro/plugins/issues)。安全问题请通过[私密漏洞报告](https://github.com/ducoro/plugins/security/advisories/new)反馈，详情见 [SECURITY.md](SECURITY.md)。

## 许可证

采用 [Apache License 2.0](LICENSE)。第三方服务及其文档适用各自的条款。
