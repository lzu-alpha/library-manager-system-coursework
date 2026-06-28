# Git 上传前检查清单

项目名称：Library Manager System Coursework  
建议仓库名：`library-manager-system-coursework`

## 应提交内容

- `pom.xml`
- `README.md`
- `SUBMISSION_CHECKLIST.md`
- `src/main/java`
- `src/main/resources`
- `src/test/java`
- `src/test/resources`
- `docs/coursework`
- `actual_test_results`
- `frontend_screenshots`
- `additional_function_screenshots`
- `initial_integration_screenshots`
- `module_integration_test_output.txt`
- `module_integration_verbose_test_output.txt`
- `generate_frontend_screenshots.js`
- `generate_actual_mvn_test_images.py`

## 不建议提交内容

- `target/`
- `.idea/`
- `docx_render_check/`
- `.DS_Store`
- 本机临时文件
- 打包生成的 `.jar`
- 压缩包备份文件

以上内容已经在 `.gitignore` 中做了基础排除。

## 上传命令

如果目录还没有初始化 Git：

```bash
git init
git add .
git commit -m "complete library manager coursework deliverable"
git branch -M main
git remote add origin <remote-repository-url>
git push -u origin main
```

如果已经有远程仓库：

```bash
git status
git add .
git commit -m "complete library manager coursework deliverable"
git push
```

## 上传后检查

1. 打开远程仓库首页，确认 `README.md` 能正常显示。
2. 打开 `docs/coursework/README.md`，确认 12 个分项文档链接可访问。
3. 打开截图目录，确认测试结果和页面截图已上传。
4. 检查 `src/main/java/com/zbw/controller/LibraryController.java` 是否存在。
5. 检查 `src/main/java/com/zbw/utils/export/CsvExportUtil.java` 是否存在。
6. 检查 `src/test/java/com/zbw/CsvExportUtilTest.java` 是否存在。
7. 确认远程仓库没有上传 `target/`、`.idea/` 等无关目录。
