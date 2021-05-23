# Imports
import functions
import main
import functions as funcs
import RecNet as rn

"""
Accounts menu
"""


def menu(option="main"):
    menu_contents = {
        "Getting Data": [
            {"name": "Get Account Data", "function": get_account_data},
            {"name": "Get My Data [AUTH]", "function": get_my_data},
            {"name": "Get Matchmaking Data [AUTH]", "function": get_matchmaking_data}
        ],
        "Profile Picture": [
            {"name": "Reset Profile Picture [AUTH]", "function": reset_profile_picture},
            {"name": "Set Profile Picture With URL [AUTH]", "function": set_profile_picture_with_url},
            {"name": "Set Room's Thumbnail as Profile Picture [AUTH]", "function": room_thumbnail_as_profile_picture},
            {"name": "Steal User's Profile Picture [AUTH]", "function": steal_user_profile_picture},
            #{"name": "Animated Profile Picture [AUTH]", "function": animated_profile_picture}
        ]
    }

    funcs.print_menu("Accounts", menu_contents, option)


"""
Submenus
"""

def animated_profile_picture():
    token = funcs.read_recnet_token_cache()
    if token:
        data = rn.auth_token_to_data(token)
        if not funcs.check_cfg_cache():
            print("Looks like you don't have caching enabled.")
            print("It's HIGHLY recommended for this feature, because in order for ReCrawler to check the validity of "
                  "your images, ReCrawler has to change your profile picture and see if RecNet accepted it.")

            print("1. Continue")
            print("2. Exit")
            option = funcs.select()
            if option != "1":
                return menu()
        else:
            old_pfp = data['profileImage']
            funcs.cache_pfp(old_pfp)

        funcs.create_txt("animated_pfp_frames.txt", )


    menu()



def get_my_data():
    token = funcs.read_recnet_token_cache()
    if token:
        data = rn.auth_token_to_data(token)

        clipboard = []
        for key in data:
            parsed = parse_account_data_key(key, data)
            clipboard.append(parsed['value'])
            print(f"{parsed['key']}: {parsed['value']}")

        print("\n")
        print("Enter: Continue")
        print("0: Copy a value")

        option = funcs.select()
        if option == "0":  # Copy a value
            funcs.clipboard_copy_menu(clipboard)
            menu()
        else:
            menu()
    menu()


def room_thumbnail_as_profile_picture():
    token = funcs.read_recnet_token_cache()
    if token:
        print("SET ROOM'S THUMBNAIL AS PROFILE PICTURE")
        print("Allows you to set your profile picture as a room's thumbnail.")
        print("Please enter the name of the room you want to steal the thumbnail from.")

        room = funcs.select("Room")

        if not room:
            return menu()

        room_data = rn.room_to_room_data(room)

        if room_data['success']:
            url = room_data['ImageName']

            if url == "DefaultRoomImage.jpg":
                funcs.printerr("Can't steal default room thumbnail!")
                return menu()

            response = rn.change_pfp(url, token)
            if response['success']:
                print("Room thumbnail set as profile picture successfully!")
            else:
                funcs.printerr(response['error'])
        else:
            funcs.printerr(room_data['error'])
    menu()


def steal_user_profile_picture():
    token = funcs.read_recnet_token_cache()
    if token:
        print("STEAL USER'S PROFILE PICTURE")
        print("Allows you to set your profile picture as someone else's.")
        print("Please enter the username of the user whose profile picture you would like to steal.")

        user = funcs.select("Username")

        if not user:
            return menu()

        acc_data = rn.user_to_acc_data(user)
        if acc_data['success']:
            url = acc_data['profileImage']

            if url == "DefaultProfileImage":
                funcs.printerr("Can't steal default profile picture!")
                return menu()

            response = rn.change_pfp(url, token)
            if response['success']:
                print("Profile picture stolen successfully!")
            else:
                funcs.printerr(response['error'])
        else:
            funcs.printerr(acc_data['error'])

    menu()

def set_profile_picture_with_url():
    token = funcs.read_recnet_token_cache()
    if token:
        print("SET PROFILE PICTURE WITH URL")
        print("Link's host must be 'img.rec.net'. No third-party images are allowed.")
        print("Profile picture will be immediately set (if it's legitimate) after you enter an url.")

        url = funcs.select("img.rec.net url")

        if not url:
            return menu()

        funcs.clear()
        response = rn.change_pfp(url, token)
        if response['success']:
            print("Profile picture changed successfully!")
        else:
            funcs.printerr(response['error'])
    menu()


def reset_profile_picture():
    token = funcs.read_recnet_token_cache()
    if token:
        print("RESET PROFILE PICTURE")
        print("Are you sure you want to reset your profile picture?")
        print("1. Yes")
        print("2. No")

        option = funcs.select()

        if option == "1":
            funcs.clear()
            response = rn.change_pfp("", token)
            if response['success']:
                print("Profile picture successfully reset!")
            else:
                funcs.printerr(response['error'])

    menu()


def get_matchmaking_data():
    token = funcs.read_recnet_token_cache()
    if token:
        print("GET MATCHMAKING DATA")
        print("Input a username")
        user = "None"
        while user == "None":
            user = input("\nUser > ")
            if not user:  # Exit
                funcs.clear()
                menu()
            match_data = rn.user_to_match_data(user, token)
            if not match_data['success']:
                funcs.clear()
                funcs.printerr(match_data['error'])
                user = "None"
        funcs.clear()

        clipboard = []
        for key in match_data:
            parsed = parse_matchmaking_key(key, match_data)
            clipboard.append(parsed['value'])
            print(f"{parsed['key']}: {parsed['value']}")

        print("\n")
        print("Enter: Continue")
        print("0: Copy a value")

        option = funcs.select()
        if option == "0":  # Copy a value
            funcs.clipboard_copy_menu(clipboard)
            menu()
        else:
            menu()

    menu()


def get_account_data():
    user = "None"
    while user == "None":
        print("GET ACCOUNT DATA")
        print("Input a username")
        user = input("\nUser > ")
        if not user:  # Exit
            funcs.clear()
            menu()
        account_data = rn.user_to_acc_data(user)
        if not account_data['success']:
            funcs.clear()
            funcs.printerr(account_data['error'])
            user = "None"
    funcs.clear()

    clipboard = []
    for key in account_data:
        parsed = parse_account_data_key(key, account_data)
        clipboard.append(parsed['value'])
        print(f"{parsed['key']}: {parsed['value']}")

    print("\n")
    print("Enter: Continue")
    print("0: Copy a value")

    option = funcs.select()
    if option == "0":  # Copy a value
        funcs.clipboard_copy_menu(clipboard)
        menu()
    else:
        menu()


"""
Functionality
"""


def parse_account_data_key(old_key, account_data):
    key_replacements = {
        "accountId": "Account Id",
        "username": "Username",
        "displayName": "Display Name",
        "profileImage": "Profile Image URL",
        "bannerImage": "Banner Image URL",
        "isJunior": "Junior",
        "platforms": "Platforms",
        "createdAt": "Join Date",
        "availableUsernameChanges": "Username Changes Left",
        "email": "E-mail",
        "birthday": "Birthday"
    }

    try:
        key = key_replacements[old_key]
    except:
        key = old_key

    value = account_data[old_key]
    if old_key == "platforms":
        value = ", ".join(rn.platform_mask_to_platforms(account_data[old_key]))
    elif old_key == "profileImage":
        img = account_data[old_key]
        value = f"https://rec.net/image/{img}\nhttps://img.rec.net/{img}"
    elif old_key == "bannerImage":
        img = account_data[old_key]
        value = f"https://rec.net/image/{img}\nhttps://img.rec.net/{img}"

    return {"key": key, "value": value}


def parse_matchmaking_key(old_key, match_data):
    key_replacements = {
        "playerId": "Account Id",
        "statusVisibility": "Appears Online To",
        "deviceClass": "Platform",
        "vrMovementMode": "Locomotion",
        "roomPlaylistId": "Playlist Id",
        "roomInstance": "Instance",
        "isOnline": "Online",
        "lastOnline": "Last Online",
        "appVersion": "Version"
    }

    device_class = {
        0: "Unknown",
        1: "VR",
        2: "Screen",
        3: "Mobile",
        4: "Quest 1",
        5: "Quest 2"
    }

    locomotions = {
        0: "Teleport",
        1: "Walk"
    }

    status_visibility = {
        0: "Public",
        1: "Friends Only",
        2: "Favorites Only",
        3: "Offline"
    }

    try:
        key = key_replacements[old_key]
    except:
        key = old_key

    value = match_data[old_key]
    if old_key == "deviceClass":
        value = device_class[int(value)]
    elif old_key == "vrMovementMode":
        value = locomotions[int(value)]
    elif old_key == "statusVisibility":
        value = status_visibility[int(value)]

    return {"key": key, "value": value}



