import time

global keyboard
keyboard = None
global is_banned
is_banned = False
global is_solving_training
is_solving_training = False
global items
items = {}
global consumables
consumables = {}
global run
run = False
global doheal
doheal = False
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
