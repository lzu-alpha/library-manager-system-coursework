# 软件工程课程实验交付文档

项目名称：Library Manager System Coursework  
建议仓库名：`library-manager-system-coursework`

本目录集中存放课程实验文档、页面截图、测试结果、联调日志和系统整合材料。

## 分项文档

| 序号 | 文档 |
| --- | --- |
| 01 | [开发环境配置](01_开发环境配置.md) |
| 02 | [Git 协作规范制定](02_Git协作规范制定.md) |
| 03 | [编码规范与质量检查](03_编码规范与质量检查.md) |
| 04 | [项目骨架搭建](04_项目骨架搭建.md) |
| 05 | [数据访问层编码](05_数据访问层编码.md) |
| 06 | [业务逻辑层编码](06_业务逻辑层编码.md) |
| 07 | [接口层编码](07_接口层编码.md) |
| 08 | [模块内联调](08_模块内联调.md) |
| 09 | [前端页面布局](09_前端页面布局.md) |
| 10 | [前后端交互实现](10_前后端交互实现.md) |
| 11 | [附加功能开发](11_附加功能开发.md) |
| 12 | [系统初版整合](12_系统初版整合.md) |

## 补充材料

| 内容 | 位置 |
| --- | --- |
| 实际测试情况 | [分项补充_实际测试情况.md](分项补充_实际测试情况.md) |
| 模块内联调调试日志 | [模块内联调_调试日志.md](模块内联调_调试日志.md) |
| 模块内联调详细运行日志 | [模块内联调_详细运行日志.md](模块内联调_详细运行日志.md) |
| 后端测试结果 | [actual_test_results](actual_test_results) |
| 前端页面截图 | [frontend_screenshots](frontend_screenshots) |
| 附加功能截图 | [additional_function_screenshots](additional_function_screenshots) |
| 系统初版整合截图 | [initial_integration_screenshots](initial_integration_screenshots) |
| 代码与文档交付清单 | [CODE_MANIFEST.md](CODE_MANIFEST.md) |

## 重点代码位置

| 内容 | 位置 |
| --- | --- |
| 系统整合控制器 | `src/main/java/com/zbw/controller/LibraryController.java` |
| CSV 导出工具 | `src/main/java/com/zbw/utils/export/CsvExportUtil.java` |
| AJAX 公共辅助脚本 | `src/main/resources/static/scripts/common/ajaxHelper.js` |
| 详细业务测试 | `src/test/java/com/zbw/DetailedBusinessTest.java` |
| CSV 导出测试 | `src/test/java/com/zbw/CsvExportUtilTest.java` |

## 使用说明

系统源码仍按 Maven 项目结构保存在 `src` 目录中，运行、测试和打包均在项目根目录执行。本目录只负责集中展示课程文档和证据材料。
