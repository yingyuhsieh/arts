"""Update the requested detail, comparison, and closing PNG slides."""

import ctypes

from rebuild_requested_slides import (
    INK,
    OUT,
    PALE,
    PREFIX,
    TEAL,
    base,
    font,
    panel,
    picture,
    save,
    text,
)


def finish(numbers):
    copy_file = ctypes.WinDLL("kernel32", use_last_error=True).CopyFileW
    copy_file.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool)
    copy_file.restype = ctypes.c_bool
    for n in numbers:
        staging = OUT / f"_rendered_slide_{n:04d}.png"
        final = OUT / f"{PREFIX}{n:04d}.png"
        if not copy_file(str(staging), str(final), False):
            raise ctypes.WinError(ctypes.get_last_error())
        staging.unlink()


def make_12():
    im, d = base("畫面細讀", "四個局部，四條觀看線索", "從尖拱窗到人物目光，觀察伍德如何安排畫面")
    cards = (
        (63, 215, 620, 416, "1.png", "尖拱窗", "真實農舍的窗形，成為全畫的垂直軸線。"),
        (659, 215, 1216, 416, "2.png", "人物與農舍", "兩人並肩站立，屋頂在身後向上收攏。"),
        (63, 440, 620, 641, "3.png", "三齒草叉", "叉齒的直線，呼應衣縫與窗框。"),
        (659, 440, 1216, 641, "4.png", "分岔的視線", "女子望向側邊；男子則直視前方。"),
    )
    for x1, y1, x2, y2, name, heading, description in cards:
        panel(d, (x1, y1, x2, y2), PALE, radius=19)
        picture(im, name, (x1 + 15, y1 + 15, x1 + 205, y2 - 15), "contain", 11)
        text(d, (x1 + 225, y1 + 24), heading, 28, TEAL, True, 295)
        text(d, (x1 + 225, y1 + 76), description, 23, INK, width=295, gap=9)
    save(im, 12)


def make_14():
    im, d = base("風格延伸", "伍德筆下的鄉村", "起伏山丘、整齊田野與小鎮，呈現他的美國中西部想像")
    works = (
        (63, 620, "IMG-004_Stone_City_Iowa_1930.jpg", "Grant Wood — Stone City, Iowa (1930)"),
        (659, 1216, "IMG-005_Midnight_Ride_Paul_Revere_1931.jpg", "Grant Wood — The Midnight Ride of Paul Revere (1931)"),
    )
    for x1, x2, image_name, caption in works:
        panel(d, (x1, 216, x2, 648), fill="#fffdf7", radius=19)
        picture(im, image_name, (x1 + 13, 229, x2 - 13, 554), "contain", 12)
        d.line((x1 + 19, 568, x2 - 19, 568), fill="#c8d9d1", width=2)
        size = 22
        while d.textlength(caption, font=font(size, True)) > x2 - x1 - 42:
            size -= 1
        text(d, (x1 + 21, 585), caption, size, INK, True)
    save(im, 14)


def make_22():
    im, d = base("尾聲", "圖像如何對觀眾說話？", "有些形象直接招呼我們；有些則留下空白，讓我們自己解讀")
    panel(d, (63, 216, 620, 590), fill="#fffdf7", radius=19)
    panel(d, (659, 216, 1216, 590), fill="#fffdf7", radius=19)
    picture(im, "Uncle Sam.png", (83, 232, 355, 502), "contain", 12)
    picture(im, "Columbia reaching out to viewer.jpg", (686, 232, 936, 502), "contain", 12)
    text(d, (370, 284), "山姆大叔", 29, TEAL, True)
    text(d, (370, 347), "指向觀眾，\n直接提出呼喚。", 24, INK, width=220)
    text(d, (951, 284), "哥倫比亞", 29, TEAL, True)
    text(d, (951, 347), "伸出雙手，\n邀請觀眾靠近。", 24, INK, width=230)
    panel(d, (63, 612, 1216, 674), fill=PALE, radius=13)
    text(d, (85, 625), "《美國哥德式》保持沉默；嚴肅的表情，讓觀眾為人物補上故事。", 24, INK, width=1085)
    save(im, 22)


if __name__ == "__main__":
    make_12()
    make_14()
    make_22()
    finish((12, 14, 22))
