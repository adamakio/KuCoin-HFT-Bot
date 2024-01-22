import os
import rich
import ccxt
import json
import shutil


def get_users_dir(curdir):
    users_dir = os.path.join(curdir, "Users")
    if not os.path.isdir(users_dir):
        os.mkdir(users_dir)
    return users_dir


def clean_users_dir(users_dir):
    users = os.listdir(users_dir)
    for user in users:
        user_dir = os.path.join(users_dir, user)
        try:
            load_keys(user_dir)
        except:
            shutil.rmtree(user_dir)


def create_user(users_dir, console, text):
    console.print(f"{text['form_name']}\n", style="bold underline")
    username, user_dir = get_username(users_dir, console, text)
    API_JSON = get_API_JSON(console, text)
    save_keys(user_dir, API_JSON)
    console.print(text["success_message"].format(username), style="green")
    return user_dir, API_JSON


def get_username(users_dir, console, text):
    console.print(text["username"], style="yellow")
    username = input()
    user_dir = os.path.join(users_dir, username)
    if os.path.isdir(user_dir):
        console.print(text["already_exists_error"].format(username), style="red")
        return get_username(users_dir, console, text)
    try:
        os.mkdir(user_dir)
        return username, user_dir
    except:
        console.print(text["invalid_username_error"].format(username), style="red")
        return get_username(users_dir, console, text)


def get_API_JSON(console, text):
    console.print(text["api_queries"][0], style="yellow")
    KUCOIN_API_KEY = input()
    console.print(text["api_queries"][1], style="yellow")
    KUCOIN_API_SECRET = input()
    console.print(text["api_queries"][2], style="yellow")
    KUCOIN_PASSWORD = input()
    API_JSON = {
        "KUCOIN_API_KEY": KUCOIN_API_KEY,
        "KUCOIN_API_SECRET": KUCOIN_API_SECRET,
        "KUCOIN_PASSWORD": KUCOIN_PASSWORD,
    }
    if check_API(API_JSON):
        return API_JSON
    else:
        console.print(text["invalid_api_error"], style="red")
        console.print_json(data=API_JSON)
        return get_API_JSON(console, text)


def fetch_user(users_dir, username, console, text):
    user_dir = os.path.join(users_dir, username)
    API_JSON = load_keys(user_dir)
    console.print(text["fetch_user_success"].format(username), style="green")
    return user_dir, API_JSON


def check_API(API_JSON):
    try:
        exchange = ccxt.kucoin(
            {
                "apiKey": API_JSON["KUCOIN_API_KEY"],
                "secret": API_JSON["KUCOIN_API_SECRET"],
                "password": API_JSON["KUCOIN_PASSWORD"],
                "timeout": 30000,
                # "verbose": True,
                "enableRateLimit": True,
                "rateLimit": 2000,
            },
        )
        exchange.fetchBalance()["USDT"]["free"]
        return True
    except ccxt.AuthenticationError:
        return False


def delete_user(users_dir, username, console, text):
    confirm_delete_msg = text["confirm_delete"].format(username)
    success_msg = text["delete_success"].format(username)
    console.print(
        f"{confirm_delete_msg} [red]{text['yes']}[/red]|[green]{text['no']}[/green]",
        style="bold",
    )
    confirmed = input() == "y"
    if confirmed:
        user_dir = os.path.join(users_dir, username)
        shutil.rmtree(user_dir)
        console.print(success_msg, style="bold")


def save_keys(user_dir, API_JSON):
    api_file = os.path.join(user_dir, "api.json")
    with open(api_file, "w") as f:
        json.dump(API_JSON, f)


def load_keys(user_dir):
    api_file = os.path.join(user_dir, "api.json")
    with open(api_file, "r") as f:
        API_JSON = json.load(f)
    return API_JSON
