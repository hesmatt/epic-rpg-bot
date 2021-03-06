import time

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
    apple = [237, 28, 36, 38, 198, 86, 201, 120, 31, "apple"]
    life_potion = [217, 17, 27, 198, 252, 255, 109, 64, 1, "life potion"]
    normie_fish = [0, 198, 255, 0, 0, 0, 0, 96, 124, "normie fish"]
    coin = [255, 242, 0, 221, 210, 0, 149, 141, 0, "coin"]
    zombie_eye = [194, 235, 71, 77, 98, 11, 40, 40, 40, "zombie eye"]
    banana = [253, 215, 0, 225, 191, 0, 209, 135, 22, "banana"]
    golden_fish = [255, 204, 0, 129, 104, 0, 0, 0, 0, "golden fish"]
    unicorn_horn = [118, 23, 54, 241, 82, 134, 237, 116, 155, "unicorn horn"]
    ruby = [230, 0, 0, 164, 0, 0, 196, 0, 0, "ruby"]
    epic_coin = [184, 95, 184, 152, 77, 202, 106, 65, 214, "epic coin"]
    tries = [apple, life_potion, normie_fish, coin, zombie_eye, banana, golden_fish, unicorn_horn, ruby, epic_coin]
    global epic_guard_answer
    epic_guard_answer = "Tvoje mamka"
    img_data = requests.get(message.attachments[0]).content
    name = str(time.time()).split(".", 1)[0] + ".png"
    with open("epic_guard_images/" + name, 'wb') as handler:
        handler.write(img_data)
    for item in tries:
        color_one = detect_color((item[0], item[1], item[2]), "epic_guard_images/" + name)
        color_two = detect_color((item[3], item[4], item[5]), "epic_guard_images/" + name)
        color_three = detect_color((item[6], item[7], item[8]), "epic_guard_images/" + name)
        if color_one is True and color_two is True and color_three is True:
            epic_guard_answer = item[9]
    return epic_guard_answer
