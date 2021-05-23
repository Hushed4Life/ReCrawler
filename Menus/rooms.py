# Imports
import main
import functions as funcs

"""
Rooms menu
"""


def menu(option="main"):
    menu_contents = {
        "": []
    }

    funcs.print_menu("Rooms", menu_contents, option)