const fs = require("fs");
const path = require("path");
const http = require("http");
const { spawn } = require("child_process");

const ROOT = __dirname;
const STATIC_DIR = path.join(ROOT, "src", "main", "resources", "static");
const OUT_DIR = path.join(ROOT, "frontend_screenshots");
const PREVIEW_DIR = path.join(OUT_DIR, "preview");
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

fs.mkdirSync(PREVIEW_DIR, { recursive: true });

const css = `
body{margin:0;font-family:Arial,"Microsoft YaHei",sans-serif;background:#f6f7fb;color:#222}
.login-bg{min-height:760px;background:#eef3f9 url('/images/background.png') center/cover no-repeat;padding-top:70px}
.login-card{width:420px;margin:0 auto;padding:34px 34px 28px;background:rgba(242,242,242,.94);border-radius:4px;box-shadow:0 10px 32px rgba(0,0,0,.18)}
.login-title{font-size:30px;color:#c40000;margin:0 0 14px}
.login-subtitle{font-size:22px;margin:0 0 28px}
.layui-body{padding:24px 32px}
.page-title{font-size:28px;font-weight:600;margin:0;text-align:center}
.section-title{font-size:24px;font-weight:600;margin:0}
.panel{background:#fff;border:1px solid #e6e6e6;border-radius:3px;padding:22px;margin-top:18px}
.home-hero{background:#fff;padding:56px;border-radius:3px;border:1px solid #e6e6e6}
.home-hero h1{font-size:34px;margin:0 0 16px}
.home-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}
.home-card{padding:22px;background:#f8fbff;border:1px solid #dce7f7;border-radius:3px}
.home-card strong{display:block;font-size:20px;margin-bottom:8px;color:#009688}
.split{display:grid;grid-template-columns:320px 1fr;gap:44px;align-items:start}
.form-card{background:#fff;border:1px solid #e6e6e6;border-radius:3px;padding:24px}
.center-form{width:480px;margin:20px auto;background:#f2f2f2;padding:28px 32px;border-radius:3px}
.data-table th,.data-table td{text-align:center}
.pagination{display:flex;gap:12px;align-items:center;justify-content:center;margin-top:14px}
.avatar{width:32px;height:32px;border-radius:50%;vertical-align:middle;margin-right:8px}
.layui-layout-admin .layui-header .brand{float:left;color:#009688;font-size:24px;line-height:60px;padding-left:24px}
`;

function layout(role, active, body) {
  const isAdmin = role === "admin";
  const name = isAdmin ? "admin" : "user1";
  const logout = isAdmin ? "/adminLogOut" : "/userLogOut";
  const nav = isAdmin ? adminNav(active) : userNav(active);
  return `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><title>图书管理系统</title>
<link rel="stylesheet" href="/layui/css/layui.css"><style>${css}</style></head>
<body class="layui-layout-body"><div class="layui-layout layui-layout-admin">
<div class="layui-header"><div class="brand">图 书 管 理 系 统</div><ul class="layui-nav layui-layout-right">
<li class="layui-nav-item"><a href="javascript:;"><img src="/images/user_image.jpg" class="layui-nav-img">${name}</a></li>
<li class="layui-nav-item"><a href="${logout}">退出登录</a></li></ul></div>
<div class="layui-side layui-bg-black"><div class="layui-side-scroll">${nav}</div></div>
<div class="layui-body">${body}</div></div><script src="/layui/layui.js"></script></body></html>`;
}

function userNav(active) {
  const cls = (key) => active === key ? "layui-this" : "";
  return `<ul class="layui-nav layui-nav-tree">
<li class="layui-nav-item ${["record","borrow"].includes(active) ? "layui-nav-itemed" : ""}"><a href="javascript:;">借阅管理</a><dl class="layui-nav-child">
<dd class="${cls("record")}"><a href="/userBorrowBookRecord">&emsp;&emsp;借书记录</a></dd>
<dd class="${cls("borrow")}"><a href="/borrowingPage">&emsp;&emsp;借阅书籍</a></dd></dl></li>
<li class="layui-nav-item ${["return","find"].includes(active) ? "layui-nav-itemed" : ""}"><a href="javascript:;">书籍管理</a><dl class="layui-nav-child">
<dd class="${cls("return")}"><a href="/userReturnBooksPage">&emsp;&emsp;归还书籍</a></dd>
<dd class="${cls("find")}"><a href="/findBookPage">&emsp;&emsp;查询书籍</a></dd></dl></li>
<li class="layui-nav-item ${cls("message")}"><a href="/userMessagePage">个人信息</a></li></ul>`;
}

function adminNav(active) {
  const cls = (key) => active === key ? "layui-this" : "";
  return `<ul class="layui-nav layui-nav-tree">
<li class="layui-nav-item ${["addBook","category","showBooks"].includes(active) ? "layui-nav-itemed" : ""}"><a href="javascript:;">书籍管理</a><dl class="layui-nav-child">
<dd class="${cls("addBook")}"><a href="/addBookPage">&emsp;&emsp;录入新书</a></dd>
<dd class="${cls("category")}"><a href="/addCategoryPage?pageNum=1">&emsp;&emsp;新建类别</a></dd>
<dd class="${cls("showBooks")}"><a href="/showBooksPage">&emsp;&emsp;查询书籍</a></dd></dl></li>
<li class="layui-nav-item ${["showUsers","addUser"].includes(active) ? "layui-nav-itemed" : ""}"><a href="javascript:;">用户管理</a><dl class="layui-nav-child">
<dd class="${cls("showUsers")}"><a href="/showUsersPage?pageNum=1">&emsp;&emsp;查询用户</a></dd>
<dd class="${cls("addUser")}"><a href="/addUserPage">&emsp;&emsp;新增用户</a></dd></dl></li>
<li class="layui-nav-item ${active === "records" ? "layui-nav-itemed" : ""}"><a href="javascript:;">借阅信息</a><dl class="layui-nav-child">
<dd class="${cls("records")}"><a href="/allBorrowBooksRecordPage?pageNum=1">&emsp;&emsp;所有记录</a></dd></dl></li>
<li class="layui-nav-item ${cls("adminInfo")}"><a href="/adminInfoPage">个人信息</a></li></ul>`;
}

function table(headers, rows) {
  return `<table class="layui-table data-table"><thead><tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr></thead><tbody>
${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}

function pageLogin() {
  return `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><title>登录</title><link rel="stylesheet" href="/layui/css/layui.css"><style>${css}</style></head>
<body><div class="login-bg"><div class="login-card"><h1 class="login-title">图书管理系统</h1><h2 class="login-subtitle">用户登录</h2>
<form class="layui-form"><div class="layui-form-item"><label class="layui-form-label">用户名:</label><div class="layui-input-block"><input class="layui-input" value="user1"></div></div>
<div class="layui-form-item"><label class="layui-form-label">密 码:</label><div class="layui-input-block"><input type="password" class="layui-input" value="123456"></div></div>
<div class="layui-form-item"><label class="layui-form-label">用户身份</label><div class="layui-input-block"><input type="radio" title="学生" checked><input type="radio" title="管理员"></div></div>
<div class="layui-form-item" style="text-align:center"><button class="layui-btn layui-btn-normal">登录</button></div></form></div></div></body></html>`;
}

const pages = {
  "01_login.html": pageLogin(),
  "02_user_index.html": layout("user", "", `<div class="home-hero"><h1>普通用户首页</h1><p>当前账号可以查询图书、借阅图书、归还图书并查看个人借阅记录。</p><div class="home-grid"><div class="home-card"><strong>查询书籍</strong>按书名关键字检索馆藏。</div><div class="home-card"><strong>借阅书籍</strong>输入图书编号完成借阅。</div><div class="home-card"><strong>借书记录</strong>查看借阅日期和预计归还日期。</div></div></div>`),
  "03_user_find_book.html": layout("user", "find", `<div class="split"><div class="form-card"><hr class="layui-bg-blue"><h1 class="section-title">查询书籍</h1><hr class="layui-bg-blue"><form class="layui-form"><input class="layui-input" value="平凡的世界"><br><button class="layui-btn">查询</button></form></div><div><hr class="layui-bg-blue"><h1 class="section-title">查询结果</h1><hr class="layui-bg-blue">${table(["书籍编号","书名","作者","出版社","状态"], [["1","平凡的世界","路遥","北京出版社","不可借"],["3","数据库系统","李四","清华大学出版社","可借"]])}</div></div>`),
  "04_user_borrow.html": layout("user", "borrow", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">借阅书籍</h2><hr class="layui-bg-blue"><form class="layui-form"><div class="layui-form-item"><label class="layui-form-label">图书编号</label><div class="layui-input-block"><input class="layui-input" value="3"></div></div><div style="text-align:center"><button class="layui-btn">借书</button></div></form></div>`),
  "05_user_return.html": layout("user", "return", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">归还书籍</h2><hr class="layui-bg-blue"><form class="layui-form"><div class="layui-form-item"><label class="layui-form-label">图书编号</label><div class="layui-input-block"><input class="layui-input" value="1"></div></div><div style="text-align:center"><button class="layui-btn">还书</button></div></form></div>`),
  "06_user_record.html": layout("user", "record", `<div class="layui-container"><hr class="layui-bg-blue"><h3 class="page-title">已 借 书 籍</h3><hr class="layui-bg-blue">${table(["书籍ID","书名","借书日期","最晚还书日期"], [["1","平凡的世界","2026-06-01","2026-08-01"],["2","Java程序设计","2026-06-10","2026-08-10"]])}</div>`),
  "07_user_message.html": layout("user", "message", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">个人信息</h2><hr class="layui-bg-blue">${table(["字段","内容"], [["用户编号","1"],["用户名","user1"],["密码","123456"],["邮箱","user1@example.com"]])}<div style="text-align:center"><button class="layui-btn">修改信息</button></div></div>`),
  "08_admin_index.html": layout("admin", "", `<div class="home-hero"><h1>管理员首页</h1><p>管理员可以维护图书、图书分类、用户信息和全部借阅记录。</p><div class="home-grid"><div class="home-card"><strong>书籍管理</strong>录入新书、查询图书、维护分类。</div><div class="home-card"><strong>用户管理</strong>新增用户、查询用户、删除用户。</div><div class="home-card"><strong>借阅信息</strong>查看所有用户借阅记录。</div></div></div>`),
  "09_admin_add_book.html": layout("admin", "addBook", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">添加书籍</h2><hr class="layui-bg-blue"><form class="layui-form">${["书 名","作 者","出版社","类 别","价 格"].map((l,i)=>`<div class="layui-form-item"><label class="layui-form-label">${l}</label><div class="layui-input-block"><input class="layui-input" value="${["数据库系统","李四","清华大学出版社","计算机","59.0"][i]}"></div></div>`).join("")}<div class="layui-form-item"><label class="layui-form-label">简 介</label><div class="layui-input-block"><textarea class="layui-textarea">数据库教材</textarea></div></div><div style="text-align:center"><button class="layui-btn">添加图书</button></div></form></div>`),
  "10_admin_category.html": layout("admin", "category", `<div class="split"><div class="form-card"><hr class="layui-bg-blue"><h2 class="section-title">新建类别</h2><hr class="layui-bg-blue"><input class="layui-input" value="文学"><br><button class="layui-btn">添加类别</button></div><div><hr class="layui-bg-blue"><h2 class="section-title">分类列表</h2><hr class="layui-bg-blue">${table(["分类编号","分类名称","操作"], [["1","小说","删除"],["2","计算机","删除"],["3","历史","删除"]])}<div class="pagination"><button class="layui-btn layui-btn-sm">上一页</button><span>1 / 1</span><button class="layui-btn layui-btn-sm">下一页</button></div></div></div>`),
  "11_admin_show_books.html": layout("admin", "showBooks", `<div class="split"><div class="form-card"><hr class="layui-bg-blue"><h2 class="section-title">查询书籍</h2><hr class="layui-bg-blue"><label>按类别查找</label><select class="layui-select"><option>计算机</option></select><br><br><button class="layui-btn">查找</button></div><div><hr class="layui-bg-blue"><h2 class="section-title">查询结果</h2><hr class="layui-bg-blue">${table(["id","书名","作者","出版社","状态"], [["2","Java程序设计","张三","电子工业出版社","不可借"],["3","数据库系统","李四","清华大学出版社","可借"]])}<div class="pagination"><button class="layui-btn layui-btn-sm">上一页</button><span>1 / 1</span><button class="layui-btn layui-btn-sm">下一页</button></div></div></div>`),
  "12_admin_add_user.html": layout("admin", "addUser", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">新增用户</h2><hr class="layui-bg-blue"><form class="layui-form">${["用户名","密码","邮箱"].map((l,i)=>`<div class="layui-form-item"><label class="layui-form-label">${l}</label><div class="layui-input-block"><input class="layui-input" value="${["newUser","123456","new@example.com"][i]}"></div></div>`).join("")}<div style="text-align:center"><button class="layui-btn">添加用户</button></div></form></div>`),
  "13_admin_show_users.html": layout("admin", "showUsers", `<div class="layui-container"><hr class="layui-bg-blue"><h2 class="page-title">用户管理</h2><hr class="layui-bg-blue">${table(["用户ID","用户名","邮箱","操作"], [["1","user1","user1@example.com","删除"],["2","yxc","yxc@example.com","删除"],["3","user2","user2@example.com","删除"]])}<div class="pagination"><button class="layui-btn layui-btn-sm">上一页</button><span>1 / 1</span><button class="layui-btn layui-btn-sm">下一页</button></div></div>`),
  "14_admin_records.html": layout("admin", "records", `<div class="layui-container"><hr class="layui-bg-blue"><h2 class="page-title">全部借阅记录</h2><hr class="layui-bg-blue">${table(["用户名","图书名","借书日期","最晚还书日期"], [["user1","平凡的世界","2026-06-01","2026-08-01"],["yxc","Java程序设计","2026-06-10","2026-08-10"]])}<div class="pagination"><button class="layui-btn layui-btn-sm">上一页</button><span>1 / 1</span><button class="layui-btn layui-btn-sm">下一页</button></div></div>`),
  "15_admin_info.html": layout("admin", "adminInfo", `<div class="center-form"><hr class="layui-bg-blue"><h2 class="page-title">管理员信息</h2><hr class="layui-bg-blue">${table(["字段","内容"], [["管理员编号","1"],["管理员名称","admin"],["密码","123456"],["邮箱","admin@example.com"]])}<div style="text-align:center"><button class="layui-btn">修改信息</button></div></div>`)
};

for (const [name, html] of Object.entries(pages)) {
  fs.writeFileSync(path.join(PREVIEW_DIR, name), html, "utf8");
}

function contentType(file) {
  if (file.endsWith(".css")) return "text/css";
  if (file.endsWith(".js")) return "application/javascript";
  if (file.endsWith(".png")) return "image/png";
  if (file.endsWith(".jpg") || file.endsWith(".jpeg")) return "image/jpeg";
  if (file.endsWith(".woff2")) return "font/woff2";
  if (file.endsWith(".woff")) return "font/woff";
  if (file.endsWith(".ttf")) return "font/ttf";
  return "text/html; charset=utf-8";
}

function serveFile(res, file) {
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }
  res.writeHead(200, { "Content-Type": contentType(file) });
  fs.createReadStream(file).pipe(res);
}

async function screenshot(pageName, port) {
  const png = path.join(OUT_DIR, pageName.replace(".html", ".png"));
  const url = `http://127.0.0.1:${port}/preview/${pageName}`;
  const args = [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1440,920",
    `--screenshot=${png}`,
    url,
  ];
  await new Promise((resolve, reject) => {
    const child = spawn(CHROME, args, { stdio: "ignore" });
    child.on("exit", code => code === 0 ? resolve() : reject(new Error(`Chrome failed: ${pageName}`)));
  });
}

async function main() {
  const server = http.createServer((req, res) => {
    const clean = decodeURIComponent(req.url.split("?")[0]);
    if (clean.startsWith("/preview/")) {
      return serveFile(res, path.join(PREVIEW_DIR, clean.replace("/preview/", "")));
    }
    return serveFile(res, path.join(STATIC_DIR, clean.replace(/^\/+/, "")));
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const port = server.address().port;
  try {
    for (const pageName of Object.keys(pages)) {
      await screenshot(pageName, port);
      console.log(path.join(OUT_DIR, pageName.replace(".html", ".png")));
    }
  } finally {
    server.close();
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
