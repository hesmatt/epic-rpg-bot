import asyncio
import random
from pynput.keyboard import Key, Controller
import time
import argparse
import discord
import re
import emoji
import nest_asyncio
from datetime import datetime
import epic_guard_solver as egs
import variables

nest_asyncio.apply()

NUMBER_GUESS_TASK = 1
NAME_GUESS_TASK = 2
EMOJI_GUESS_TASK = 3
LETTER_GUESS_TASK = 4
INVENTORY_COUNT_GUESS_TASK = 5

client = discord.Client()
parser = argparse.ArgumentParser(description="Process app arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--username", default="Vajicko", type=str,
                    help="Set the username for which the script will be reacting")
args = parser.parse_args()
config = vars(args)
is_banned = False
window = None
keyboard = None
is_solving_training = False

global run
run = "no"

global doheal
doheal = "no"

random_work = ["drill"]
next_adventure_timestamp = time.time()
next_training_timestamp = time.time()
next_lootbox_timestamp = time.time()
next_farm_timestamp = time.time()
next_work_timestamp = time.time()


def split(words):
    return [char for char in words]


async def type_message(message):
    for i in split(message):
        if window is not None:
            window.send_keystrokes(i)
        elif keyboard is not None:
            keyboard.type(i)


async def press_enter():
    if window is not None:
        window.send_keystrokes("{ENTER}")
    elif keyboard is not None:
        keyboard.press(Key.enter)
    await asyncio.sleep(1.5)


async def type_command(command):
    if check_ban_status():
        die()

    await type_message("rpg " + command)
    await press_enter()


async def heal():
    if doheal == "yes":
        await type_command("heal")


def check_ban_status():
    return is_banned


def base_emoji_to_epic_rpg_name(basic_emoji_name):
    basic_emoji_name = basic_emoji_name.lower()
    basic_emoji_transcribes = {
        "gem stone": "diamond",
        "gift": "gift",
        "four leaf clover": "four leaf clover"
    }

    return basic_emoji_transcribes.get(basic_emoji_name)


def letter_of_position(word, position):
    word = word + word
    transcribes = {
        "first": word[0],
        "second": word[1],
        "third": word[2],
        "fourth": word[3],
        "fifth": word[4],
        "sixth": word[5],
        "seventh": word[6],
        "eight": word[7],
        "ninth": word[8],
        "tenth": word[9]
    }

    return transcribes.get(position)


def which_fish(fish):
    transcribes = {
        "normiefish": 1,
        "goldenfish": 2,
        "epicfish": 3
    }

    return transcribes.get(fish)


async def solve_training(training_task_text):
    global is_solving_training

    task_type = get_training_task(training_task_text)
    task_text_lines = training_task_text.splitlines()
    answer = "No idea"

    if task_type is NUMBER_GUESS_TASK:
        emoji_to_search = task_text_lines[2].split(":", 1)[1].split(":", 1)[0].replace(":", "").strip().lower().replace(
            "_", " ")
        total_emoji_count = task_text_lines[1].lower().count(emoji_to_search)
        answer = str(total_emoji_count)

    elif task_type is NAME_GUESS_TASK:
        fish = task_text_lines[1].lower().split(":", 1)[1].split(":", 1)[0]
        answer = str(which_fish(fish))

    elif task_type is EMOJI_GUESS_TASK:
        answer = "no"
        real_emoji_name = base_emoji_to_epic_rpg_name(
            task_text_lines[1].split("?", 1)[1].strip().replace(":", "").replace("_", " "))
        given_emoji_name = task_text_lines[1].split("a", 1)[1].split("?")[0].strip().lower().replace("_", " ")
        if given_emoji_name == real_emoji_name:
            answer = "yes"

    elif task_type is LETTER_GUESS_TASK:
        word = task_text_lines[1].split(":", 1)[1].split(":", 1)[0].lower()
        position = task_text_lines[1].split("the", 1)[1].split("letter", 1)[0].strip().lower().replace("*", "")
        answer = str(letter_of_position(word, position))

    elif task_type is INVENTORY_COUNT_GUESS_TASK:
        answer = "no"
        expected_count = int(
            task_text_lines[1].split("than", 1)[1].split(":", 1)[0].replace("<", "").replace(" ", "").strip())
        current_count = get_count_of_item_in_inventory("ruby")
        if current_count > expected_count:
            answer = "yes"

    time.sleep(3)
    await type_message(answer)
    await press_enter()
    is_solving_training = False


def get_training_task(training_task_text):
    training_task_text = training_task_text.lower()

    if "how many" in training_task_text:
        return NUMBER_GUESS_TASK
    elif "what is the name" in training_task_text:
        return NAME_GUESS_TASK
    elif "is this a" in training_task_text:
        return EMOJI_GUESS_TASK
    elif "answer with a letter" in training_task_text:
        return LETTER_GUESS_TASK
    elif "do you have more" in training_task_text:
        return INVENTORY_COUNT_GUESS_TASK


def is_training_task(message):
    if "is training" in message and config["username"].lower() in message:
        return True

    return False


def is_epic_guard_message(message):
    if "epic guard" in message and "485032715008212992" in message.lower():
        return True

    return False


def is_jail_message(message):
    if ("you are in the jail" in message or "is now in the jail" in message or "jail" in message) and config[
        "username"].lower() in message.lower():
        return True

    return False


def die():
    exit(0)


def get_count_of_item_in_inventory(item):
    count = 0
    if item in items:
        count = int(items[item])
        return count

    return count


def get_count_of_consumables_in_inventory(consumable):
    count = 0
    if consumable in consumables:
        count = int(consumables[consumable])
        return count

    return count


def farm_by_seed():
    if get_count_of_consumables_in_inventory("carrotseed") > 0:
        return "carrot"
    if get_count_of_consumables_in_inventory("breadseed") > 0:
        return "bread"
    if get_count_of_consumables_in_inventory("potatoseed") > 0:
        return "potato"
    return "basic"


async def game_runner():
    while True:
        global next_work_timestamp
        global next_adventure_timestamp
        global next_farm_timestamp
        global next_training_timestamp
        global next_lootbox_timestamp
        global is_solving_training

        if check_ban_status():
            die()

        if is_solving_training:
            continue

        time_now = time.time()
        if run == "yes":
            await heal()
            await type_command("hunt")

            await type_command("cd")

            if time_now > next_work_timestamp:
                await type_command(random.choice(random_work))
                next_work_timestamp = time.time() + 300

            if time_now > next_lootbox_timestamp:
                await type_command("withdraw 421k")
                await type_command("buy edgy lootbox")
                next_lootbox_timestamp = time.time() + 10800

            if time_now > next_adventure_timestamp:
                await heal()
                await type_command("adventure")
                next_adventure_timestamp = time.time() + 3600

            if time_now > next_farm_timestamp:
                await type_command("i")
                await type_command("farm " + farm_by_seed())
                next_farm_timestamp = time.time() + 600

            if time_now > next_training_timestamp:
                is_solving_training = True
                await type_command("i")
                await type_command("tr")
                next_training_timestamp = time.time() + 900

        await asyncio.sleep(60)


@client.event
async def on_ready():
    global window
    global keyboard
    keyboard = Controller()


@client.event
async def on_message(message):
    global next_work_timestamp
    global next_adventure_timestamp
    global next_farm_timestamp
    global next_training_timestamp
    global next_lootbox_timestamp
    global is_banned
    global is_solving_training
    global items
    global consumables
    global run
    message_content = emoji.demojize(message.content)
    embeds = message.embeds

    if "tdlf" in message_content:
        if message_content == "tdlf start" and message.author.name == "Vajicko":
            run = "yes"
            await game_runner()
            await message.channel.send(file=discord.File('start.gif'))
        if message_content == "tdlf end" and message.author.name == "Vajicko":
            run = "no"
            await message.channel.send(file=discord.File('end.gif'))
        if message_content == "tdlf tr" and message.author.name == "Vajicko":
            await type_command("i")
            await type_command("tr")
        if message_content == "tdlf ad" and message.author.name == "Vajicko":
            await type_command("heal")
            await type_command("adventure")
        if "help" in message_content:
            embedVar = discord.Embed(title="Možné tdlf helper commandy", description="", color=0x00ff00)
            embedVar.add_field(
                name="```tdlf start```",
                value="Pustí tu kurvu bota", inline=False)
            embedVar.add_field(
                name="```tdlf start```",
                value="Vypne tu kurvu bota", inline=False)
            embedVar.add_field(
                name="```tdlf tr```",
                value="Pustí automatický training", inline=False)
            embedVar.add_field(
                name="```tdlf ad```",
                value="Pustí adventure s healem", inline=False)
            embedVar.add_field(
                name="```tdlf craft ultra log use apple ruby banana epicfish goldenfish```\n"
                     "```tdlf craft ultra log```",
                value="Automaticky spustí commandy pro craft ULTRA logu, use je optional a definují se tam itemy, které se můžou vytradit nebo dismantlnout. Pokud se use nepoužije, je to jako by byly vypsané všechny itemy, takže se vytradí a dismantlí.",
                inline=False)
            await message.channel.send(embed=embedVar)
        if "craft" in message_content:
            craft_item = message_content.split("craft ", 1)[1].split(" use")[0]
            use = message_content.split("craft ", 1)[1].split("use ")[1]
            if craft_item == "ultra log":
                await type_command("i")
                if get_count_of_item_in_inventory("ruby") > 0 and "ruby" in use:
                    await type_command("trade e all")
                if get_count_of_item_in_inventory("banana") > 0 and "banana" in use:
                    await type_command("dismantle banana all")
                if get_count_of_item_in_inventory("epicfish") > 0 and "epicfish" in use:
                    await type_command("dismantle epic fish all")
                if get_count_of_item_in_inventory("goldenfish") > 0 and "goldenfish" in use:
                    await type_command("dismantle golden fish all")
                    await type_command("i")
                if get_count_of_item_in_inventory("apple") > 0 and "apple" in use:
                    await type_command("trade c all")
                    await type_command("i")
                if get_count_of_item_in_inventory("normiefish") > 0:
                    await type_command("trade a all")
                    await type_command("i")
                if get_count_of_item_in_inventory("woodenlog") > 24:
                    await type_command("craft epic log all")
                    await type_command("i")
                if get_count_of_item_in_inventory("epiclog") > 9:
                    await type_command("craft super log all")
                    await type_command("i")
                if get_count_of_item_in_inventory("superlog") > 9:
                    await type_command("craft mega log all")
                    await type_command("i")
                if get_count_of_item_in_inventory("megalog") > 9:
                    await type_command("craft hyper log all")
                    await type_command("i")
                if get_count_of_item_in_inventory("hyperlog") > 9:
                    await type_command("craft ultra log all")

    for embed in embeds:
        if config["username"] + "'s inventory" == embed.to_dict()["author"]["name"]:
            items = {}
            consumables = {}
            embed_text = embed.to_dict()
            for split_item in re.sub('<[^>]+>', '', embed_text["fields"][0]["value"].replace("**", "")).splitlines():
                item = split_item.split(":", 1)[0].strip().replace(" ", "").lower()
                count = split_item.split(":", 1)[1].strip().replace(",", "")
                items[item] = count

            for split_consumable in re.sub('<[^>]+>', '',
                                           embed_text["fields"][1]["value"].replace("**", "")).splitlines():
                consumable = split_consumable.split(":", 1)[0].strip().replace(" ", "").lower()
                count = split_consumable.split(":", 1)[1].strip().replace(",", "")
                consumables[consumable] = count

        if config["username"] + "'s cooldowns" == embed.to_dict()["author"]["name"]:
            embed_text = embed.to_dict()
            for ema in embed_text["fields"][0]["value"].splitlines():
                if "(" in ema and "Lootbox" in ema:
                    hours_seconds = (int(ema.split("(**", 1)[1].split("h", 1)[0])) * 60 * 60
                    seconds = (int(ema.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].split("h", 1)[1].replace(" ",
                                                                                                                    "")) + 1) * 60
                    total_seconds = hours_seconds + seconds
                    next_lootbox_timestamp = time.time() + total_seconds

            for em in embed_text["fields"][1]["value"].splitlines():
                if "(" in em and ("Training" in em or "Adventure" in em):
                    seconds = (int(em.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].replace(" ", "").replace("h",
                                                                                                                   "")) + 1) * 60
                    if "Training" in em:
                        next_training_timestamp = time.time() + seconds
                    if "Adventure" in em:
                        next_adventure_timestamp = time.time() + seconds

            for ems in embed_text["fields"][2]["value"].splitlines():
                if "(" in ems and ("Chop" in ems or "Farm" in ems):
                    seconds = (int(ems.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].replace(" ", "").replace("h",
                                                                                                                    "")) + 1) * 60
                    if "Chop" in ems:
                        next_work_timestamp = time.time() + seconds
                    if "Farm" in ems:
                        next_farm_timestamp = time.time() + seconds

    if is_epic_guard_message(message_content.lower()):
        channel = client.get_channel(979667826694582303)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await channel.send(current_time)
        await type_message(egs.solve_epic_guard(message))
        await press_enter()

    if is_jail_message(message_content.lower()):
        is_banned = True

    if is_training_task(message_content.lower()):
        is_solving_training = True
        await solve_training(message_content)


client.run(variables.discord_client)
