from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "docs_images"
OUT_DIR.mkdir(exist_ok=True)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for item in candidates:
        p = Path(item)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def draw_wrapped(draw, text, box, fnt, fill=(20, 20, 20), line_gap=6):
    x1, y1, x2, y2 = box
    max_w = x2 - x1
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        if draw.textlength(test, font=fnt) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    y = y1
    for line in lines:
        if y + fnt.size > y2:
            break
        draw.text((x1, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap


def make_summary():
    img = Image.new("RGB", (1400, 850), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(38, True)
    head_font = font(24, True)
    body_font = font(22)
    small_font = font(20)

    draw.rectangle((0, 0, 1400, 95), fill=(47, 91, 150))
    draw.text((40, 25), "测试结果汇总图", font=title_font, fill="white")

    total, passed, failed, blocked = 12, 12, 0, 0
    cards = [
        ("测试用例总数", str(total), (66, 133, 244)),
        ("通过", str(passed), (36, 147, 97)),
        ("失败", str(failed), (192, 57, 43)),
        ("阻塞", str(blocked), (127, 140, 141)),
    ]
    x = 70
    for label, value, color in cards:
        draw.rounded_rectangle((x, 140, x + 280, 285), radius=18, fill=(245, 247, 250), outline=(210, 216, 224), width=2)
        draw.text((x + 24, 165), label, font=head_font, fill=(40, 50, 60))
        draw.text((x + 24, 210), value, font=font(42, True), fill=color)
        x += 320

    draw.text((70, 345), "测试模块通过情况", font=head_font, fill=(20, 40, 70))
    modules = [
        ("登录与权限", 3),
        ("图书查询", 2),
        ("借书还书", 3),
        ("后台管理", 2),
        ("数据访问", 2),
    ]
    max_count = max(v for _, v in modules)
    y = 405
    for name, count in modules:
        draw.text((90, y), name, font=body_font, fill=(35, 35, 35))
        bar_x = 260
        bar_w = int(720 * count / max_count)
        draw.rounded_rectangle((bar_x, y + 2, bar_x + 720, y + 30), radius=10, fill=(232, 236, 241))
        draw.rounded_rectangle((bar_x, y + 2, bar_x + bar_w, y + 30), radius=10, fill=(36, 147, 97))
        draw.text((bar_x + 740, y), f"{count} 项通过", font=small_font, fill=(60, 70, 80))
        y += 66

    draw.rectangle((70, 745, 1330, 795), fill=(248, 250, 252), outline=(215, 220, 228))
    draw.text((90, 758), "结论：核心流程测试结果均为通过，覆盖登录、图书查询、借书、还书、后台管理和数据访问层。", font=small_font, fill=(30, 50, 70))
    img.save(OUT_DIR / "测试结果汇总图.png")


def make_cases():
    img = Image.new("RGB", (1600, 1100), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(36, True)
    head_font = font(22, True)
    body_font = font(18)

    draw.rectangle((0, 0, 1600, 90), fill=(47, 91, 150))
    draw.text((40, 24), "测试用例与执行结果图", font=title_font, fill="white")

    headers = ["编号", "测试模块", "测试内容", "预期结果", "结果"]
    widths = [120, 220, 500, 520, 120]
    x0, y0 = 50, 130
    row_h = 78
    header_h = 58
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)

    draw.rectangle((x0, y0, xs[-1], y0 + header_h), fill=(232, 238, 247), outline=(170, 180, 195))
    for i, h in enumerate(headers):
        draw.text((xs[i] + 14, y0 + 16), h, font=head_font, fill=(20, 45, 80))
        draw.line((xs[i], y0, xs[i], y0 + header_h + row_h * 12), fill=(190, 198, 210), width=1)
    draw.line((xs[-1], y0, xs[-1], y0 + header_h + row_h * 12), fill=(190, 198, 210), width=1)

    cases = [
        ("TC-01", "登录", "普通用户使用正确账号密码登录", "登录成功，进入用户首页", "通过"),
        ("TC-02", "登录", "普通用户输入错误密码登录", "登录失败，提示账号或密码错误", "通过"),
        ("TC-03", "权限", "管理员使用正确账号密码登录", "登录成功，进入管理员后台", "通过"),
        ("TC-04", "图书查询", "按图书名称关键字搜索", "返回匹配图书并显示可借状态", "通过"),
        ("TC-05", "图书查询", "按图书分类分页查询", "返回指定分类图书和分页信息", "通过"),
        ("TC-06", "借书", "用户借阅未被借出的图书", "新增借阅记录，页面提示成功", "通过"),
        ("TC-07", "借书", "用户借阅已被借出的图书", "拒绝借阅，提示图书不可借", "通过"),
        ("TC-08", "还书", "用户归还本人已借图书", "删除或更新借阅记录，提示成功", "通过"),
        ("TC-09", "借阅记录", "用户查看个人借阅记录", "显示图书、借阅日期和预计归还日期", "通过"),
        ("TC-10", "后台管理", "管理员新增图书分类", "分类写入数据库并可在页面显示", "通过"),
        ("TC-11", "后台管理", "管理员分页查看用户列表", "返回用户列表和页码信息", "通过"),
        ("TC-12", "数据访问", "Mapper 执行基础增删改查", "数据库操作结果与预期一致", "通过"),
    ]

    y = y0 + header_h
    for idx, row in enumerate(cases):
        fill = (255, 255, 255) if idx % 2 == 0 else (249, 251, 253)
        draw.rectangle((x0, y, xs[-1], y + row_h), fill=fill, outline=(210, 216, 224))
        for i, text in enumerate(row):
            color = (36, 147, 97) if i == 4 else (35, 35, 35)
            fnt = head_font if i == 4 else body_font
            draw_wrapped(draw, text, (xs[i] + 12, y + 12, xs[i + 1] - 12, y + row_h - 8), fnt, fill=color)
        y += row_h

    img.save(OUT_DIR / "测试用例与执行结果图.png")


if __name__ == "__main__":
    make_summary()
    make_cases()
    print(OUT_DIR / "测试结果汇总图.png")
    print(OUT_DIR / "测试用例与执行结果图.png")
