import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from PIL import Image
from io import BytesIO
import subprocess

class ConsoleColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class Survivor:
    def __init__(self, name, perks):
        self.name = name
        self.perks = perks

class Killer:
    def __init__(self, name, power, perks):
        self.name = name
        self.power = power
        self.perks = perks

def log_message(message, color, is_bold=False):
    if is_bold:
        print(color + ConsoleColors.BOLD + message + ConsoleColors.ENDC)
    else:
        print(color + message + ConsoleColors.ENDC)

def souper(input):
    url = "https://deadbydaylight.fandom.com" + input
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def remove_special_characters(string):
    characters_to_remove = [":", "*", "?", '"', "<", ">", "|", "/", "\\"]
    for char in characters_to_remove:
        string = string.replace(char, "")
    return string

def download_and_resize_image(url, name, target_size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(target_size)
    img.save(name)

# def download_gif_to_png(url, save_path):
#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     img.seek(img.n_frames - 1)
#     img.save(save_path)

log_message(">>> Starting Update <<<", ConsoleColors.HEADER, is_bold=True)

log_message("Step 1: Creating folders...", ConsoleColors.OKBLUE)
try:
    folder_creation = False
    main_folders = ["Assets", "Settings"]
    for folder in main_folders:
        if os.path.exists(os.path.join(os.path.dirname(__file__), folder)) == False:
            os.makedirs(os.path.join(os.path.dirname(__file__), folder))
            folder_creation = True
    sub_folders = ["Killers", "Powers", "Killer Perks", "General Killer Perks", "Survivors", "Items", "Survivor Perks", "General Survivor Perks", "General Images"]
    for folder in sub_folders:
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Assets\\" + folder)) == False:
            os.makedirs(os.path.join(os.path.dirname(__file__), "Assets\\" + folder))
            folder_creation = True
    if folder_creation == True:
        log_message("Step 1: Folders created", ConsoleColors.OKGREEN)
    else:
        log_message("Step 1: Folders already exist", ConsoleColors.OKGREEN)
except Exception as e:
    log_message("Step 1: " + str(e), ConsoleColors.FAIL)

log_message("Step 2: Downloading general images...", ConsoleColors.OKBLUE)
try:
    directory = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\")
    download_and_resize_image("https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/ef/UnknownKiller_charPreview_portrait.png/revision/latest?cb=20210911183012", directory + "Unknown Character.png", (512, 512))
    download_and_resize_image("https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/5a/IconPerks_hiddenPerk.png/revision/latest?cb=20231014113930", directory + "Unknown Perk.png", (256, 256))
    download_and_resize_image("https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/e5/Unknown_QuestionMark.png/revision/latest?cb=20210929093312", directory + "Unknown.png", (256, 256))
    program_to_run = os.path.join(os.path.dirname(__file__), "Rarity Images.py")
    result = subprocess.run(['python', program_to_run], capture_output=True, text=True)
    subprocess_output = result.stdout.strip()
    log_message("Step 2: " + str(3 + int(subprocess_output)) + " general images downloaded", ConsoleColors.OKGREEN)
except Exception as e:
    log_message("Step 2: " + str(e), ConsoleColors.FAIL)

log_message("Step 3: Collecting killer data...", ConsoleColors.OKBLUE)
try:
    soup = souper("/wiki/Killers")
    target_divs = soup.find_all("div", style="display: inline-block; text-align:center; margin: 10px")
    a_list, killer_titles, killers = [], [], []
    for div in target_divs:
        a_elements = div.find_all("a")
        title = div.get_text()
        title = "The " + title.split(" - ")[1]
        killer_titles.append(title)
        for a in a_elements:
            a_list.append(a)
    a_list = a_list[::2]
    for a in a_list:
        soup = souper(a["href"])
        span_list = soup.find_all("span", class_ = "mw-headline", id = True)
        for span in span_list:
            span = span.get_text()
            if span.startswith("Power: "):
                power = span.replace("Power: ", "")
                power_id = span.replace(" ", "_")
                break
        image_link = soup.find("span", id = power_id).find_parent().find_next_sibling("div", class_ = "floatright").find_next()["href"]
        urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + ".png"))
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power))) == False:
            os.makedirs(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power)))
        addons = []
        wikitable = soup.find("span", id = "Add-ons_for" + power_id.replace("Power:", "")).find_parent().find_next_sibling()
        table_rows = wikitable.find_all("tr")
        addon_index = 0
        for row in table_rows:
            try:
                table_header = row.find_all("th")[1]
                addon = table_header.find("a")["title"].replace(f" ({power})", "")
                addons.append(addon)
                table_header_image = row.find_all("th")[0]
                image_link = table_header_image.find("a").find_next()["data-src"]
                urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + "\\" + remove_special_characters(addon) + ".png"))
                match addon_index:
                    case 0 | 1 | 2 | 3:
                        rarity = "Common"
                    case 4 | 5 | 6 | 7 | 8:
                        rarity = "Uncommon"
                    case 9 | 10 | 11 | 12 | 13:
                        rarity = "Rare"
                    case 14 | 15 | 16 | 17:
                        rarity = "Very Rare"
                    case 18 | 19:
                        rarity = "Ultra Rare"
                addon_index += 1
                background_image_directory = os.path.join(os.path.dirname(__file__), "Assets\\General Images\\")
                background_image = Image.open(f"{background_image_directory}{rarity}.png")
                foreground_image = Image.open(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + "\\" + remove_special_characters(addon) + ".png"))
                result_image = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
                result_image.paste(background_image, (0, 0))
                result_image.paste(foreground_image, (22, 22, 278, 278), foreground_image)
                result_image.save(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + "\\" + remove_special_characters(addon) + ".png"))
            except TypeError:
                pass
        with open(os.path.join(os.path.dirname(__file__), "Assets\\Powers\\" + remove_special_characters(power) + ".txt"), "w", encoding="utf-8") as file:
            for addon in addons:
                file.write(addon + "\n")
        perks = []
        wikitable = soup.find("table", class_ = "wikitable")
        table_rows = wikitable.find_all("tr")
        for row in table_rows:
            table_header = row.find_all("th")[1]
            perk = table_header.find("a")["title"]
            perks.append(perk)
            table_header_image = row.find_all("th")[0]
            image_link = table_header_image.find("a").find_next()["data-src"]
            #download_gif_to_png(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Killer Perks\\" + remove_special_characters(perk) + ".png"))
            urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Killer Perks\\" + remove_special_characters(perk) + ".png"))
        killer = Killer(killer_titles[a_list.index(a)], power, perks)
        killers.append(killer)
    with open(os.path.join(os.path.dirname(__file__), "Assets\\Killers.txt"), "w", encoding="utf-8") as file:
        for killer in killers:
            file.write(killer.name + "|" + killer.power + "|" + killer.perks[0] + "|" + killer.perks[1] + "|" + killer.perks[2] + "\n")
    for i in range(1, len(killers) + 1):
        try:
            image_link = soup.find("img", alt = "K" + f"{i:02}" + " charSelect portrait")["data-src"]
        except KeyError:
            image_link = soup.find("img", alt = "K" + f"{i:02}" + " charSelect portrait")["src"]
        scale_index = image_link.find("/scale")
        question_mark_index = image_link.find("?", scale_index)
        image_link = image_link[:scale_index] + image_link[question_mark_index:]
        urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Killers\\" + remove_special_characters(killers[i - 1].name) + ".png"))
    log_message("Step 3: Data of " + str(len(killers)) + " killers collected", ConsoleColors.OKGREEN)
except Exception as e:
    log_message("Step 3: " + str(e), ConsoleColors.FAIL)

log_message("Step 4: Collecting survivor data...", ConsoleColors.OKBLUE)
try:
    soup = souper("/wiki/Survivors")
    target_divs = soup.find_all("div", style="display: inline-block; text-align:center; margin: 10px")
    a_list = []
    for div in target_divs:
        a_elements = div.find_all("a")
        for a in a_elements:
            a_list.append(a)
    a_list = a_list[::2]
    survivors = []
    for a in a_list:
        soup = souper(a["href"])
        wikitable = soup.find("table", class_ = "wikitable")
        table_rows = wikitable.find_all("tr")
        perks = []
        for row in table_rows:
            table_header = row.find_all("th")[1]
            perk = table_header.find("a")["title"]
            perks.append(perk)
            table_header_image = row.find_all("th")[0]
            image_link = table_header_image.find("a").find_next()["data-src"]
            #download_gif_to_png(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Survivor Perks\\" + remove_special_characters(perk) + ".png"))
            urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Survivor Perks\\" + remove_special_characters(perk) + ".png"))
        names_to_replace = ["Detective David Tapp", 'Jeffrey "Jeff" Johansen', "Leon Scott Kennedy"]
        new_names = ["Detective Tapp", "Jeff Johansen", "Leon S. Kennedy"]
        if a["title"] in names_to_replace:
            name = new_names[names_to_replace.index(a["title"])]
        else:
            name = a["title"]
        survivor = Survivor(name, perks)
        survivors.append(survivor)
    with open(os.path.join(os.path.dirname(__file__), "Assets\\Survivors.txt"), "w", encoding="utf-8") as file:
        for survivor in survivors:
            file.write(survivor.name + "|" + survivor.perks[0] + "|" + survivor.perks[1] + "|" + survivor.perks[2] + "\n")
    for i in range(1, len(survivors) + 1):
        try:
            image_link = soup.find("img", alt = "S" + f"{i:02}" + " charSelect portrait")["data-src"]
        except KeyError:
            image_link = soup.find("img", alt = "S" + f"{i:02}" + " charSelect portrait")["src"]
        scale_index = image_link.find("/scale")
        question_mark_index = image_link.find("?", scale_index)
        image_link = image_link[:scale_index] + image_link[question_mark_index:]
        urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\Survivors\\" + remove_special_characters(survivors[i - 1].name) + ".png"))
    log_message("Step 4: Data of " + str(len(survivors)) + " survivors collected", ConsoleColors.OKGREEN)
except Exception as e:
    log_message("Step 4: " + str(e), ConsoleColors.FAIL)

log_message("Step 5: Collecting general perks data...", ConsoleColors.OKBLUE)
try:
    soup = souper("/wiki/Perks/General_Perks")
    wikitables = soup.find_all("table", class_ = "wikitable")
    roles = ["Survivor", "Killer"]
    for role in roles:
        table_rows = wikitables[roles.index(role)].find_all("tr")
        perks, links = [], []
        for row in table_rows:
            table_header = row.find_all("th")[1]
            perk = table_header.find("a")["title"]
            perks.append(perk)
            link = table_header.find("a")["href"]
            links.append(link)
        with open(os.path.join(os.path.dirname(__file__), "Assets\\General " + role + " Perks.txt"), "w", encoding="utf-8") as file:
            for perk in perks:
                file.write(perk + "\n")
        for link in links:
            soup = souper(link)
            try:
                image_link = soup.find("div", class_ = "floatnone").find_next().find_next()["data-src"]
            except KeyError:
                image_link = soup.find("div", class_ = "floatnone").find_next().find_next()["src"]
            scale_index = image_link.find("/scale")
            question_mark_index = image_link.find("?", scale_index)
            image_link = image_link[:scale_index] + image_link[question_mark_index:]
            #download_gif_to_png(image_link, os.path.join(os.path.dirname(__file__), "Assets\\General " + role + " Perks\\" + remove_special_characters(perks[links.index(link)]) + ".png"))
            urllib.request.urlretrieve(image_link, os.path.join(os.path.dirname(__file__), "Assets\\General " + role + " Perks\\" + remove_special_characters(perks[links.index(link)]) + ".png"))
        roles[roles.index(role)] = len(perks)
    log_message("Step 5: Data of " + str(roles[0] + roles[1]) + " general perks collected", ConsoleColors.OKGREEN)
except Exception as e:
    log_message("Step 5: " + str(e), ConsoleColors.FAIL)

log_message(">>> Update Complete <<<", ConsoleColors.HEADER, is_bold=True)