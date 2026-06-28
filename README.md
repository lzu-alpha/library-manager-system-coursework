# Library Manager System Coursework

建议仓库名：`library-manager-system-coursework`

这是一个基于 Spring Boot、Thymeleaf、MyBatis 和 MySQL 的图书管理系统课程项目。系统包含普通用户端和管理员端，支持登录、图书查询、借书、还书、图书分类管理、用户管理、借阅记录查看、个人信息维护、CSV 数据导出等功能。

## 项目结构

```text
src/main/java/com/zbw
  controller        页面路由、AJAX 接口、CSV 导出接口
  domain            实体对象和视图对象
  mapper            MyBatis Mapper 接口
  service           业务接口
  service/impl      业务实现
  utils             分页工具、CSV 导出工具

src/main/resources
  db                数据库脚本
  mapper            MyBatis XML 映射
  static            前端静态资源
  templates         Thymeleaf 页面

src/test
  java              单元测试和业务测试
  resources         测试数据库脚本和测试配置

docs/coursework     课程实验文档、截图、测试结果和联调日志
```

## 交付文档

课程实验文档统一整理在：

[docs/coursework/README.md](docs/coursework/README.md)

其中包含 12 个分项确认稿、测试结果、前端页面截图、附加功能截图、系统初版整合截图、联调日志和调试日志。

## 核心功能

- 用户登录、管理员登录、退出登录
- 用户端图书查询、借书、还书、借阅记录、个人信息维护
- 管理员端图书录入、分类维护、图书查询、用户管理、借阅记录查看
- 前后端 AJAX 交互和异常提示
- 搜索筛选、分页控制
- CSV 数据导出
- Mapper、Service、业务流程和导出工具测试

## 运行环境

| 软件 | 建议版本 |
| --- | --- |
| JDK | 1.8 |
| Maven | 3.x |
| MySQL | 8.x |
| 浏览器 | Chrome 或 Edge |

## 运行步骤

1. 创建 MySQL 数据库。
2. 执行 `src/main/resources/db/library-manager-system.sql`。
3. 修改 `src/main/resources/application.yml` 中的数据库用户名和密码。
4. 在项目根目录执行：

```bash
mvn spring-boot:run
```

5. 浏览器访问：

```text
http://localhost:8080/
```

## 测试

```bash
mvn test
```

已整理的测试截图和日志位于：

[docs/coursework/actual_test_results](docs/coursework/actual_test_results)

## 本次整理新增的关键文件

- `README.md`
- `SUBMISSION_CHECKLIST.md`
- `docs/coursework/README.md`
- `src/main/java/com/zbw/controller/LibraryController.java`
- `src/main/java/com/zbw/utils/export/CsvExportUtil.java`
- `src/main/resources/static/scripts/common/ajaxHelper.js`
- `src/test/java/com/zbw/DetailedBusinessTest.java`
- `src/test/java/com/zbw/CsvExportUtilTest.java`

## Git 提交建议

```bash
git init
git add .
git commit -m "complete library manager coursework deliverable"
git branch -M main
git remote add origin <remote-repository-url>
git push -u origin main
```
