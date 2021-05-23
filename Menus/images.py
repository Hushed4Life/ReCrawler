# Imports
import main
import functions as funcs
import RecNet as rn

"""
Images menu
"""


def menu(option="main"):
    menu_contents = {
        "POST": [
            {"name": "Set Post Description [AUTH]", "function": set_image_desc}
        ]
    }

    funcs.print_menu("Images", menu_contents, option)

"""
Submenus
"""

def set_image_desc():
    token = funcs.read_recnet_token_cache()
    if token:
        data = rn.auth_token_to_data(token)
        print("SET POST DESCRIPTION")
        print("Allows you to write a description on a post. This is not an official feature in RecNet, and Rec Room "
              "staff *may* not appreciate this.")
        print("The description appears in embeds. If you send the post once with the description, you won't be able "
              "to change the embed text anymore.")

        url = funcs.select("RecNet post link")
        post_data = rn.post_id_to_data(url)

        # Error handling
        if post_data['success']:
            if post_data['PlayerId'] != data['accountId']:
                print("You don't own that post!")
                return menu()
        else:
            print("The post you inputted doesn't exist!")
            return menu()

        print("Input the description. This will also show up in embeds.")
        desc = funcs.select("Description")
        if not desc:
            return menu()

        response = rn.set_post_description(url, desc, token)
        if response['success']:
            print("Description successfully set!")
        else:
            print(response['error'])

    menu()