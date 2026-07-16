import json
import os


FILE = "permissions.json"


def create_file():

    if not os.path.exists(FILE):

        with open(FILE, "w") as f:
            json.dump([], f)



def load_users():

    create_file()

    with open(FILE, "r") as f:

        return json.load(f)



def save_users(users):

    with open(FILE, "w") as f:

        json.dump(
            users,
            f,
            indent=4
        )



def has_permission(user_id):

    users = load_users()

    return user_id in users



def add_user(user_id):

    users = load_users()


    if user_id not in users:

        users.append(user_id)

        save_users(users)

        return True


    return False



def remove_user(user_id):

    users = load_users()


    if user_id in users:

        users.remove(user_id)

        save_users(users)

        return True


    return False



def get_users():

    return load_users()
