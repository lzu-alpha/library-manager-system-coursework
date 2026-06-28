# 第2项 Git 协作规范制定

## 1. 项目仓库信息

本项目使用 GitHub 作为远程代码托管平台，仓库用于保存系统源码、数据库脚本、测试代码、课程文档、截图材料和阶段性提交记录。

| 项目 | 内容 |
| --- | --- |
| 仓库名称 | `library-manager-system-coursework` |
| 仓库地址 | `https://github.com/lzu-alpha/library-manager-system-coursework` |
| 远程地址 | `https://github.com/lzu-alpha/library-manager-system-coursework.git` |
| 仓库所有者 | `lzu-alpha` |
| 默认分支 | `main` |
| 可见性 | Public |
| 许可证 | MIT License |
| 当前主要提交 | `23a1bd4` |
| 本地 Git 用户 | `kanglzu <kangzf@lzu.edu.cn>` |

当前仓库已经完成初始化，并已将项目源码和课程交付材料推送到 GitHub。仓库首页应包含 `README.md`，课程文档集中位于 `docs/coursework`。

## 2. 当前提交记录

当前仓库已有以下关键提交：

| 提交号 | 提交说明 | 说明 |
| --- | --- | --- |
| `471b981` | `Initial commit` | GitHub 页面创建仓库时生成的初始提交，包含 `LICENSE` |
| `64917ba` | `complete library manager coursework deliverable` | 本地整理后的项目源码、文档、截图和测试材料 |
| `23a1bd4` | `Merge branch 'main'...` | 合并远程初始提交与本地完整项目后的最终提交 |

当前本地分支 `main` 已跟踪远程分支 `origin/main`。后续开发应在提交前执行：

```bash
git status
git pull origin main
```

确认本地分支与远程分支同步后再进行开发。

## 3. 仓库内容规范

仓库应提交以下内容：

| 内容 | 位置 |
| --- | --- |
| 后端源码 | `src/main/java` |
| 前端页面和静态资源 | `src/main/resources/templates`、`src/main/resources/static` |
| MyBatis SQL 映射 | `src/main/resources/mapper` |
| 数据库脚本 | `src/main/resources/db` |
| 测试代码 | `src/test/java`、`src/test/resources` |
| 项目说明 | `README.md` |
| 上传检查清单 | `SUBMISSION_CHECKLIST.md` |
| 课程实验文档 | `docs/coursework` |

不应提交以下内容：

| 内容 | 原因 |
| --- | --- |
| `target/` | Maven 构建产物，可重新生成 |
| `.idea/`、`.vscode/` | IDE 本地配置，与个人环境相关 |
| `.DS_Store`、`Thumbs.db` | 操作系统临时文件 |
| 本地数据库密码、私钥、Token | 敏感信息，不应进入远程仓库 |
| 临时压缩包、临时渲染目录 | 非项目必要内容 |

`.gitignore` 已配置基础排除规则。新增临时文件前，应先判断是否需要加入 `.gitignore`。

## 4. 分支管理策略

当前课程交付阶段以 `main` 分支为主。若后续继续多人协作，采用以下分支策略。

### 4.1 主分支 `main`

`main` 用于保存稳定版本和最终交付版本。

要求：

1. `main` 分支必须保持可运行、可检查、可提交。
2. 不在 `main` 上直接做大规模实验性修改。
3. 合并前应完成基本编译检查或测试检查。
4. 每次提交信息应说明修改目的。
5. 阶段性版本可使用 Tag 标记。

### 4.2 开发分支 `develop`

`develop` 用于日常集成开发。当前仓库尚未创建该分支，后续多人协作时可创建：

```bash
git checkout -b develop
git push -u origin develop
```

适用场景：

1. 多个功能需要同时开发。
2. 需要先在开发分支完成联调。
3. 不希望未验证代码直接进入 `main`。

### 4.3 功能分支 `feature/*`

功能分支用于开发单个功能或修复单个问题。

命名规则：

```text
feature/module-name
fix/problem-name
docs/document-name
test/test-scope
```

示例：

```bash
git checkout -b feature/csv-export
git checkout -b docs/git-collaboration-standard
git checkout -b fix/user-return-book
```

功能完成后通过 Pull Request 合并到 `develop` 或 `main`。

## 5. 提交规范

提交信息应简洁说明本次变更。推荐格式：

```text
<type>: <summary>
```

常用类型：

| 类型 | 说明 | 示例 |
| --- | --- | --- |
| `feat` | 新功能 | `feat: add csv export utility` |
| `fix` | 缺陷修复 | `fix: handle empty book search result` |
| `docs` | 文档修改 | `docs: update git collaboration standard` |
| `test` | 测试相关 | `test: add csv export unit tests` |
| `refactor` | 重构 | `refactor: simplify ajax helper` |
| `chore` | 构建或杂项 | `chore: update gitignore` |

提交前检查：

```bash
git status
git diff
git add <files>
git commit -m "docs: update git collaboration standard"
```

要求：

1. 一个提交只解决一类问题。
2. 不把无关文件混入同一个提交。
3. 不提交未确认用途的临时文件。
4. 修改文档时同步检查链接是否有效。
5. 修改代码时同步考虑是否需要测试。

## 6. 推送规范

推送前先拉取远程更新：

```bash
git pull origin main
```

推送到远程仓库：

```bash
git push origin main
```

当前仓库已经配置远程地址：

```bash
git remote -v
```

应显示：

```text
origin  https://github.com/lzu-alpha/library-manager-system-coursework.git (fetch)
origin  https://github.com/lzu-alpha/library-manager-system-coursework.git (push)
```

如果命令行无法连接 GitHub，而浏览器可以访问 GitHub，应检查本机代理配置。当前环境曾使用本机代理：

```bash
git config http.proxy http://127.0.0.1:7897
git config https.proxy http://127.0.0.1:7897
```

如果不再需要代理，可取消配置：

```bash
git config --unset http.proxy
git config --unset https.proxy
```

## 7. Pull Request 规范

多人协作时，功能分支合并到主分支应使用 Pull Request。

PR 标题建议：

```text
feat: add book export endpoint
docs: update coursework documents
fix: correct user update parameter binding
```

PR 描述应包含：

1. 修改目的。
2. 修改文件范围。
3. 已完成的测试或检查。
4. 可能影响的功能。
5. 是否涉及数据库脚本变更。

合并前检查：

1. 页面能正常访问。
2. 后端接口能正常响应。
3. 数据库脚本未破坏已有结构。
4. 测试用例可运行。
5. 文档链接和截图路径可访问。

## 8. 冲突处理规范

发生冲突时，按以下流程处理：

```bash
git pull origin main
```

如果出现冲突：

1. 打开冲突文件。
2. 查找 `<<<<<<<`、`=======`、`>>>>>>>` 标记。
3. 与相关开发者确认保留内容。
4. 删除冲突标记。
5. 重新执行测试或页面检查。
6. 提交合并结果。

命令示例：

```bash
git status
git add <resolved-files>
git commit
git push origin main
```

冲突处理原则：

1. 不直接覆盖他人修改。
2. 不删除不理解的业务代码。
3. 对数据库脚本冲突要重点确认表结构和初始化数据。
4. 对文档冲突要确认目录链接是否仍然正确。

## 9. 版本标记规范

阶段性版本可使用 Git Tag 标记。

建议标签：

| 标签 | 含义 |
| --- | --- |
| `v0.1-docs` | 文档整理完成 |
| `v0.2-tests` | 测试用例和结果补充完成 |
| `v0.3-integration` | 系统初版整合完成 |
| `v1.0-coursework` | 课程作业最终提交版本 |

创建标签：

```bash
git tag -a v1.0-coursework -m "coursework final version"
git push origin v1.0-coursework
```

## 10. Issue 管理规范

GitHub Issue 用于记录问题、任务和改进点。

Issue 类型：

| 类型 | 示例 |
| --- | --- |
| 功能开发 | 添加导出按钮 |
| 缺陷修复 | 修复还书失败提示 |
| 文档补充 | 补充数据库脚本说明 |
| 测试任务 | 增加控制器层测试 |
| 环境问题 | Maven 无法识别 |

Issue 应包含：

1. 问题描述。
2. 复现步骤或任务目标。
3. 影响范围。
4. 期望结果。
5. 相关文件或截图。

## 11. 安全规范

仓库为公开仓库，必须避免提交敏感信息。

禁止提交：

1. GitHub Token。
2. 数据库真实生产密码。
3. 私钥文件。
4. 个人账号密码。
5. 本机绝对路径形式的隐私信息。

配置文件中的数据库密码如用于课程本地测试，应在 README 中说明需要按本机环境修改。更规范的做法是使用环境变量或单独的本地配置文件。

## 12. 当前仓库协作结论

当前仓库已完成以下 Git 协作配置：

1. 已创建 GitHub 远程仓库。
2. 已配置远程地址 `origin`。
3. 已使用 `main` 作为默认分支。
4. 已合并 GitHub 初始 `LICENSE` 提交。
5. 已推送完整项目源码、文档、截图和测试材料。
6. 已通过 `.gitignore` 排除构建产物、IDE 配置和重复临时材料。
7. 已建立后续分支、提交、PR、冲突处理和版本标记规范。

本项产出物为 Git 协作规范文档和已推送到远程仓库的项目版本。
