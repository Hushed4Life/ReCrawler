# Modules
import requests
import functions as funcs

"""
Others
"""


def check_recnet_token(auth):
    auth = auth.replace('Bearer ', '')
    response = requests.get(f"https://accounts.rec.net/account/me", headers={'Authorization': f"Bearer {auth}"})
    if response.ok:
        data = response.json()
        funcs.cache_recnet_token(auth)  # Cache token
        funcs.cache_user_data(data)
        funcs.printdeb("RecNet token cached!")
        return True
    funcs.printdeb("Faulty token!")
    return False  # If faulty token


"""
Account API calls
"""


def auth_token_to_data(auth):
    auth = funcs.strip_token_from_bearer(auth)
    response = requests.get(f"https://accounts.rec.net/account/me", headers={'Authorization': f"Bearer {auth}"})
    if response.ok:
        data = response.json()
        data['success'] = True
        funcs.cache_user_data(data)
        return data
    return {'success': False, 'error': "Token is faulty!"}  # If faulty token


def acc_id_to_acc_data(acc_id):
    response = requests.get(f"https://accounts.rec.net/account/{acc_id}")
    if response.ok:
        acc_data = response.json()
        acc_data['success'] = True
        return acc_data
    return {'success': False, 'error': "User doesn't exist!"}


def username_to_acc_data(username):
    response = requests.get(f"https://accounts.rec.net/account?username={username}")
    if response.ok:
        acc_data = response.json()
        acc_data['success'] = True
        return acc_data
    else:
        return {'success': False, 'error': "User doesn't exist!"}


# Accepts either account id or username
def user_to_acc_data(user):
    if type(user) is int:
        return acc_id_to_acc_data(user)
    elif type(user) is str:
        return username_to_acc_data(user)
    else:
        return {'success': False, 'error': "Invalid user!"}


def acc_id_to_match_data(acc_id, auth):
    response = requests.get(f"https://match.rec.net/player?id={acc_id}", headers={'Authorization': f"Bearer {auth}"})
    if response.ok:
        match_data = response.json()[0]
        match_data['success'] = True
        return match_data
    else:
        return {'success': False, 'error': "User doesn't exist!"}


def username_to_match_data(username, auth):
    acc_data = username_to_acc_data(username)
    if acc_data['success']:
        return acc_id_to_match_data(acc_data['accountId'], auth)
    else:
        return acc_data  # return the error


# Accepts either account id or username
def user_to_match_data(user, auth):
    if type(user) is int:
        return acc_id_to_match_data(user, auth)
    elif type(user) is str:
        return username_to_match_data(user, auth)
    else:
        return {'success': False, 'error': "Invalid user!"}


def change_pfp(url, auth):
    if url:
        url = parse_post_url(url)

    funcs.printdeb(f"Image URL: {url}")

    response = requests.put("https://accounts.rec.net/account/me/profileimage",
                            headers={"Authorization": f"Bearer {auth}", "Accept": "*/*",
                                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                            data=f"imageName={url}")
    if response.ok:
        if not url:
            return {'success': True}

        acc_data = auth_token_to_data(auth)
        if acc_data['profileImage'] == url:
            return {'success': True}
        else:
            return {'success': False, 'error': "Invalid url!"}
    else:
        return {'success': False, 'error': f"Error {response.status_code} occurred!"}


def platform_mask_to_platforms(platforms):
    chk_tuple = ('Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS')
    output = []
    pos = 0
    while platforms:
        if platforms & 1:
            output.append(chk_tuple[pos])
        pos += 1
        platforms >>= 1
    return output


"""
Room API calls
"""


def room_id_to_room_data(room_id):
    response = requests.get(f"https://rooms.rec.net/rooms/{room_id}?include=366")
    if response.ok:
        room_data = response.json()
        room_data['success'] = True
        return room_data
    else:
        return {'success': False, 'error': "Room either doesn't exist or is private!"}


def room_name_to_room_data(room_name):
    response = requests.get(f"https://rooms.rec.net/rooms?name={room_name}")
    if response.ok:
        room_data = response.json()
        return room_id_to_room_data(room_data['RoomId'])  # Get all data
    else:
        return {'success': False, 'error': "Room either doesn't exist or is private!"}


# Accepts either room id or room name
def room_to_room_data(room):
    if type(room) is int:
        return room_id_to_room_data(room)
    elif type(room) is str:
        return room_name_to_room_data(room)
    else:
        return {'success': False, 'error': "Invalid room!"}


"""
Image API calls
"""


def set_post_description(url, desc, auth):
    img_id = parse_post_url(url)
    auth = funcs.strip_token_from_bearer(auth)
    response = requests.put(f"https://api.rec.net/api/images/v1/{img_id}/description",
                            headers={"Authorization": f"Bearer {auth}", "Accept": "*/*",
                                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                            data=f"description={desc}")
    img_data = post_id_to_data(url)
    if img_data['Description'] == desc:
        return {'success': True}
    else:
        return {'success': False, 'error': 'Invalid description!'}


def acc_id_to_images_taken(acc_id, take=1000000):
    response = requests.get(f"https://api.rec.net/api/images/v4/player/{acc_id}?take=3")
    if response.ok:
        room_data = response.json()
        return room_id_to_room_data(room_data['RoomId'])  # Get all data
    else:
        if user_to_acc_data(acc_id)['success']:
            return {'success': False, 'error': "User hasn't published anything!"}
        else:
            return {'success': False, 'error': "User doesn't exist!"}


def parse_post_url(url):
    post_id = url.split("/")[-1]
    try:
        post_id = int(post_id)
        return post_id
    except:
        return False


def post_id_to_data(img_id):
    img_id = parse_post_url(img_id)
    response = requests.get(f"https://api.rec.net/api/images/v4/{img_id}")
    if response.ok:
        data = response.json()
        data['success'] = True
        return data
    else:
        return {'success': False, 'error': "Post doesn't exist!"}
