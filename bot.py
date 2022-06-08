import asyncio
import random
from pynput.keyboard import Controller
import time
import discord
import re
import emoji
import nest_asyncio
from datetime import datetime
import variables
from modules import training_solver, typer, epic_guard_solver, run_checker, inventory
import globals_

nest_asyncio.apply()

client = discord.Client()

random_work = ["drill"]


async def heal():
    if globals_.doheal:
        await typer.type_command("heal")


def is_training_task(message):
    if "is training" in message and variables.username.lower() in message:
        return True

    return False


def is_epic_guard_message(message):
    if "epic guard" in message and "485032715008212992" in message.lower():
        return True

    return False


def is_jail_message(message):
    if (
            "you are in the jail" in message or "is now in the jail" in message or "jail" in message) and variables.username.lower() in message.lower():
        return True

    return False


def farm_by_seed():
    if inventory.get_count_of_consumables_in_inventory("carrotseed") > 0:
        return "carrot"
    if inventory.get_count_of_consumables_in_inventory("breadseed") > 0:
        return "bread"
    if inventory.get_count_of_consumables_in_inventory("potatoseed") > 0:
        return "potato"
    return "basic"


async def game_runner():
    while True:
        if globals_.is_solving_training:
            continue

        time_now = time.time()
        if globals_.run:
            await heal()
            await typer.type_command("hunt")
            await typer.type_command("cd")

            if time_now > globals_.next_work_timestamp:
                await typer.type_command(random.choice(random_work))
                globals_.next_work_timestamp = time.time() + 300

            if time_now > globals_.next_lootbox_timestamp:
                await typer.type_command("withdraw 421k")
                await typer.type_command("buy edgy lootbox")
                globals_.next_lootbox_timestamp = time.time() + 10800

            if time_now > globals_.next_epic_quest_timestamp:
                await typer.type_command("heal")
                await typer.type_command("epic quest")
                await typer.type_message("15")
                await typer.press_enter()
                globals_.next_epic_quest_timestamp = time.time() + 21600

            if time_now > globals_.next_adventure_timestamp:
                await heal()
                await typer.type_command("adventure")
                globals_.next_adventure_timestamp = time.time() + 3600

            if time_now > globals_.next_farm_timestamp:
                await typer.type_command("i")
                await typer.type_command("farm " + farm_by_seed())
                globals_.next_farm_timestamp = time.time() + 600

            if time_now > globals_.next_training_timestamp:
                globals_.is_solving_training = True
                await typer.type_command("i")
                await typer.type_command("tr")
                globals_.next_training_timestamp = time.time() + 900

        await asyncio.sleep(60)


@client.event
async def on_ready():
    globals_.keyboard = Controller()
    await game_runner()


@client.event
async def on_message(message):
    message_content = emoji.demojize(message.content)
    embeds = message.embeds
    if "tdlf" in message_content:
        if message_content == "tdlf start" and message.author.id == variables.user_id:
            globals_.run = True
            embedVar = discord.Embed(title="Start bota proběhne do minuty",
                                     description="Pro ukončení napiš ```tdlf end```", color=0x00ff00)
            await message.channel.send(embed=embedVar)

        if message_content == "tdlf cons" and message.author.id == variables.user_id:
            await typer.type_command("i")
            embedVar = discord.Embed(title="Consumables", description=globals_.consumables, color=0x00ff00)
            await message.channel.send(embed=embedVar)

        if message_content == "tdlf i" and message.author.id == variables.user_id:
            await typer.type_command("i")
            embedVar = discord.Embed(title="Items", description=globals_.items, color=0x00ff00)
            await message.channel.send(embed=embedVar)

        if message_content == "tdlf open lb" and message.author.id == variables.user_id:
            await typer.type_command("open edgy lootbox all")
            await typer.type_command("open epic lootbox all")
            await typer.type_command("open rare lootbox all")
            await typer.type_command("open uncommon lootbox all")
            await typer.type_command("open common lootbox all")

        if message_content == "tdlf end" and message.author.id == variables.user_id:
            globals_.run = False
            embedVar = discord.Embed(title="Bot končí", description="Možná ještě projede posledních pár commandů",
                                     color=0x00ff00)
            await message.channel.send(embed=embedVar)

        if message_content == "tdlf tr" and message.author.id == variables.user_id:
            await typer.type_command("i")
            await typer.type_command("tr")

        if message_content == "tdlf farm" and message.author.id == variables.user_id:
            await typer.type_command("i")
            await typer.type_command("farm " + farm_by_seed())

        if message_content == "tdlf ad" and message.author.id == variables.user_id:
            await typer.type_command("heal")
            await typer.type_command("adventure")

        if "help" in message_content:
            embedVar = discord.Embed(title="Možné tdlf helper commandy", description="", color=0x00ff00)
            embedVar.add_field(
                name="```tdlf start```",
                value="Pustí tu kurvu bota", inline=False)
            embedVar.add_field(
                name="```tdlf end```",
                value="Vypne tu kurvu bota", inline=False)
            embedVar.add_field(
                name="```tdlf tr```",
                value="Pustí automatický training", inline=False)
            embedVar.add_field(
                name="```tdlf farm```",
                value="Zandá rpg farm podle seedu co máš v inventáři", inline=False)
            embedVar.add_field(
                name="```tdlf ad```",
                value="Pustí adventure s healem", inline=False)
            embedVar.add_field(
                name="```tdlf open lb```",
                value="Otevře všechny lootboxy", inline=False)
            embedVar.add_field(
                name="```tdlf cons```",
                value="Json consumables", inline=False)
            embedVar.add_field(
                name="```tdlf i```",
                value="Json items", inline=False)
            embedVar.add_field(
                name="```tdlf craft ultra log use apple ruby banana epicfish goldenfish```\n"
                     "```tdlf craft ultra log```",
                value="Automaticky spustí commandy pro craft ULTRA logu, use je optional a definují se tam itemy, které se můžou vytradit nebo dismantlnout. Pokud se use nepoužije, je to jako by byly vypsané všechny itemy, takže se vytradí a dismantlí.",
                inline=False)
            await message.channel.send(embed=embedVar)
        if "craft" in message_content and message.author.id == variables.user_id:
            craft_item = message_content.split("craft ", 1)[1].split(" use")[0]
            use = message_content.split("craft ", 1)[1].split("use ")[1]
            if craft_item == "ultra log":
                await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("ruby") > 0 and "ruby" in use:
                    await typer.type_command("trade e all")
                if inventory.get_count_of_item_in_inventory("banana") > 0 and "banana" in use:
                    await typer.type_command("dismantle banana all")
                if inventory.get_count_of_item_in_inventory("epicfish") > 0 and "epicfish" in use:
                    await typer.type_command("dismantle epic fish all")
                if inventory.get_count_of_item_in_inventory("goldenfish") > 0 and "goldenfish" in use:
                    await typer.type_command("dismantle golden fish all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("apple") > 0 and "apple" in use:
                    await typer.type_command("trade c all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("normiefish") > 0:
                    await typer.type_command("trade a all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("woodenlog") > 24:
                    await typer.type_command("craft epic log all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("epiclog") > 9:
                    await typer.type_command("craft super log all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("superlog") > 9:
                    await typer.type_command("craft mega log all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("megalog") > 9:
                    await typer.type_command("craft hyper log all")
                    await typer.type_command("i")
                if inventory.get_count_of_item_in_inventory("hyperlog") > 9:
                    await typer.type_command("craft ultra log all")

    for embed in embeds:
        print(embed.to_dict())
        if variables.username + "'s inventory" == embed.to_dict()["author"]["name"]:
            embed_text = embed.to_dict()
            for split_item in re.sub('<[^>]+>', '', embed_text["fields"][0]["value"].replace("**", "")).splitlines():
                item = split_item.split(":", 1)[0].strip().replace(" ", "").lower()
                count = split_item.split(":", 1)[1].strip().replace(",", "")
                globals_.items[item] = count

            for split_consumable in re.sub('<[^>]+>', '',
                                           embed_text["fields"][1]["value"].replace("**", "")).splitlines():
                consumable = split_consumable.split(":", 1)[0].strip().replace(" ", "").lower()
                count = split_consumable.split(":", 1)[1].strip().replace(",", "")
                globals_.consumables[consumable] = count

        if variables.username + "'s cooldowns" == embed.to_dict()["author"]["name"]:
            embed_text = embed.to_dict()
            for ema in embed_text["fields"][0]["value"].splitlines():
                if "(" in ema and "Lootbox" in ema:
                    hours_seconds = (int(ema.split("(**", 1)[1].split("h", 1)[0])) * 60 * 60
                    seconds = (int(ema.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].split("h", 1)[1].replace(" ",
                                                                                                                    "")) + 1) * 60
                    total_seconds = hours_seconds + seconds
                    globals_.next_lootbox_timestamp = time.time() + total_seconds

            for em in embed_text["fields"][1]["value"].splitlines():
                if "(" in em and ("Training" in em or "Adventure" in em):
                    seconds = (int(em.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].replace(" ", "").replace("h",
                                                                                                                   "")) + 1) * 60
                    if "Training" in em:
                        globals_.next_training_timestamp = time.time() + seconds
                    if "Adventure" in em:
                        globals_.next_adventure_timestamp = time.time() + seconds

            for ems in embed_text["fields"][2]["value"].splitlines():
                if "(" in ems and ("Chop" in ems or "Farm" in ems):
                    seconds = (int(ems.split("(", 1)[1].split("**", 1)[1].split("m", 1)[0].replace(" ", "").replace("h",
                                                                                                                    "")) + 1) * 60
                    if "Chop" in ems:
                        globals_.next_work_timestamp = time.time() + seconds
                    if "Farm" in ems:
                        globals_.next_farm_timestamp = time.time() + seconds

    if is_epic_guard_message(message_content.lower()):
        channel = client.get_channel(979667826694582303)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await channel.send(variables.username + " triggered epic guard at " + current_time)
        await typer.type_message(epic_guard_solver.solve_epic_guard(message))
        await typer.press_enter()

    if is_jail_message(message_content.lower()):
        globals_.run = False
        globals_.is_banned = True

    if is_training_task(message_content.lower()):
        globals_.is_solving_training = True
        await training_solver.solve_training(message_content)


client.run(variables.discord_client)
