import os
import rich
import time
from consolemenu import SelectionMenu

from enum import Enum
from rich.live import Live
from rich.padding import Padding
from rich.console import Console

from User import get_users_dir, clean_users_dir, create_user, fetch_user, delete_user
from Task import create_task, copy_task, view_task, delete_task, print_bot_config
from SimpleBot import SimpleBot
from english_text import english_text
from spanish_text import spanish_text


class Language(Enum):
    english = 1
    espanol = 2


def print_ascii_logo():
    lines = [
        "$$$$$$$$$$hJj{~I^.   `:>]/Xq%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$MX]`   'i](/jjf|}<'    <rb$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$m]   ,(Co$$$$$$$$$$$$WZji   lXB$$$$$$$$$$$$$$$$$$$$$$$$$$$$oCvuvYmB$8db%$$$$$$$$$$$$",
        "$$a_   ]m$$$$$$wzzzzzXUQp8$$$of`  :Q$$$$$$$$$$$$$$$$$$$$$$$$$@{      `%Q.  'q$$$$$$$$$$$",
        "$0'  lp$$$$$$$$l          _q$$$W{   \$$$$$$$$$$$$$$$$$$$$$$$$Y   ih&aq$Wj]]n%$$$O'''I$$$",
        "p.  >8$$$$$$$$h    U8Wk(   .a$$BBx-~+Jdd%$$$$$MkppkM$$$$$$@BB>   UBB@$$BBBB@$@BB1   \BBB",
        "+   o$$$$$$$$$x   .8$$$U    b$U   I/^  ,B$Wv_`      '+z%$$_         x$%'   h$[        .w",
        ".  ;$$$$$$$$$$!   ]v|{>   'c$$?    _--rm$U`  .{XOOX_   IM$wm}   +mmm&$Q   I$$qmx   ,mmp$",
        "I  '%$$$$$$$$a    Xl;Ii-\C8$$8.   v:  k$o    q$$$$$$I   v$$$!   U$$$$${   j$$$$|   /$$$$",
        "X   \$$$$$$$$n   .&$$$$$$$$$$J   >\  _$$b    h$$$$$0.   p$$o   .&$$$$B`   b$$$@^   q$$$$",
        "$|   |%$$$$$#;   -$$$$$$$$$$$]   n, lW$$$x.  .-|\{;   lZ$$$u   -$$$$$O   :$$$$m   ,$$$$$",
        "$$z`  ^{xvj?.    v$$$$$$$$$$@[---U 18$$$$$Mc}i,``,!]xp$$$$$f???0$$$$$X???z$$$$Y???v$$$$$",
        "$$$M/'          _8$$$$$$$$@dxl   -p$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$8U};.  `i\w$$$$$WZv|~'   ixo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$$$$$B@$$$$$$qtl    :-fLM$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$$$$$$$$$$@YI i\Yq#@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$$$$$$$$$b!?J&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$$$$$$$$w\*$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "$$$$$$$$$$$$$Z$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
    ]
    lenline = len(lines[-1])
    logo = "\n".join(lines)
    rich.print(f"[blue]{logo}[/blue]")
    return lenline


def App(language):
    console = Console()
    if language == Language.english:
        text = english_text
    elif language == Language.espanol:
        text = spanish_text
    else:
        raise ValueError(f"Language {language} not supported")

    lenline = print_ascii_logo()
    lentext = len(text["welcome_message"])
    lenspace = (lenline - lentext) // 2
    welcome = " " * lenspace + text["welcome_message"] + " " * lenspace + "'"
    console.print(welcome, style="blue on white")
    console.print(
        f"\n[bold]{text['tutorial_name']}:[/bold]\n"
        "[link]https://shrimpyapp.medium.com/linking-kucoin-api-keys-tutorial-99417739d30c\n[/link]"
    )
    curdir = os.path.abspath(os.path.curdir)
    console.print(f"{text['folder_warning']} {curdir}\n", style="yellow")

    users_dir = get_users_dir(curdir)
    clean_users_dir(users_dir)

    user_dir, API_JSON = LogInMenu(users_dir, console, text["log_in_menu"])

    tasks_dir = os.path.join(user_dir, "Tasks")
    if not os.path.isdir(tasks_dir):
        os.mkdir(tasks_dir)
    run_task(tasks_dir, API_JSON, console, text["run_task"])


def LogInMenu(users_dir, console, text):
    users = os.listdir(users_dir)
    if users:
        options = text["options"]
        log_in_menu = SelectionMenu(
            options, text["select_titles"][0], clear_screen=False
        )
        log_in_menu.show()
        log_in_menu.join()
        selection = log_in_menu.selected_option
        if selection == 0:
            return create_user(users_dir, console, text["create_user"])
        elif selection == 1:
            select_user_menu = SelectionMenu(
                users, text["select_titles"][1], clear_screen=False
            )
            select_user_menu.show()
            select_user_menu.join()
            if select_user_menu.selected_option < len(users):
                user = users[select_user_menu.selected_option]
                return fetch_user(users_dir, user, console, text)
            else:
                return LogInMenu(users_dir, console, text)
        elif selection == 2:
            select_user_menu = SelectionMenu(
                users, text["select_titles"][2], clear_screen=False
            )
            select_user_menu.show()
            select_user_menu.join()
            if select_user_menu.selected_option < len(users):
                user = users[select_user_menu.selected_option]
                delete_user(users_dir, user, console, text)
            return LogInMenu(users_dir, console, text)
        else:
            return LogInMenu(users_dir, console, text)
    else:
        return create_user(users_dir, console, text["create_user"])


def run_task(tasks_dir, API_JSON, console, text):
    bot_config = TaskMenu(tasks_dir, console, text["task_menu"])
    task = os.path.basename(bot_config["trades_path"])
    confirm_task_msg = text["confirm_task"].format(task)
    console.print(
        confirm_task_msg,
        style="red on white",
        justify="center",
    )
    print_bot_config(
        bot_config,
        console,
        text["task_menu"]["view_task"]["bot_config"],
        justify="center",
    )
    console.print(
        f"{text['confirm']} [red]{text['yes']}[/red]|[green]{text['no']}[/green]",
        style="bold",
    )
    confirmed = input() == text["yes"]

    if confirmed:
        console.print(
            f"\n[bold]{text['starting_task']}[green]{task}[/green][/bold]\n {text['info']}",
            style="yellow italic",
            justify="center",
        )
        bot = SimpleBot(bot_config, API_JSON)

        if bot.insufficient_balnce:
            console.print(
                text["insufficient_balance"],
                style="red",
            )
            return run_task(tasks_dir, API_JSON, console, text)
        if bot_config["keep_profits_invested"]:
            profits_currency = bot_config["base_currency"]
        else:
            profits_currency = bot_config["quote_currency"]
        with Live(bot.market_info(text["market_info"])) as live:
            while True:
                try:
                    moved = bot.executeBot()
                    if moved:
                        trades_table = bot.trades_table(
                            text["task_menu"]["view_task"]["task_trades"]
                        )
                        profits = bot.calculate_profits()
                        live.console.print()
                        live.console.print(trades_table, justify="center")
                        live.console.print(
                            text["task_menu"]["view_task"]["profits"].format(
                                profits, profits_currency
                            ),
                            justify="center",
                        )

                    live.update(bot.market_info(text["market_info"]), refresh=True)
                    time.sleep(1)
                except KeyboardInterrupt:
                    live.console.print(text["user_interrupted"], style="red")
                    break
                # except:
                #    live.console.print(text["rate_limited"])
                #    time.sleep(6 * 60)
        return run_task(tasks_dir, API_JSON, console, text)
    else:
        return run_task(tasks_dir, API_JSON, console, text)


def TaskMenu(tasks_dir, console, text):
    tasks = os.listdir(tasks_dir)
    if tasks:
        options = text["options"]
        task_menu = SelectionMenu(options, text["select_titles"][0], clear_screen=False)
        task_menu.show()
        task_menu.join()
        selection = task_menu.selected_option
        if selection == 0:
            return create_task(tasks_dir, console, text["create_task"])
        elif selection == 1:
            select_task_menu = SelectionMenu(
                tasks, text["select_titles"][1], clear_screen=False
            )
            select_task_menu.show()
            select_task_menu.join()
            if select_task_menu.selected_option < len(tasks):
                task = tasks[select_task_menu.selected_option]
                bot_config = copy_task(tasks_dir, task, console, text["copy_task"])
                if bot_config == {}:
                    return TaskMenu(tasks_dir, console, text)
                else:
                    return bot_config
            else:
                return TaskMenu(tasks_dir, console, text)
        elif selection == 2:
            select_task_menu = SelectionMenu(
                tasks, text["select_titles"][2], clear_screen=False
            )
            select_task_menu.show()
            select_task_menu.join()
            if select_task_menu.selected_option < len(tasks):
                task = tasks[select_task_menu.selected_option]
                view_task(tasks_dir, task, console, text["view_task"])
            return TaskMenu(tasks_dir, console, text)
        elif selection == 3:
            select_task_menu = SelectionMenu(
                tasks, text["select_titles"][3], clear_screen=False
            )
            select_task_menu.show()
            select_task_menu.join()
            if select_task_menu.selected_option < len(tasks):
                task = tasks[select_task_menu.selected_option]
                delete_task(tasks_dir, task, console, text["delete_task"])
            return TaskMenu(tasks_dir, console, text)
        else:
            return App(language=language)
    else:
        return create_task(tasks_dir, console, text["create_task"])


if __name__ == "__main__":
    language = Language.espanol
    App(language=language)
