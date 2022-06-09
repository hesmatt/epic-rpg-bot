import time

global doheal
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
global epic_guard_answer

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
epic_guard_answer = "Tvoje mamka"  # Default epic guard answer if !solved
run = False  # set to True to run automatic tdlf bot on start
doheal = False  # set to True to use healing during automatic run
