# Imports
import os
import RecNet as rn
import functions as funcs
from Menus import accounts, images, rooms, settings


def intro():
    funcs.render_text("ReCrawler")
    print(
        "ReCrawler is an API library for RecNet. This is a completely revamped version of the previous ReCrawlers, "
        "and much, MUCH faster.")
    print("It's not an absolute guarantee this is safe to use. The features themselves are safe, "
          "but Rec Room's ToS does prohibit the usage of the API.")
    print("Any possible consequence is on you, and the creator of this software is NOT to be held accountable. Please "
          "continue at your own risk.")
    print("Also, I would recommend you to read the FAQ found in Settings > Help.")
    funcs.enter_continue()
    funcs.clear()

    funcs.update_config("intro", False)
    menu()


def menu(option="main"):
    config = funcs.get_config()
    data = funcs.read_user_data_cache()
    if data['success']:
        title = f"Hello there, {data['username']}!"
    else:
        title = "!Main"

    menu_contents = {
        title: [
            {"name": "Settings", "function": settings.menu},
            {"name": "Accounts", "function": accounts.menu},
            {"name": "Images", "function": images.menu},
            {"name": "Rooms", "function": rooms.menu},
            {"name": "Exit and Clear Cache", "function": exit_and_clear_cache}
        ]
    }

    funcs.print_menu("ReCrawler", menu_contents, option)


def exit_and_clear_cache():
    funcs.reset_cache()
    print("Cleared cache, closing...")
    exit()


def initialize():
    funcs.set_terminal_color(color="brightred")  # Turn terminal text color to light red (windows only)
    config = funcs.get_config()
    if config['intro']:
        intro()
    else:
        menu()


if __name__ == "__main__":
    initialize()
