import asyncio
from modules import run_checker

from pynput.keyboard import Key

import globals_


def split(words):
    return [char for char in words]


async def type_message(message):
    for i in split(message):
        if globals_.window is not None:
            globals_.window.send_keystrokes(i)


async def press_enter():
    if globals_.window is not None:
        globals_.window.send_keystrokes("{ENTER}")
    await asyncio.sleep(1.9)


async def type_command(command):
    if run_checker.check_ban_status():
        run_checker.die()
    await type_message("rpg " + command)
    await press_enter()
