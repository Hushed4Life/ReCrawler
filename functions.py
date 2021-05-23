# Imports
import json
import os
import pyperclip
import main
import shutil
import RecNet as rn

try:
    import pyfiglet
    import pyfiglet.fonts
    from pyfiglet import Figlet
except:
    pass

appdata = os.getenv('APPDATA') + "/"
cache_folder_name = "ReCrawlerCache"

pfp_path = appdata + cache_folder_name + "/pfp.txt"
token_path = appdata + "token.txt"
cache_path = appdata + cache_folder_name
last_id_path = appdata + cache_folder_name + "/last_acc_id.txt"

"""
Files
"""


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        printdeb("Tried deleting a nonexistent file!")


def delete_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    else:
        printdeb("Tried deleting a nonexistent folder!")


def create_txt(file_name, contents):
    with open(file_name, 'w') as f:
        f.write(contents)


def load_txt(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def check_file_existence(file_name):
    try:
        with open(file_name) as f:
            return True  # File exists!
    except FileNotFoundError:
        return False  # File doesn't exist!


def strip_token_from_bearer(token):
    try:
        return token.replace('Bearer ', '')
    except AttributeError:
        return token


"""
Cache
"""


def cache_pfp(pfp):
    if not check_cfg_cache():
        return
    check_and_create_cache_folder()
    create_txt(pfp_path, pfp)


def check_cfg_cache():
    cfg = get_config()
    enabled = cfg['cache']
    if not enabled:
        reset_cache()
    return enabled


def check_and_create_cache_folder():
    if not check_cfg_cache():
        return
    try:
        os.mkdir(cache_path)
        printdeb("Cache folder created!")
    except FileExistsError:
        printdeb("Cache folder exists!")


def cache_last_acc_id(acc_id):
    if not check_cfg_cache():
        return
    check_and_create_cache_folder()
    create_txt(last_id_path, acc_id)


def cache_recnet_token(auth):
    if not check_cfg_cache():
        return
    check_and_create_cache_folder()
    create_txt(token_path, auth)


def cache_user_data(data):
    if not check_cfg_cache():
        return

    acc_id = str(data['accountId'])

    check_and_create_cache_folder()
    save_j(cache_path + acc_id + ".json", data)
    cache_last_acc_id(acc_id)
    printdeb("Cached user data!")


def read_user_data_cache():
    if not check_cfg_cache():
        return {'success': False}

    acc_id = read_last_acc_id()
    if not acc_id:
        return {'success': False}

    path = cache_path + str(acc_id) + ".json"

    if check_file_existence(path):
        data = load_j(path)
        data['success'] = True
        printdeb("Returned user data cache!")
        return data
    printdeb("Failed to return user data cache!")
    return {'success': False}


def read_last_acc_id():
    if not check_cfg_cache():
        return {'success': False}
    if check_file_existence(last_id_path):
        acc_id = load_txt(last_id_path)
        if acc_id:
            printdeb("Returned last account id!")
            return acc_id
    printdeb("Failed to return last account id!")
    return {'success': False}


def reset_cache():
    delete_folder(cache_path)
    printdeb("Cache reset!")


def read_recnet_token_cache(prompt=True):
    if check_file_existence(token_path):
        token = load_txt(token_path)
        if token:
            if rn.check_recnet_token(token):
                return token
            else:
                reset_cache()
                if prompt:
                    return prompt_recnet_token("expired")
        else:
            if prompt:
                return prompt_recnet_token("")
    else:
        if prompt:
            return prompt_recnet_token("")


"""
JSON
"""


def load_j(file):
    with open(file) as json_file:
        return json.load(json_file)


def save_j(to_file, file):
    with open(to_file, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)


"""
Others
"""


def prompt_recnet_token(mode="input"):
    if mode == "input":
        option = "1"  # Get straight to the point
    else:
        if mode == "required":
            print("Authorization is required for this feature. Do you wish to input it?")
        elif mode == "expired":
            print("Your authorization token has expired! Do you wish to renew it?")
        else:
            print("Authorization wasn't found. Do you wish to input it?")
        print("1. Yes")
        print("2. No")
        option = select()
    if option == "1":
        reset_cache()
        token = "None"
        while token == "None":
            print("Input your authorization token from RecNet.")
            print("You may leave the input field empty in order to exit this prompt.")
            token = input("\nToken > ")
            if not token:  # Exit
                return False
            if rn.check_recnet_token(token):
                clear()
                print("Valid token!")
                return token
            else:
                clear()
                token = "None"
                printerr("Invalid token!")
    else:
        clear()
        reset_cache()
        return False


def set_terminal_color(color="white"):
    colors = {
        "black": 0,
        "blue": 1,
        "green": 2,
        "cyan": 3,
        "red": 4,
        "magenta": 5,
        "yellow": 6,
        "brown": 6,
        "white": 7,
        "gray": 8,
        "brightblue": 9,
        "brightgreen": "A",
        "brightcyan": "B",
        "brightred": "C",
        "brightmagenta": "D",
        "brightyellow": "E",
    }

    if color in colors:
        os.system(f'color {colors[color]}')
    else:
        os.system(f"color {colors['white']}")


def select(text="Select"):
    selection = input(f"\n{text} > ")
    clear()
    return selection


def open_website(url):
    os.system(f"start \"\" {url}")


def clear():
    os.system('cls')


def printdeb(text):
    config = get_config()
    if config['debug']:
        print(f"DEBUG - {text}")


def printerr(text):
    print(f"ERROR - {text}")


def enter_continue(text=""):
    if text:
        input(f"{text}\n\nPress Enter to continue...")
    else:
        input("\nPress Enter to continue...")

    clear()


def render_text(text, font="standard"):
    try:
        f = Figlet(font=font)
        print(f.renderText(text))
    except:
        print(text.upper())


def clipboard_copy_menu(clipboard):
    i = 0
    for key in clipboard:
        print(f"{i}. {key}")
        i += 1

    print("Select value to copy")
    option = select()

    try:
        option = int(option)
        pyperclip.copy(clipboard[option])
        print(f"Copied '{clipboard[option]}' to clipboard!")
        return clipboard[option]
    except:
        printerr("Invalid value, cancelling...")
        return False


def get_menu_selection(menu_contents, selection):
    try:
        selection = int(selection)
    except:
        return False

    i = 0
    for category in menu_contents:
        for feature in menu_contents[category]:
            if i == selection:
                return feature['function']
            i += 1
    return False


def print_menu(title, menu_contents, option="main"):
    if option == "main":
        render_text(title)
        i = 0
        for category in menu_contents:
            if category[:1] != "!":
                print("\r")
                print(category)
            for feature in menu_contents[category]:
                print(f"{i}. {feature['name']}")
                i += 1
    elif option == "":
        main.menu()
    else:
        function = get_menu_selection(menu_contents, option)
        if function:
            if type(function) is list:  # Fire all functions, if multiple
                for func in function:
                    func()
            else:
                function()
        else:
            printerr("Invalid selection!")
            print_menu(title, menu_contents)

    option = select()
    print_menu(title, menu_contents, option)


def get_menu_contents(menu):
    menu_contents = load_j('menu_contents.json')
    if menu in menu_contents:
        return menu_contents[menu]
    else:
        return False


"""
Config
"""


def get_default_config():
    return {
        "version": 1.0,
        "cache": True,
        "intro": True,
        "debug": False
    }


def update_config(setting, value):
    config = get_config()
    if setting in config:
        config[setting] = value
        save_config(config)
        printdeb(f"Updated key '{setting}' to '{value}' in config...")
    else:
        printdeb(f"Key '{setting}' not found in config!")


def patch_config(config):
    default_cfg = get_default_config()
    change_flag = False

    # Check for missing keys
    for key in default_cfg:
        if key not in config:
            if not change_flag:
                print("Detected config tampering, started patching...")
                change_flag = True
            config[key] = default_cfg[key]
            print(f"Patched key '{key}' in config...")

    # Check for unnecessary keys
    to_remove = []
    for key in config:
        if key not in default_cfg:
            if not change_flag:
                print("Detected config tampering, started patching...")
                change_flag = True
            to_remove.append(key)

    for key in to_remove:
        config.pop(key)
        print(f"Removed key '{key}' from config...")

    if change_flag:  # Only print if something was patched
        save_config(config)
        print("Done patching config!")

    return config


def get_config():
    if not check_file_existence('config.json'):
        save_j("config.json", get_default_config())

    config = patch_config(load_j("config.json"))
    return config


def save_config(config):
    save_j('config.json', config)
