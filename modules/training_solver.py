from constants import guess_task_constants
from modules import typer, inventory
import globals_


def which_fish(fish):
    transcribes = {
        "normiefish": 1,
        "goldenfish": 2,
        "epicfish": 3
    }

    return transcribes.get(fish)


def get_training_task(training_task_text):
    training_task_text = training_task_text.lower()

    if "how many" in training_task_text:
        return guess_task_constants.NUMBER_GUESS_TASK
    elif "what is the name" in training_task_text:
        return guess_task_constants.NAME_GUESS_TASK
    elif "is this a" in training_task_text:
        return guess_task_constants.EMOJI_GUESS_TASK
    elif "answer with a letter" in training_task_text:
        return guess_task_constants.LETTER_GUESS_TASK
    elif "do you have more" in training_task_text:
        return guess_task_constants.INVENTORY_COUNT_GUESS_TASK


def base_emoji_to_epic_rpg_name(basic_emoji_name):
    basic_emoji_name = basic_emoji_name.lower()
    basic_emoji_transcribes = {
        "gem stone": "diamond",
        "wrapped gift": "gift",
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


async def solve_training(training_task_text):
    task_type = get_training_task(training_task_text)
    task_text_lines = training_task_text.splitlines()
    answer = "No idea"

    if task_type is guess_task_constants.NUMBER_GUESS_TASK:
        emoji_to_search = task_text_lines[2].split(":", 1)[1].split(":", 1)[0].replace(":", "").strip().lower().replace(
            "_", " ")
        total_emoji_count = task_text_lines[1].lower().count(emoji_to_search)
        answer = str(total_emoji_count)

    elif task_type is guess_task_constants.NAME_GUESS_TASK:
        fish = task_text_lines[1].lower().split(":", 1)[1].split(":", 1)[0]
        answer = str(which_fish(fish))

    elif task_type is guess_task_constants.EMOJI_GUESS_TASK:
        answer = "no"
        real_emoji_name = base_emoji_to_epic_rpg_name(
            task_text_lines[1].split("?", 1)[1].strip().replace(":", "").replace("_", " "))
        given_emoji_name = task_text_lines[1].split("a", 1)[1].split("?")[0].strip().lower().replace("_", " ")
        if given_emoji_name == real_emoji_name:
            answer = "yes"

    elif task_type is guess_task_constants.LETTER_GUESS_TASK:
        word = task_text_lines[1].split(":", 1)[1].split(":", 1)[0].lower()
        position = task_text_lines[1].split("the", 1)[1].split("letter", 1)[0].strip().lower().replace("*", "")
        answer = str(letter_of_position(word, position))

    elif task_type is guess_task_constants.INVENTORY_COUNT_GUESS_TASK:
        answer = "no"
        expected_count = int(
            task_text_lines[1].split("than", 1)[1].split(":", 1)[0].replace("<", "").replace(" ", "").strip())
        current_count = inventory.get_count_of_item_in_inventory("ruby")
        if current_count > expected_count:
            answer = "yes"

    await typer.type_message(answer)
    await typer.press_enter()
    globals_.is_solving_training = False