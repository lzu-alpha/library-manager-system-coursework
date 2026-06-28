# 代码与文档交付清单

项目名称：Library Manager System Coursework  
建议仓库名：`library-manager-system-coursework`

## 关键新增代码

| 文件 | 说明 |
| --- | --- |
| `src/main/java/com/zbw/controller/LibraryController.java` | 系统整合控制器，包含登录、页面路由、AJAX 接口、CSV 导出接口 |
| `src/main/java/com/zbw/utils/export/CsvExportUtil.java` | CSV 导出工具，支持图书结果和借阅记录导出 |
| `src/main/resources/static/scripts/common/ajaxHelper.js` | 通用 AJAX 辅助脚本，封装加载提示和异常提示 |
| `src/test/java/com/zbw/DetailedBusinessTest.java` | 详细业务测试，覆盖登录、查询、借书、还书、分页和记录组装 |
| `src/test/java/com/zbw/CsvExportUtilTest.java` | CSV 导出工具测试，覆盖表头、数据行、转义和空集合 |

## 核心原有代码

| 目录 | 说明 |
| --- | --- |
| `src/main/java/com/zbw/domain` | 实体类和视图对象 |
| `src/main/java/com/zbw/mapper` | MyBatis Mapper 接口 |
| `src/main/java/com/zbw/service` | 业务接口 |
| `src/main/java/com/zbw/service/impl` | 业务实现 |
| `src/main/resources/mapper` | MyBatis XML SQL 映射 |
| `src/main/resources/templates` | Thymeleaf 页面 |
| `src/main/resources/static` | CSS、图片、Layui、前端脚本 |
| `src/main/resources/db` | 数据库脚本 |

## 文档材料

| 内容 | 位置 |
| --- | --- |
| 12 个分项确认稿 | `docs/coursework/分项确认稿_*.md` |
| 前端页面截图 | `docs/coursework/frontend_screenshots` |
| 实际测试结果 | `docs/coursework/actual_test_results` |
| 附加功能截图 | `docs/coursework/additional_function_screenshots` |
| 系统初版整合截图 | `docs/coursework/initial_integration_screenshots` |
| 联调日志 | `docs/coursework/模块内联调_调试日志.md`、`docs/coursework/模块内联调_详细运行日志.md` |

## Git 上传建议

上传时建议以项目根目录作为仓库根目录，而不是只上传 `docs/coursework`。这样源码、测试、数据库脚本和文档可以保持在同一个仓库中。
