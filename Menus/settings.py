# Imports
import functions
import main
import functions as funcs
import RecNet as rn

"""
Settings menu
"""


def menu(option="main"):
    menu_contents = {
        "General": [
            {"name": "Help", "function": help_me},
            {"name": "Toggle Debug Mode", "function": toggle_debug},
            {"name": "Reset Data", "function": reset_data}
        ],
        "Authorization": [
            {"name": "Check RecNet Authorization", "function": check_recnet_authorization},
            {"name": "Input RecNet Authorization", "function": [funcs.prompt_recnet_token, menu]}
        ],
        "Cache": [
            {"name": "Toggle Caching", "function": toggle_cache},
            {"name": "Clear Cache",
             "function": [funcs.reset_cache, menu]}
        ]
    }

    funcs.print_menu("Settings", menu_contents, option)


def check_recnet_authorization():
    funcs.read_recnet_token_cache()
    menu()


def reset_data():
    funcs.delete_file('config.json')
    funcs.reset_cache()
    main.initialize()


def toggle_debug():
    cfg = funcs.get_config()
    funcs.update_config("debug", not cfg['debug'])
    menu()


def toggle_cache():
    cfg = funcs.get_config()
    cfg['cache'] = not cfg['cache']
    funcs.save_config(cfg)
    funcs.reset_cache()
    if cfg['cache']:
        print("Cache toggled on!")
    else:
        print("Cache toggled off!")
    menu()


def help_me():
    funcs.render_text("Help")
    print("First time using ReCrawler? Here's an useful FAQ.")

    print("\n")

    print("Q: How do I get my authorization token?")
    print("A: Stop using this program. Right now.")

    print("\n")

    print("Q: How do I go back on a menu? How about canceling an action?")
    print("A: Just press enter.")

    print("\n")

    print("Q: Do I need a RecNet authorization token?")
    print("A: For every authorized feature, yes. If a feature requires authorization, there will be an indicator next "
          "to it. If you try to use a feature that requires your token, ReCrawler will kindly ask you for it.")

    print("\n")

    print("Q: Does my RecNet token get cached?")
    print("A: Yes, indeed. This is done to save you from pasting it every time you want to use a feature, that "
          "requires your token. However, keep in mind, that tokens expire after an hour!")

    print("\n")

    print("Q: Is this program illegal?")
    print("A: Sorta. Generally using RecNet's API is technically against the ToS. Some features reveal lots of data "
          "of someone. It should be safe to use this program, but it's not a 100% guarantee.\nIf you do somehow get "
          "punished for using this program, it's all your fault, and the creator of this program is not in any way "
          "responsible for it.")

    print("\n")

    print("Q: Will I get banned for using this program?")
    print("A: Read the above again. The odds are as minuscule as Rec Room's team size.")

    print("\n")

    print("Q: Will my token get stolen?")
    print("A: No.")

    print("\n")

    print("Q: Wanna make out?")
    print("A: Sure.")

    functions.enter_continue()

    menu()
