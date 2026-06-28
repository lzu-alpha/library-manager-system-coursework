from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "actual_test_results"
OUT.mkdir(exist_ok=True)


def get_font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, width):
    lines = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        test = current + ch
        if draw.textlength(test, font=font) <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_text_box(draw, text, xy, width, font, fill=(30, 30, 30), line_gap=6):
    x, y = xy
    for line in wrap_text(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def make_execution_image():
    log_path = OUT / "test_execution_log.txt"
    text = log_path.read_text(encoding="utf-8")
    img = Image.new("RGB", (1500, 1420), "white")
    draw = ImageDraw.Draw(img)
    title_font = get_font(34, True)
    mono = get_font(22)
    body = get_font(22)

    draw.rectangle((0, 0, 1500, 90), fill=(47, 91, 150))
    draw.text((40, 25), "实际测试执行结果截图", font=title_font, fill="white")

    draw.rounded_rectangle((45, 125, 1455, 1305), radius=16, fill=(248, 250, 252), outline=(205, 213, 224), width=2)
    draw_text_box(draw, text, (75, 155), 1350, mono, fill=(20, 30, 40), line_gap=8)

    draw.rectangle((45, 1335, 1455, 1380), fill=(255, 244, 230), outline=(230, 190, 120))
    draw.text((70, 1345), "结论：已在当前项目状态下进行真实测试执行尝试；由于项目缺少运行与构建条件，测试被阻塞。", font=body, fill=(110, 70, 20))
    img.save(OUT / "actual_test_execution_result.png")


def make_case_status_image():
    cases = [
        ("TC-01", "用户登录", "正确账号密码登录", "需启动 Web 应用后验证", "阻塞"),
        ("TC-02", "用户登录", "错误密码登录", "需启动 Web 应用后验证", "阻塞"),
        ("TC-03", "管理员登录", "管理员账号登录", "需启动 Web 应用后验证", "阻塞"),
        ("TC-04", "图书查询", "按关键字查询图书", "需启动 Web 应用并连接数据库", "阻塞"),
        ("TC-05", "图书查询", "按分类分页查询", "需执行 Service/Mapper 测试", "阻塞"),
        ("TC-06", "借书", "借阅未借出图书", "需启动应用并连接数据库", "阻塞"),
        ("TC-07", "借书", "重复借阅已借出图书", "需准备运行环境和测试数据", "阻塞"),
        ("TC-08", "还书", "归还本人已借图书", "需启动应用并连接数据库", "阻塞"),
        ("TC-09", "借阅记录", "查看个人借阅记录", "需启动 Web 应用后验证", "阻塞"),
        ("TC-10", "后台管理", "新增图书分类", "需管理员接口和运行环境", "阻塞"),
        ("TC-11", "后台管理", "分页查看用户列表", "需管理员接口和运行环境", "阻塞"),
        ("TC-12", "数据访问层", "执行 Mapper CRUD 测试", "需 Maven/Gradle 和 JDK", "阻塞"),
    ]
    img = Image.new("RGB", (1650, 1180), "white")
    draw = ImageDraw.Draw(img)
    title_font = get_font(34, True)
    head = get_font(21, True)
    body = get_font(18)

    draw.rectangle((0, 0, 1650, 90), fill=(47, 91, 150))
    draw.text((40, 25), "实际测试用例执行状态图", font=title_font, fill="white")

    headers = ["编号", "模块", "测试内容", "实际执行情况", "结果"]
    widths = [120, 190, 410, 670, 150]
    x0, y0 = 55, 130
    row_h = 75
    header_h = 55
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)

    draw.rectangle((x0, y0, xs[-1], y0 + header_h), fill=(232, 238, 247), outline=(185, 195, 210))
    for i, h in enumerate(headers):
        draw.text((xs[i] + 12, y0 + 15), h, font=head, fill=(20, 45, 80))
        draw.line((xs[i], y0, xs[i], y0 + header_h + row_h * len(cases)), fill=(195, 202, 214))
    draw.line((xs[-1], y0, xs[-1], y0 + header_h + row_h * len(cases)), fill=(195, 202, 214))

    y = y0 + header_h
    for idx, row in enumerate(cases):
        fill = (255, 255, 255) if idx % 2 == 0 else (249, 251, 253)
        draw.rectangle((x0, y, xs[-1], y + row_h), fill=fill, outline=(215, 221, 230))
        for i, text in enumerate(row):
            color = (160, 85, 0) if i == 4 else (35, 35, 35)
            fnt = head if i == 4 else body
            draw_text_box(draw, text, (xs[i] + 10, y + 14), widths[i] - 20, fnt, fill=color, line_gap=4)
        y += row_h

    img.save(OUT / "actual_test_case_status.png")


if __name__ == "__main__":
    make_execution_image()
    make_case_status_image()
    print(OUT / "actual_test_execution_result.png")
    print(OUT / "actual_test_case_status.png")
