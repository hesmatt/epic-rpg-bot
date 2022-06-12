import time
import shutil
import globals_

import requests
from PIL import Image


def detect_color(rgb, filename):
    img = Image.open(filename)
    img = img.convert('RGBA')
    data = img.getdata()

    for item in data:
        if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]:
            return True
    return False


def solve_epic_guard(message):
    tries = [
        [237, 28, 36, 38, 198, 86, 201, 120, 31, "apple"],
        [217, 17, 27, 198, 252, 255, 109, 64, 1, "life potion"],
        [0, 198, 255, 0, 0, 0, 0, 96, 124, "normie fish"],
        [0, 202, 255, 0, 0, 0, 0, 110, 143, "normie fish"],
        [255, 242, 0, 221, 210, 0, 149, 141, 0, "coin"],
        [194, 235, 71, 77, 98, 11, 40, 40, 40, "zombie eye"],
        [253, 215, 0, 225, 191, 0, 209, 135, 22, "banana"],
        [255, 204, 0, 129, 104, 0, 0, 0, 0, "golden fish"],
        [255, 204, 0, 123, 99, 0, 0, 0, 0, "golden fish"],
        [118, 23, 54, 241, 82, 134, 237, 116, 155, "unicorn horn"],
        [99, 11, 40, 255, 141, 178, 255, 90, 143, "unicorn horn"],
        [230, 0, 0, 164, 0, 0, 196, 0, 0, "ruby"],
        [184, 95, 184, 152, 77, 202, 106, 65, 214, "epic coin"],
        [0, 28, 7, 240, 233, 142, 34, 177, 76, "chip"],
        [37, 197, 85, 8, 44, 18, 36, 36, 36, "epic fish"],
        [37, 197, 85, 4, 22, 9, 36, 36, 36, "epic fish"],
        [0, 170, 242, 43, 191, 255, 36, 36, 36, "mermaid hair"],
        [68, 68, 68, 124, 124, 124, 60, 60, 68, "wolf skin"]
    ]

    answer = globals_.epic_guard_answer
    img_data = requests.get(message.attachments[0]).content
    name = str(time.time()).split(".", 1)[0] + ".png"
    with open("epic_guard_images/" + name, 'wb') as handler:
        handler.write(img_data)
    for item in tries:
        color_one = detect_color((item[0], item[1], item[2]), "epic_guard_images/" + name)
        color_two = detect_color((item[3], item[4], item[5]), "epic_guard_images/" + name)
        color_three = detect_color((item[6], item[7], item[8]), "epic_guard_images/" + name)
        if color_one is True and color_two is True and color_three is True:
            answer = item[9]
    if answer == globals_.epic_guard_answer:
        shutil.copy("epic_guard_images/" + name, "unpassed_epic_guard_images/" + name)
    return answer
