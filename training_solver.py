import guess_task_constants


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
