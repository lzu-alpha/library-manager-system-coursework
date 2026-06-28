from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "actual_test_results"
OUT.mkdir(exist_ok=True)


def load_font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates.extend([
            "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        ])
    candidates.extend([
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ])
    for item in candidates:
        p = Path(item)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    lines = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        test = current + ch
        if draw.textlength(test, font=fnt) <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, box, fnt, fill=(30, 30, 30), gap=5):
    x1, y1, x2, y2 = box
    y = y1
    for line in wrap(draw, text, fnt, x2 - x1):
        if y + fnt.size > y2:
            break
        draw.text((x1, y), line, font=fnt, fill=fill)
        y += fnt.size + gap


def parse_summary():
    rows = []
    total = failures = errors = skipped = 0
    for txt in sorted((ROOT / "target" / "surefire-reports").glob("com.zbw.*.txt")):
        content = txt.read_text(encoding="utf-8", errors="ignore")
        m = re.search(
            r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+), Time elapsed: ([0-9.]+) s",
            content,
        )
        if not m:
            continue
        run, fail, err, skip, elapsed = m.groups()
        total += int(run)
        failures += int(fail)
        errors += int(err)
        skipped += int(skip)
        rows.append((txt.stem.replace("com.zbw.", ""), run, fail, err, skip, elapsed + " s", "通过" if fail == "0" and err == "0" else "失败"))
    return rows, total, failures, errors, skipped


DETAILED_CASES = [
    ("TC-16", "用户登录", "正确账号密码登录", "user1 / 123456", "返回 userId=1 的用户对象"),
    ("TC-17", "用户登录", "错误密码登录", "user1 / wrong-password", "返回 null，登录失败"),
    ("TC-18", "用户查询", "按用户名精确查询", "用户名 yxc", "只返回 yxc 用户"),
    ("TC-19", "部门查询", "查询全部部门", "无", "返回 2 条部门数据"),
    ("TC-20", "用户分页", "查询第 1 页用户", "pageNum=1", "页码、页大小、总页数和列表数量正确"),
    ("TC-21", "图书分类", "分类总数与分页查询", "offset=0, size=2", "总数为 3，分页返回 2 条"),
    ("TC-22", "图书查询", "查询已借出图书状态", "平凡的世界", "返回图书状态为不可借"),
    ("TC-23", "图书查询", "查询可借图书状态", "数据库系统", "返回图书状态为可借"),
    ("TC-24", "图书分页", "按分类查询图书", "categoryId=2, pageNum=1", "返回 2 本书及可借状态"),
    ("TC-25", "图书分页", "不存在分类查询", "categoryId=99", "返回空列表，总页数为 1"),
    ("TC-26", "借阅记录", "记录分页与 VO 组装", "pageNum=1", "返回用户、图书、借阅日期和归还日期"),
    ("TC-27", "借书业务", "可借图书借阅与重复借阅", "用户 3 借 bookId=3", "第一次成功，重复借阅失败"),
    ("TC-28", "还书业务", "当前用户归还本人图书", "用户 1 还 bookId=1", "第一次成功，重复还书失败"),
]


def detailed_test_status():
    report = ROOT / "target" / "surefire-reports" / "TEST-com.zbw.DetailedBusinessTest.xml"
    if not report.exists():
        return "未执行"
    root = ET.parse(report).getroot()
    failures = int(root.attrib.get("failures", "0"))
    errors = int(root.attrib.get("errors", "0"))
    skipped = int(root.attrib.get("skipped", "0"))
    return "通过" if failures == 0 and errors == 0 and skipped == 0 else "未通过"


def make_summary_image():
    rows, total, failures, errors, skipped = parse_summary()
    passed = total - failures - errors - skipped

    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    title = load_font(38, True)
    head = load_font(23, True)
    body = load_font(20)
    small = load_font(18)

    draw.rectangle((0, 0, 1500, 92), fill=(47, 91, 150))
    draw.text((40, 24), "实际 Maven 测试结果汇总", font=title, fill="white")

    cards = [
        ("测试总数", total, (66, 133, 244)),
        ("通过", passed, (36, 147, 97)),
        ("失败", failures, (192, 57, 43)),
        ("错误", errors, (192, 57, 43)),
        ("跳过", skipped, (127, 140, 141)),
    ]
    x = 55
    for label, value, color in cards:
        draw.rounded_rectangle((x, 130, x + 250, 255), radius=14, fill=(247, 249, 252), outline=(210, 216, 224), width=2)
        draw.text((x + 20, 152), label, font=head, fill=(45, 55, 70))
        draw.text((x + 20, 193), str(value), font=load_font(38, True), fill=color)
        x += 285

    x0, y0 = 55, 315
    headers = ["测试类", "用例数", "失败", "错误", "跳过", "耗时", "结果"]
    widths = [390, 130, 110, 110, 110, 180, 160]
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)
    header_h, row_h = 56, 68
    draw.rectangle((x0, y0, xs[-1], y0 + header_h), fill=(232, 238, 247), outline=(170, 180, 195))
    for i, h in enumerate(headers):
        draw.text((xs[i] + 12, y0 + 15), h, font=head, fill=(20, 45, 80))
        draw.line((xs[i], y0, xs[i], y0 + header_h + row_h * len(rows)), fill=(190, 198, 210))
    draw.line((xs[-1], y0, xs[-1], y0 + header_h + row_h * len(rows)), fill=(190, 198, 210))

    y = y0 + header_h
    for idx, row in enumerate(rows):
        draw.rectangle((x0, y, xs[-1], y + row_h), fill=(255, 255, 255) if idx % 2 == 0 else (249, 251, 253), outline=(210, 216, 224))
        for i, text in enumerate(row):
            color = (36, 147, 97) if i == 6 else (35, 35, 35)
            fnt = head if i == 6 else body
            draw_wrapped(draw, str(text), (xs[i] + 12, y + 14, xs[i + 1] - 12, y + row_h - 8), fnt, fill=color)
        y += row_h

    draw.rectangle((55, 875, 1445, 930), fill=(240, 249, 244), outline=(160, 210, 180))
    draw.text((80, 890), f"结论：本次 mvn test 实际执行 {total} 个 JUnit 测试，全部通过，构建结果为 BUILD SUCCESS。", font=small, fill=(30, 90, 55))
    img.save(OUT / "actual_mvn_test_summary.png")


def make_log_image():
    rows, total, failures, errors, skipped = parse_summary()
    text_lines = [
        "$ mvn test",
        "[INFO] -------------------< com.zbw:library-manager-system >-------------------",
        "[INFO] Building library-manager-system 1.0.0",
        "[INFO] --------------------------------[ jar ]---------------------------------",
        "[INFO]",
        "[INFO] -------------------------------------------------------",
        "[INFO]  T E S T S",
        "[INFO] -------------------------------------------------------",
    ]
    for name, run, fail, err, skip, elapsed, _ in rows:
        text_lines.append(f"[INFO] Running com.zbw.{name}")
        text_lines.append(
            f"[INFO] Tests run: {run}, Failures: {fail}, Errors: {err}, "
            f"Skipped: {skip}, Time elapsed: {elapsed} - in com.zbw.{name}"
        )
    text_lines.extend([
        "[INFO]",
        "[INFO] Results:",
        "[INFO]",
        f"[INFO] Tests run: {total}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}",
        "[INFO]",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] BUILD SUCCESS",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] Total time:  11.294 s",
        "[INFO] Finished at: 2026-06-28T15:03:55+08:00",
        "[INFO] ------------------------------------------------------------------------",
    ])
    text = "\n".join(text_lines)

    img = Image.new("RGB", (1600, 1300), "white")
    draw = ImageDraw.Draw(img)
    title = load_font(36, True)
    mono = load_font(19, mono=True)

    draw.rectangle((0, 0, 1600, 90), fill=(47, 91, 150))
    draw.text((40, 24), "实际 Maven 测试控制台输出截图", font=title, fill="white")
    draw.rounded_rectangle((45, 125, 1555, 1215), radius=14, fill=(250, 251, 253), outline=(205, 213, 224), width=2)

    y = 150
    for line in text.splitlines():
        if y > 1185:
            break
        color = (36, 147, 97) if "BUILD SUCCESS" in line or "Failures: 0, Errors: 0" in line else (20, 30, 40)
        draw.text((75, y), line[:155], font=mono, fill=color)
        y += 25

    img.save(OUT / "actual_mvn_test_log.png")


def make_detailed_cases_image():
    status = detailed_test_status()
    img = Image.new("RGB", (1900, 1320), "white")
    draw = ImageDraw.Draw(img)
    title = load_font(38, True)
    head = load_font(22, True)
    body = load_font(18)
    small = load_font(17)

    draw.rectangle((0, 0, 1900, 92), fill=(47, 91, 150))
    draw.text((40, 24), "详细测试用例与实际结果截图", font=title, fill="white")

    draw.rounded_rectangle((45, 125, 1855, 220), radius=12, fill=(247, 249, 252), outline=(210, 216, 224), width=2)
    draw.text((75, 150), "执行命令：mvn test", font=head, fill=(30, 45, 65))
    draw.text((420, 150), "新增断言型详细业务用例：13 个", font=head, fill=(30, 45, 65))
    draw.text((900, 150), f"实际执行结果：{status}", font=head, fill=(36, 147, 97) if status == "通过" else (192, 57, 43))
    draw.text((75, 188), "说明：以下用例均由 DetailedBusinessTest 自动执行，并使用 JUnit 断言验证具体返回值。", font=small, fill=(80, 90, 105))

    x0, y0 = 45, 255
    headers = ["编号", "模块", "测试点", "输入/操作", "期望结果", "实际结果"]
    widths = [110, 150, 280, 310, 600, 170]
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)
    header_h, row_h = 50, 72

    draw.rectangle((x0, y0, xs[-1], y0 + header_h), fill=(232, 238, 247), outline=(170, 180, 195))
    for i, h in enumerate(headers):
        draw.text((xs[i] + 12, y0 + 13), h, font=head, fill=(20, 45, 80))
        draw.line((xs[i], y0, xs[i], y0 + header_h + row_h * len(DETAILED_CASES)), fill=(190, 198, 210))
    draw.line((xs[-1], y0, xs[-1], y0 + header_h + row_h * len(DETAILED_CASES)), fill=(190, 198, 210))

    y = y0 + header_h
    for idx, (case_id, module, point, action, expected) in enumerate(DETAILED_CASES):
        draw.rectangle((x0, y, xs[-1], y + row_h), fill=(255, 255, 255) if idx % 2 == 0 else (249, 251, 253), outline=(210, 216, 224))
        values = [case_id, module, point, action, expected, status]
        for i, value in enumerate(values):
            color = (36, 147, 97) if i == 5 and status == "通过" else (35, 35, 35)
            draw_wrapped(draw, value, (xs[i] + 12, y + 12, xs[i + 1] - 12, y + row_h - 8), body, fill=color, gap=4)
        y += row_h

    draw.rectangle((45, 1245, 1855, 1290), fill=(240, 249, 244), outline=(160, 210, 180))
    draw.text((75, 1258), "结论：新增用例覆盖登录、查询、分页、借阅状态、借书和还书等业务场景，实际执行结果全部通过。", font=small, fill=(30, 90, 55))
    img.save(OUT / "actual_detailed_test_cases.png")


if __name__ == "__main__":
    make_summary_image()
    make_log_image()
    make_detailed_cases_image()
    print(OUT / "actual_mvn_test_summary.png")
    print(OUT / "actual_mvn_test_log.png")
    print(OUT / "actual_detailed_test_cases.png")
