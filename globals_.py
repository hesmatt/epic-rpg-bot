import time
import pywinauto

global do_heal
global run
global keyboard
global items
global consumables
global is_banned
global is_solving_training
global next_work_timestamp
global next_adventure_timestamp
global next_farm_timestamp
global next_training_timestamp
global next_lootbox_timestamp
global next_epic_quest_timestamp

next_training_timestamp = time.time()
next_lootbox_timestamp = time.time()
next_epic_quest_timestamp = time.time()
next_farm_timestamp = time.time()
next_work_timestamp = time.time()
next_adventure_timestamp = time.time()
keyboard = None
is_banned = False
is_solving_training = False
items = {}
consumables = {}
run = True  # set to True to run automatic tdlf bot on start
do_heal = False  # set to True to use healing during automatic run
window = pywinauto.Application().connect(title="🦊matoo-rpg - Discord", timeout=5000).window(
    title="🦊matoo-rpg - Discord")
