import os
import random
import PySimpleGUI as sg

class Survivor:
    def __init__(self, name, perks):
        self.name = name
        self.perks = perks

class Killer:
    def __init__(self, name, power, perks):
        self.name = name
        self.power = power
        self.perks = perks

class Fonts:
    MEDIUM = ("Roboto-Light", 12)
    MEDIUM_BOLD = ("Roboto-Light", 12, "bold")
    MEDIUM = ("Roboto-Light", 18)
    MEDIUM_BOLD = ("Roboto-Light", 18, "bold")
    BIG = ("Roboto-Light", 24)
    BIG_BOLD = ("Roboto-Light", 24, "bold")

def remove_special_characters(string):
    characters_to_remove = [":", "*", "?", '"', "<", ">", "|", "/", "\\"]
    for char in characters_to_remove:
        string = string.replace(char, "")
    return string

def refresh_main_window():
    main_random_survivor = random.choice(main_selected_survivors)
    main_survivor_image = os.path.join(os.path.dirname(__file__), "Assets\\Survivors\\" + remove_special_characters(main_random_survivor) + ".png")
    window["main_survivor_image"].update(filename = main_survivor_image)
    main_random_killer = random.choice(main_selected_killers)
    main_killer_image = os.path.join(os.path.dirname(__file__), "Assets\\Killers\\" + remove_special_characters(main_random_killer) + ".png")
    window["main_killer_image"].update(filename = main_killer_image)

def create_main_settings_window():
    layout = [
        [sg.Button("Back", font = Fonts.MEDIUM), sg.Button("Refresh", font = Fonts.MEDIUM)],
        [sg.Stretch(), sg.Text("Main Menu Settings", font = Fonts.MEDIUM), sg.Stretch()],
        [sg.Stretch(), sg.Column([
            [sg.Stretch(), sg.Frame(" Main Menu Survivors ", font = Fonts.MEDIUM, title_location = "n", layout = [
                [sg.Stretch(), sg.Column([
                    [sg.Checkbox(survivor.name, key = survivor.name, default = (survivor.name in main_selected_survivors), font = Fonts.MEDIUM)] for survivor in survivors
                ], scrollable=True, vertical_scroll_only=True, size = (300, 700)), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check All", key = "check_all_survivors", font = Fonts.MEDIUM), sg.Button("Uncheck All", key = "uncheck_all_survivors", font = Fonts.MEDIUM), sg.Stretch()]
            ]), sg.Stretch()],
        ]), sg.Stretch(), sg.Column([
            [sg.Stretch(), sg.Frame(" Main Menu Killers ", font = Fonts.MEDIUM, title_location = "n", layout = [
                [sg.Stretch(), sg.Column([
                    [sg.Checkbox(killer.name, key = killer.name, default = (killer.name in main_selected_killers), font = Fonts.MEDIUM)] for killer in killers
                ], scrollable=True, vertical_scroll_only=True, size = (300, 700)), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check All", key = "check_all_killers", font = Fonts.MEDIUM), sg.Button("Uncheck All", key = "uncheck_all_killers", font = Fonts.MEDIUM), sg.Stretch()]
            ]), sg.Stretch()],
        ]), sg.Stretch()]
    ]
    window = sg.Window("General Settings", layout, resizable = True, finalize = True, enable_close_attempted_event = True)
    window.maximize()
    while True:
        event, values = window.read()
        match event:
            case "check_all_survivors":
                for survivor in survivors:
                    window[survivor.name].update(value = True)
            case "uncheck_all_survivors":
                for survivor in survivors:
                    window[survivor.name].update(value = False)
            case "check_all_killers":
                for killer in killers:
                    window[killer.name].update(value = True)
            case "uncheck_all_killers":
                for killer in killers:
                    window[killer.name].update(value = False)
            case "Refresh" | "Back" | sg.WIN_CLOSE_ATTEMPTED_EVENT:
                for survivor in survivors:
                    if values[survivor.name] == True and survivor.name not in main_selected_survivors:
                        main_selected_survivors.append(survivor.name)
                    elif values[survivor.name] == False and survivor.name in main_selected_survivors:
                        main_selected_survivors.remove(survivor.name)
                for killer in killers:
                    if values[killer.name] == True and killer.name not in main_selected_killers:
                        main_selected_killers.append(killer.name)
                    elif values[killer.name] == False and killer.name in main_selected_killers:
                        main_selected_killers.remove(killer.name)
                if not main_selected_survivors:
                    main_selected_survivors.append(survivors[0].name)
                if not main_selected_killers:
                    main_selected_killers.append(killers[0].name)
                with open(os.path.join(os.path.dirname(__file__), "Settings\\Main Menu.txt"), "w", encoding = "utf-8") as file:
                    for survivor in main_selected_survivors:
                        file.write(f"{str(survivor)}\n")
                    file.write("\n")
                    for killer in main_selected_killers:
                        file.write(f"{str(killer)}\n")
                if event == "Refresh":
                    refresh_main_window()
                else:
                    break
    window.close()

def create_killer_window():
    global no_repeating_killers, no_repeating_killer_perks
    layout = [
        [sg.Button("Back", font = Fonts.MEDIUM), sg.Button("Settings", font = Fonts.MEDIUM), sg.Stretch(), sg.Button("Randomize", font = Fonts.MEDIUM)],
        [sg.Column([
            [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown Character.png"), key = "killer_image"), sg.Stretch()],
            [sg.Stretch(), sg.Text("", key = "killer", font = Fonts.BIG), sg.Stretch()]
        ]), sg.Column([
            [sg.Column([
                [sg.Stretch(), sg.Text("", key = "spacing", font = Fonts.BIG), sg.Stretch()],
                [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown.png"), key = "power_image"), sg.Stretch()],
                [sg.Stretch(), sg.Text("", key = "power", font = Fonts.BIG), sg.Stretch()]
            ]), sg.Column([
                [sg.Stretch(), sg.Text("Add-ons", font = Fonts.BIG_BOLD), sg.Stretch()],
                [sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown.png"), key = "addon_0_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "addon_0", font = Fonts.BIG), sg.Stretch()]
                ]), sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown.png"), key = "addon_1_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "addon_1", font = Fonts.BIG), sg.Stretch()]
                ]), sg.Stretch()]
            ])],
            [sg.VStretch()],
            [sg.Stretch(), sg.Column([
                [sg.Stretch(), sg.Text("Perks", font = Fonts.BIG_BOLD), sg.Stretch()],
                [sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown Perk.png"), key = "perk_0_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "perk_0", font = Fonts.BIG, justification="center"), sg.Stretch()]
                ]), sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown Perk.png"), key = "perk_1_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "perk_1", font = Fonts.BIG, justification="center"), sg.Stretch()]
                ]), sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown Perk.png"), key = "perk_2_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "perk_2", font = Fonts.BIG, justification="center"), sg.Stretch()]
                ]), sg.Stretch(), sg.Column([
                    [sg.Stretch(), sg.Image(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\Unknown Perk.png"), key = "perk_3_image"), sg.Stretch()],
                    [sg.Stretch(), sg.Text("", key = "perk_3", font = Fonts.BIG, justification="center"), sg.Stretch()]
                ]), sg.Stretch()]
            ]), sg.Stretch()]
        ])]
    ]
    window = sg.Window("Killer Randomizer", layout, resizable = True, finalize = True)
    window.maximize()
    while True:
        event, values = window.read()
        match event:
            case "Randomize":
                random_killer = random.choice(selected_killers)
                random_perks = random.sample(selected_killer_perks, 4)
                addon_indexes = []
                for rarity in selected_killer_addons:
                    match rarity:
                        case "Common":
                            addon_indexes += [0, 1, 2, 3]
                        case "Uncommon":
                            addon_indexes += [4, 5, 6, 7, 8]
                        case "Rare":
                            addon_indexes += [9, 10, 11, 12, 13]
                        case "Very Rare":
                            addon_indexes += [14, 15, 16, 17]
                        case "Ultra Rare":
                            addon_indexes += [18, 19]
                for killer in killers:
                    if killer.name == random_killer:
                        power = killer.power
                        break
                with open(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + power + ".txt"), "r", encoding = "utf-8") as file:
                    addons = file.readlines()
                addons = [item.strip() for item in addons]
                random_addons = random.sample(addon_indexes, 2)
                random_addons = [addons[index] for index in random_addons]
                if no_repeating_killers == True:
                    selected_killers.remove(random_killer)
                if no_repeating_killer_perks == True:
                    for perk in random_perks:
                        selected_killer_perks.remove(perk)
                window["killer"].update(random_killer)
                window["killer_image"].update(filename = os.path.join(os.path.dirname(__file__), "Assets\\Killers\\" + remove_special_characters(random_killer) + ".png"))
                window["power"].update(power)
                window["power_image"].update(filename = os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + ".png"))
                for i in range(len(random_addons)):
                    window["addon_" + str(i)].update(random_addons[i])
                    window["addon_" + str(i) + "_image"].update(filename = os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + power + "\\" + remove_special_characters(random_addons[i]) + ".png"))
                for i in range(len(random_perks)):
                    if ":" in random_perks[i]:
                        window["perk_" + str(i)].update(random_perks[i].replace(": ", ":\n"))
                    else:
                        window["perk_" + str(i)].update(random_perks[i] + "\n")
                    image_path = os.path.join(os.path.dirname(__file__), "Assets\\Killer Perks\\" + remove_special_characters(random_perks[i]) + ".png")
                    if os.path.exists(image_path):
                        window["perk_" + str(i) + "_image"].update(filename = image_path)
                    else:
                        window["perk_" + str(i) + "_image"].update(filename = os.path.join(os.path.dirname(__file__), "Assets\\General Killer Perks\\" + remove_special_characters(random_perks[i]) + ".png"))
            case "Settings":
                window.hide()
                create_killer_settings_window()
                window.un_hide()
                window.maximize()
            case "Back" | sg.WIN_CLOSED:
                with open(os.path.join(os.path.dirname(__file__), "Settings\\Killer.txt"), "w", encoding = "utf-8") as file:
                    if no_repeating_killers == True:
                        file.write("True" + "\n")
                    else:
                        file.write("False" + "\n")
                    if no_repeating_killer_perks == True:
                        file.write("True" + "\n")
                    else:
                        file.write("False" + "\n")
                    file.write("\n")
                    for killer in selected_killers:
                        file.write(f"{str(killer)}\n")
                    file.write("\n")
                    for perk in selected_killer_perks:
                        file.write(f"{str(perk)}\n")
                    file.write("\n")
                    for rarity in selected_killer_addons:
                        file.write(f"{str(rarity)}\n")
                break
    window.close()

def create_killer_settings_window():
    global no_repeating_killers
    global no_repeating_killer_perks
    layout = [
        [sg.Button("Back", font = Fonts.MEDIUM)],
        [sg.Stretch(), sg.Column([
            [sg.Stretch(), sg.Frame(" Random Killer Selection ", font = Fonts.BIG_BOLD, title_location = "n", layout = [
                [sg.Stretch(), sg.Column([
                    [sg.Checkbox(killer.name, key = killer.name, default = (killer.name in selected_killers), font = Fonts.MEDIUM), sg.Stretch()] for killer in killers
                ], scrollable=True, vertical_scroll_only=True, size = (300, 700)), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check All", key = "check_all_killers", font = Fonts.MEDIUM), sg.Button("Uncheck All", key = "uncheck_all_killers", font = Fonts.MEDIUM), sg.Stretch()],
                [sg.Stretch(), sg.Checkbox("No Repeating Killers", key = "no_repeating_killers", default = no_repeating_killers, font = Fonts.MEDIUM), sg.Stretch()]
            ]), sg.Stretch()]
        ]), sg.Stretch(), sg.Column([
            [sg.Stretch(), sg.Frame(" Random Perk Selection ", font = Fonts.BIG_BOLD, title_location = "n", layout = [
                [sg.Stretch(), sg.Column([
                    [sg.Checkbox(perk, key = perk, default = (perk in selected_killer_perks), font = Fonts.MEDIUM), sg.Stretch()] for perk in killer_perks
                ], scrollable=True, vertical_scroll_only=True, size = (400, 700)), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check All", key = "check_all_killer_perks", font = Fonts.MEDIUM), sg.Button("Uncheck All", key = "uncheck_all_killer_perks", font = Fonts.MEDIUM), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check General Perks", key = "check_general_killer_perks", font = Fonts.MEDIUM), sg.Stretch()],
                [sg.Stretch(), sg.Button("Check Perks of Checked Killers", key = "check_perks_of_checked_killers", font = Fonts.MEDIUM), sg.Stretch()],
                [sg.Stretch(), sg.Checkbox("No Repeating Perks", key = "no_repeating_killer_perks", default = no_repeating_killer_perks, font = Fonts.MEDIUM), sg.Stretch()]
            ]), sg.Stretch()]
        ]), sg.Stretch(), sg.Column([
                [sg.Stretch(), sg.Frame(" Random Add-on Selection ", font = Fonts.BIG_BOLD, title_location = "n", layout = [
                    [sg.Checkbox(rarity, key = rarity, default = (rarity in selected_killer_addons), font = Fonts.MEDIUM, text_color = addon_colors[addon_rarities.index(rarity)]), sg.Stretch()] for rarity in addon_rarities
                ]), sg.Stretch()],
        ]), sg.Stretch()]
    ]
    window = sg.Window("Killer Settings", layout, resizable = True, finalize = True, enable_close_attempted_event = True)
    window.maximize()
    while True:
        event, values = window.read()
        match event:
            case "check_all_killers":
                for killer in killers:
                    window[killer.name].update(value = True)
            case "uncheck_all_killers":
                for killer in killers:
                    window[killer.name].update(value = False)
            case "check_all_killer_perks":
                for perk in killer_perks:
                    window[perk].update(value = True)
            case "uncheck_all_killer_perks":
                for perk in killer_perks:
                    window[perk].update(value = False)
            case "check_perks_of_checked_killers":
                for killer in killers:
                    if values[killer.name] == True:
                        perks = killer.perks
                        for perk in perks:
                            window[perk].update(value = True)
            case "check_general_killer_perks":
                for perk in killer_perks:
                    if perk in general_killer_perks:
                        window[perk].update(value = True)
            case "Back" | sg.WIN_CLOSE_ATTEMPTED_EVENT:
                if values["no_repeating_killers"] == True:
                    no_repeating_killers = True
                else:
                    no_repeating_killers = False
                for killer in killers:
                    if values[killer.name] == True and killer.name not in selected_killers:
                        selected_killers.append(killer.name)
                    elif values[killer.name] == False and killer.name in selected_killers:
                        selected_killers.remove(killer.name)
                if values["no_repeating_killer_perks"] == True:
                    no_repeating_killer_perks = True
                else:
                    no_repeating_killer_perks = False
                for perk in killer_perks:
                    if values[perk] == True and perk not in selected_killer_perks:
                        selected_killer_perks.append(perk)
                    elif values[perk] == False and perk in selected_killer_perks:
                        selected_killer_perks.remove(perk)
                for rarity in addon_rarities:
                    if values[rarity] == True and rarity not in selected_killer_addons:
                        selected_killer_addons.append(rarity)
                    elif values[rarity] == False and rarity in selected_killer_addons:
                        selected_killer_addons.remove(rarity)
                break
    window.close()

sg.theme("DarkGrey13")
username = os.getlogin()
greeting_messages = [
    f"Hello, {username}!",
    f"Hi there, {username}!",
    f"Greetings, {username}!",
    f"Welcome, {username}!",
    f"Hey, {username}!",
    f"Good to see you, {username}!",
    f"Nice to see you, {username}!",
    f"Good day, {username}!",
    f"How's it going, {username}?",
    f"A warm welcome to you, {username}!",
    f"Nice to have you here, {username}!",
    f"Welcome aboard, {username}!",
    f"Great to have you, {username}!",
]
welcome_messages = [
    "Let's get started!",
    "Time to dive in!",
    "Get ready to roll!",
    "Ready for some action?",
    "Buckle up, we're starting!",
    "Let the fun begin!",
    "Step into a world of possibilities!",
    "It's time to shine!"
]
addon_rarities = ["Common", "Uncommon", "Rare", "Very Rare", "Ultra Rare"]
addon_colors = ["#ab713c", "#e8c252", "#199b1e", "#ac3ee3", "#ff0955"]

### Load killers ###
with open(os.path.join(os.path.dirname(__file__), "Assets\\Killers.txt"), "r", encoding = "utf-8") as file:
    raw_killers = file.readlines()
raw_killers = [item.strip() for item in raw_killers]
killers = []
for raw_killer in raw_killers:
    raw_killer = raw_killer.split("|")
    name = raw_killer[0]
    power = raw_killer[1]
    perks = [raw_killer[2], raw_killer[3], raw_killer[4]]
    killer = Killer(name, power, perks)
    killers.append(killer)

### Load survivors ###
with open(os.path.join(os.path.dirname(__file__), "Assets\\Survivors.txt"), "r", encoding = "utf-8") as file:
    raw_survivors = file.readlines()
raw_survivors = [item.strip() for item in raw_survivors]
survivors = []
for raw_survivor in raw_survivors:
    raw_survivor = raw_survivor.split("|")
    name = raw_survivor[0]
    perks = [raw_survivor[1], raw_survivor[2], raw_survivor[3]]
    survivor = Survivor(name, perks)
    survivors.append(survivor)

### Create perk lists ###
with open(os.path.join(os.path.dirname(__file__), "Assets\\General Killer Perks.txt"), "r", encoding = "utf-8") as file:
    general_killer_perks = file.readlines()
general_killer_perks = [item.strip() for item in general_killer_perks]
killer_perks = general_killer_perks.copy()
for killer in killers:
    killer_perks = killer_perks + killer.perks
killer_perks.sort()

with open(os.path.join(os.path.dirname(__file__), "Assets\\General Survivor Perks.txt"), "r", encoding = "utf-8") as file:
    general_survivor_perks = file.readlines()
general_survivor_perks = [item.strip() for item in general_survivor_perks]
survivor_perks = general_survivor_perks.copy()
for survivor in survivors:
    survivor_perks = survivor_perks + survivor.perks
survivor_perks.sort()

### General Settings ###
main_selected_survivors, main_selected_killers = [], []
if os.path.exists(os.path.join(os.path.dirname(__file__), "Settings\\Main Menu.txt")):
    with open(os.path.join(os.path.dirname(__file__), "Settings\\Main Menu.txt"), "r", encoding = "utf-8") as file:
        main_selected_characters = file.readlines()
    main_selected_characters = [item.strip() for item in main_selected_characters]
    for character in main_selected_characters:
        if character == "":
            break
        main_selected_survivors.append(character)
    for character in main_selected_characters[len(main_selected_survivors) + 1:]:
        main_selected_killers.append(character)
else:
    with open(os.path.join(os.path.dirname(__file__), "Settings\\Main Menu.txt"), "w", encoding = "utf-8") as file:
        for survivor in survivors:
            main_selected_survivors.append(survivor.name)
            file.write(survivor.name + "\n")
        file.write("\n")
        for killer in killers:
            main_selected_killers.append(killer.name)
            file.write(killer.name + "\n")
main_random_survivor = random.choice(main_selected_survivors)
main_survivor_image = os.path.join(os.path.dirname(__file__), "Assets\\Survivors\\" + remove_special_characters(main_random_survivor) + ".png")
main_random_killer = random.choice(main_selected_killers)
main_killer_image = os.path.join(os.path.dirname(__file__), "Assets\\Killers\\" + remove_special_characters(main_random_killer) + ".png")

### Killer Settings ###
# No Repeating Killers / No Repeating Perks
# Bez powtarzania killerów / Bez powtarzania perków
selected_killers, selected_killer_perks, selected_killer_addons = [], [], []
if os.path.exists(os.path.join(os.path.dirname(__file__), "Settings\\Killer.txt")):
    with open(os.path.join(os.path.dirname(__file__), "Settings\\Killer.txt"), "r", encoding = "utf-8") as file:
        killer_settings_raw = file.readlines()
    killer_settings_raw = [item.strip() for item in killer_settings_raw]
    if killer_settings_raw[0] == "True":
        no_repeating_killers = True
    else:
        no_repeating_killers = False
    if killer_settings_raw[1] == "True":
        no_repeating_killer_perks = True
    else:
        no_repeating_killer_perks = False
    for setting in killer_settings_raw[3:]:
        if setting == "":
            break
        selected_killers.append(setting)
    for setting in killer_settings_raw[len(selected_killers) + 4:]:
        if setting == "":
            break
        selected_killer_perks.append(setting)
    for setting in killer_settings_raw[len(selected_killers) + len(selected_killer_perks) + 5:]:
        selected_killer_addons.append(setting)
else:
    with open(os.path.join(os.path.dirname(__file__), "Settings\\Killer.txt"), "w", encoding = "utf-8") as file:
        file.write("False" + "\n" + "False" + "\n" + "\n")
        for killer in killers:
            file.write(killer.name + "\n")
        file.write("\n")
        for perk in killer_perks:
            file.write(perk + "\n")
        file.write("\n")
        for rarity in addon_rarities:
            file.write(rarity + "\n")
    no_repeating_killers = False
    no_repeating_killer_perks = False
    selected_killers = [killer.name for killer in killers]
    selected_killer_perks = killer_perks.copy()
    selected_killer_addons = addon_rarities.copy()

### Create main GUI window ###
layout = [
    [sg.VStretch()],
    [sg.Stretch(), sg.Text(random.choice(greeting_messages), font = Fonts.BIG), sg.Stretch()],
    [sg.Stretch(), sg.Text(random.choice(welcome_messages), font = Fonts.MEDIUM), sg.Stretch()],
    [sg.Stretch(), sg.Column([
        [sg.Stretch(), sg.Image(filename = main_survivor_image, key = "main_survivor_image"), sg.Stretch()],
        [sg.Stretch(), sg.Button("Play Survivor", font = Fonts.MEDIUM), sg.Stretch()]
    ]), sg.Stretch(), sg.Column([
        [sg.Stretch(), sg.Image(filename = main_killer_image, key = "main_killer_image"), sg.Stretch()],
        [sg.Stretch(), sg.Button("Play Killer", font = Fonts.MEDIUM), sg.Stretch()]
    ]), sg.Stretch()],
    [sg.VStretch()],
    [sg.Button("Settings", font = Fonts.MEDIUM), sg.Stretch(), sg.Button("Exit", font = Fonts.MEDIUM)]
]
window = sg.Window("Dead by Daylight Randomizer", layout, resizable = True, finalize = True)
window.maximize()
while True:
    event, values = window.read()
    match event:
        case "Settings":
            window.hide()
            create_main_settings_window()
            window.un_hide()
            window.maximize()
        case "Play Killer":
            window.hide()
            create_killer_window()
            window.un_hide()
            window.maximize()
        case "Exit" | sg.WIN_CLOSED:
            break
window.close()