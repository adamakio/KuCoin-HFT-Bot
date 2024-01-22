import os
import json
import shutil

from rich.table import Table
from datetime import datetime


def create_task(tasks_dir, console, text):
    print("")
    console.print(text["form_name"], style="bold underline")
    print("")
    symbol = "ETH/USDT"
    [base_currency, quote_currency] = symbol.split("/")

    task_dir, task_name = get_task_name(tasks_dir, console, text)
    console.print(
        text["info"][0].format(quote_currency),
        style="cyan",
    )
    trade_size = get_typed_input(text["inputs"][0], float, console, text)
    console.print(
        text["info"][1],
        style="cyan",
    )
    max_trades = get_typed_input(text["inputs"][1], int, console, text)
    console.print(
        text["info"][2],
        style="cyan",
    )
    buy_percent = get_typed_input(
        text["inputs"][2], float, console, text, bounds=[0, 100]
    )
    console.print(
        text["info"][3],
        style="cyan",
    )
    sell_percent = get_typed_input(
        text["inputs"][3], float, console, text, bounds=[0, 100]
    )
    console.print(
        text["info"][4].format(base_currency),
        style="cyan",
    )
    console.print(
        f"[yellow]{text['confirm_profits']}[/yellow] ([green]{text['yes']}[/green]|[red]{text['no']}[/red])  "
    )
    keep_profits_invested = input() == text["yes"]

    bot_config = {
        "base_currency": base_currency,
        "quote_currency": quote_currency,
        "symbol": symbol,
        "trade_size": trade_size,
        "buy_percent": buy_percent / 100,
        "buy_slippage": 0.05 / 100,  # percent limit order buy
        "sell_percent": sell_percent / 100,
        "sell_slippage": 0.05 / 100,  # percent limit order sell
        "max_trades": max_trades,  # max amount of
        "trades_path": task_dir,
        "keep_profits_invested": keep_profits_invested,
    }
    save_bot_config(bot_config, task_dir)
    print()
    console.print(text["success_message"].format(task_name), style="green")
    print()
    return bot_config


def get_task_name(tasks_dir, console, text):
    console.print(text["task_name"], style="yellow")
    task_name = input()
    task_dir = os.path.join(tasks_dir, task_name)
    if os.path.isdir(task_dir):
        console.print(text["task_exists"].format(task_name), style="red")
        return get_task_name(tasks_dir, console, text)
    try:
        os.mkdir(task_dir)
        return task_dir, task_name
    except:
        console.print(text["invalid_task"].format(task_name), style="red")
        return get_task_name(tasks_dir, console, text)


def get_typed_input(name, dtype, console, text, bounds=None):
    input_field = text["input_field"].format(name)
    input_set_message = text["input_set_message"]
    invalid_input_message = text["invalid_input_message"]
    console.print(input_field, style="yellow")
    s = input()
    try:
        user_input = dtype(s)
        if bounds is None:
            console.print(input_set_message.format(name, user_input, ""), style="green")
            return user_input
        if bounds[0] < user_input < bounds[1]:
            console.print(
                input_set_message.format(name, user_input, "%"), style="green"
            )
            return user_input
        console.print(invalid_input_message.format(name, s), style="red")
        return get_typed_input(name, dtype, console, bounds=bounds)
    except ValueError:
        console.print(invalid_input_message.format(name, s), style="red")
        return get_typed_input(name, dtype, console, bounds=bounds)
    except TypeError:
        console.print(invalid_input_message.format(name, s), style="red")
        return get_typed_input(name, dtype, console, bounds=bounds)


def copy_task(tasks_dir, task, console, text):
    try:
        console.print(text["info"].format(task), style="bold underline")
        old_task_dir = os.path.join(tasks_dir, task)
        print()
        new_task_dir, new_task = get_task_name(tasks_dir, console, text)
        bot_config = load_bot_config(old_task_dir)
        bot_config["trades_path"] = new_task_dir
        save_bot_config(bot_config, new_task_dir)
        console.print(text["success_message"].format(new_task), style="green")
        return bot_config
    except FileNotFoundError:
        console.print(text["invalid_task"].format(task))
        return {}


view_task_text = {
    "header": "Task {} configuration",
    "task_config_not_found": "Unable to view task configuration because it was not found",
    "task_trades_not_found": "Unable to view task trades because they were not found",
    "bot_config": {
        "trade_size": "Trade size",
        "buy_percent": "Buy Percent",
        "sell_percent": "Sell Percent",
        "max_trades": "Maximum buys",
        "keep_profits_invested": "Keep Profits Invested",
    },
    "task_trades": {
        "trades_title": "Filled Trades",
        "trades_columns": [
            "KuCoin Order ID",
            "Side",
            "Date",
            "Time",
            "Price (USDT per ETH)",
            "Amount (in ETH)",
            "Fee (in USDT)",
        ],
    },
    "profits": "Profits from completed cycles: {} {}",
}


def view_task(tasks_dir, task, console, text):
    task_dir = os.path.join(tasks_dir, task)
    try:
        bot_config = load_bot_config(task_dir)
        console.print(
            text["header"].format(task), style="red on white", justify="center"
        )
        print_bot_config(bot_config, console, text["bot_config"])
    except FileNotFoundError:
        console.print(text["task_config_not_found"], style="red")
    try:
        trades = load_trades(task_dir)
        print_task_trades(trades, bot_config, console, text)
    except FileNotFoundError:
        console.print(
            text["task_trades_not_found"],
            style="red",
        )


def print_bot_config(bot_config, console, text, justify="center"):
    shown_keys = text
    for key in bot_config:
        if key not in shown_keys:
            continue
        if "percent" in key:
            console.print(
                f"[bold]{shown_keys[key]}[/bold] : {bot_config[key] * 100:.2f} %",
                justify=justify,
            )
        else:
            console.print(
                f"[bold]{shown_keys[key]}[/bold] : {bot_config[key]}", justify=justify
            )


# ["id", "side", "timestamp", "price", "amount", "filled", "fee"]
def print_task_trades(trades, bot_config, console, text):
    task_trades_text = text["task_trades"]
    trades_table = Table(title=task_trades_text["trades_title"], style="blue")

    for column in task_trades_text["trades_columns"]:
        trades_table.add_column(column, no_wrap=True)
    for trade in trades:
        if not trade[5]:
            continue
        id = str(trade[0])
        side = trade[1]
        timestamp = trade[2]
        date = datetime.fromtimestamp(timestamp).strftime("%A, %B %d, %Y")
        time = datetime.fromtimestamp(timestamp).strftime("%I:%M:%S %p")
        price = str(trade[3])  # USDT per ETH
        amount = str(trade[4])  # ETH
        fee = str(trade[6])  # USDT
        if side == "buy":
            trades_table.add_row(
                id, side, date, time, price, amount, fee, style="green"
            )
        else:
            trades_table.add_row(id, side, date, time, price, amount, fee, style="red")

    console.print(trades_table, justify="center")
    profits = calculate_profits(trades, bot_config)
    if bot_config["keep_profits_invested"]:
        profits_currency = bot_config["base_currency"]
    else:
        profits_currency = bot_config["quote_currency"]
    console.print(text["profits"].format(profits, profits_currency), justify="center")


def load_trades(task_dir):
    trades_file = os.path.join(task_dir, "trades.json")
    with open(trades_file, "r") as fp:
        bot_config = json.load(fp)
    return bot_config


def calculate_profits(trades, bot_config):
    stack = []
    profits = 0.0
    for trade in trades:
        if not trade[5]:
            continue
        if trade[1] == "buy":
            stack.append(trade)
        else:
            sell_trade = trade
            buy_trade = stack.pop()
            buy_price, sell_price = buy_trade[3], sell_trade[3]
            buy_amount, sell_amount = buy_trade[4], sell_trade[4]
            buy_fee, sell_fee = buy_trade[6], sell_trade[6]
            if not bot_config["keep_profits_invested"]:
                cycle_profit = (sell_price - buy_price) * buy_amount  # USDT
                cycle_loss = buy_fee + sell_fee
            else:
                cycle_profit = sell_amount - buy_amount  # ETH
                cycle_loss = buy_fee / buy_price + sell_fee / sell_price
            profits += cycle_profit - cycle_loss
    return profits


def delete_task(tasks_dir, task, console, text):
    confirm_text = text["confirm"].format(task)
    console.print(
        f"{confirm_text} [red]{text['yes']}[/red]|[green]{text['no']}[/green]",
        style="bold",
    )
    confirmed = input() == text["yes"]
    if confirmed:
        user_dir = os.path.join(tasks_dir, task)
        shutil.rmtree(user_dir)
        console.print(text["task_deleted"].format(task), style="bold")


def save_bot_config(bot_config, task_dir):
    bot_config_file = os.path.join(task_dir, "bot_config.json")
    with open(bot_config_file, "w") as fp:
        json.dump(bot_config, fp, indent=4)


def load_bot_config(task_dir):
    bot_config_file = os.path.join(task_dir, "bot_config.json")
    with open(bot_config_file, "r") as fp:
        bot_config = json.load(fp)
    return bot_config
