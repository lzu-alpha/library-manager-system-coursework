# 第 2 项：Git 协作规范制定

## 1. 目标

建立统一的 Git 分支管理、提交规范、代码合并和远程仓库管理规则，保证多人协作时版本清晰、责任明确、代码可追溯。

## 2. 远程仓库要求

项目代码应托管到 Gitee 或 GitHub 远程仓库中。远程仓库用于保存项目源码、阶段性提交记录、文档和版本发布记录。

远程仓库应至少包含以下内容：

| 内容 | 说明 |
|---|---|
| 源代码 | 后端 Java 代码、前端页面、静态资源、配置文件 |
| 数据库脚本 | 数据库建表和初始化脚本 |
| 项目文档 | 环境配置、编码规范、接口说明、数据库说明等文档 |
| `.gitignore` | 排除不需要提交的临时文件、编译产物和 IDE 配置 |
| README | 简要说明项目功能、技术栈、启动方式和协作规则 |

不应提交以下内容：

- IDE 本地缓存文件；
- 编译输出目录；
- 操作系统临时文件；
- 本机数据库密码、私钥、Token 等敏感信息；
- 运行日志和临时测试数据。

## 3. 分支管理策略

项目采用主分支、开发分支、功能分支相结合的分支管理方式。

### 3.1 主分支 `main`

`main` 分支用于保存稳定版本代码。

要求：

- 只保存能够正常运行的版本；
- 不直接在 `main` 分支上开发功能；
- 合并到 `main` 前必须完成基本测试；
- 每次合并后应打上阶段性说明或版本标签。

适用场景：

- 阶段作业提交；
- 系统初版发布；
- 最终版本归档。

### 3.2 开发分支 `develop`

`develop` 分支用于日常集成开发。

要求：

- 各功能分支开发完成后先合并到 `develop`；
- 在 `develop` 分支进行模块联调；
- 保持 `develop` 分支基本可运行；
- 发现冲突或联调问题时在该分支集中修复。

适用场景：

- 数据访问层与业务逻辑层联调；
- 接口层与前端页面联调；
- 阶段性功能集成。

### 3.3 功能分支 `feature/*`

`feature/*` 分支用于单个功能开发。

命名格式：

```text
feature/功能名称
```

示例：

```text
feature/user-login
feature/book-search
feature/book-borrow
feature/admin-book-manage
feature/database-init
```

要求：

- 每个功能单独建立分支；
- 一个分支只完成一个明确任务；
- 功能完成并自测后合并到 `develop`；
- 合并完成后可删除已完成的功能分支。

### 3.4 修复分支 `fix/*`

`fix/*` 分支用于修复缺陷。

命名格式：

```text
fix/问题描述
```

示例：

```text
fix/login-error
fix/book-category-query
fix/database-connection
```

要求：

- 问题修复后先合并到 `develop`；
- 如果是影响稳定版本的紧急问题，应同步合并到 `main`；
- 修复提交中应说明问题原因和修改内容。

## 4. 提交规范

每次提交应只包含一个明确变更，提交信息应简洁、准确、可追溯。

提交信息格式：

```text
类型: 提交说明
```

常用类型如下：

| 类型 | 含义 | 示例 |
|---|---|---|
| `feat` | 新增功能 | `feat: add user login service` |
| `fix` | 修复问题 | `fix: correct database connection url` |
| `docs` | 修改文档 | `docs: add environment setup guide` |
| `style` | 调整格式 | `style: format mapper xml files` |
| `refactor` | 代码重构 | `refactor: simplify book query logic` |
| `test` | 添加或修改测试 | `test: add book mapper test cases` |
| `chore` | 构建、配置或杂项 | `chore: update gitignore rules` |

提交示例：

```text
feat: add book category mapper
feat: implement user borrow book service
fix: handle empty book search result
docs: add database initialization steps
test: add borrowing record mapper test
```

不推荐的提交信息：

```text
update
修改
test
111
临时提交
```

## 5. 合并规范

代码合并应遵循以下流程：

1. 从 `develop` 创建功能分支；
2. 在功能分支上完成开发；
3. 本地完成编译检查和基本测试；
4. 提交代码并推送到远程仓库；
5. 发起合并请求；
6. 检查代码冲突、功能完整性和测试结果；
7. 合并到 `develop`；
8. 阶段性功能稳定后，由 `develop` 合并到 `main`。

合并前检查项：

| 检查项 | 要求 |
|---|---|
| 编译检查 | 项目能够正常编译 |
| 单元测试 | 相关 Mapper、Service 测试通过 |
| 配置检查 | 不提交个人数据库密码、绝对路径或本地临时配置 |
| SQL 检查 | 数据库脚本可重复执行或有明确说明 |
| 页面检查 | 页面资源路径正确，静态资源可加载 |
| 冲突检查 | 合并前解决所有代码冲突 |

## 6. 代码冲突处理

多人同时修改同一文件时可能产生冲突。冲突处理原则如下：

- 先拉取远程最新代码；
- 明确冲突双方修改意图；
- 保留正确业务逻辑，不盲目覆盖他人代码；
- 冲突解决后重新运行相关测试；
- 提交信息中说明本次解决了哪些冲突。

常用命令：

```bash
git pull origin develop
git status
git add .
git commit -m "fix: resolve merge conflicts in book module"
git push origin feature/book-search
```

## 7. `.gitignore` 规范

`.gitignore` 用于排除不应进入远程仓库的文件。项目应忽略以下内容：

```gitignore
# Java build output
target/
*.class

# IDE files
.idea/
*.iml
.classpath
.project
.settings/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.bak
```

说明：

- `target/` 是编译输出目录，不应提交；
- `.idea/`、`*.iml` 等是 IDE 本地配置，不应影响其他成员；
- `.DS_Store`、`Thumbs.db` 是操作系统生成文件；
- 日志和临时文件不属于项目源码。

## 8. 远程仓库目录规范

远程仓库建议保持如下结构：

```text
project-root
├── src
│   ├── main
│   │   ├── java
│   │   └── resources
│   └── test
├── docs
├── README.md
├── .gitignore
└── pom.xml / build.gradle
```

其中：

- `src` 保存项目源码；
- `docs` 保存环境配置、编码规范、接口文档、数据库文档等；
- `README.md` 保存项目简介和启动说明；
- `.gitignore` 保存忽略规则；
- `pom.xml` 或 `build.gradle` 保存依赖管理配置。

## 9. 阶段性提交要求

每个阶段完成后应形成一次清晰提交或合并记录。

| 阶段 | 建议提交内容 |
|---|---|
| 开发环境配置 | 配置文件、数据库初始化脚本、环境配置文档 |
| 编码规范制定 | 编码规范文档、格式化规则、质量检查说明 |
| 项目骨架搭建 | 基础目录、工具类、配置文件 |
| 数据访问层开发 | Mapper 接口、XML 映射、数据访问测试 |
| 业务逻辑层开发 | Service 接口与实现、业务测试 |
| 接口层开发 | Controller/API 接口、接口文档 |
| 前端页面开发 | 页面模板、CSS、JavaScript |
| 联调与整合 | 问题修复、联调记录、可运行版本 |

阶段性提交可以保证项目开发过程可追溯，也便于后续检查每个成员的贡献。

## 10. 协作要求

项目协作过程中应遵循以下要求：

1. 开发前先拉取远程最新代码；
2. 不直接在 `main` 分支开发；
3. 不提交个人本地配置和敏感信息；
4. 每次提交保持粒度清晰；
5. 合并前完成自测；
6. 发现问题及时在提交信息或联调记录中说明；
7. 重要功能合并后同步更新文档；
8. 数据库脚本变更必须说明执行顺序和影响范围。

## 11. 本项产出物

本项产出物包括：

- Git 协作规范文档；
- 远程仓库项目；
- `.gitignore` 忽略规则；
- 分支管理说明；
- 提交信息规范；
- 合并与冲突处理规则。

通过以上规范，可以保证项目在多人协作开发时版本清晰、提交可追溯、代码合并有依据，减少因分支混乱、文件误提交和冲突处理不当造成的问题。
