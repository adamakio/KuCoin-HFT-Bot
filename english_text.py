english_text = {
    "welcome_message": "Welcome to @Profit Kucoin Bot",
    "tutorial_name": "Linking KuCoin API Keys [Tutorial] by ShrimpyApp",
    "folder_warning": "WARNING: DO NOT MODIFY THIS FOLDER",
    "log_in_menu": {
        "yes": "y",
        "no": "n",
        "options": ["Create User", "Select User", "Delete User"],
        "select_titles": [
            "Select an option",
            "Select a user to fetch",
            "Select a user to delete",
        ],
        "create_user": {
            "form_name": "User Creation Form.",
            "success_message": "User {} created successfully!",
            "username": "Input Username: ",
            "already_exists_error": "User {} already exists.",
            "invalid_username_error": "Invalid username {}",
            "api_queries": [
                "Input kucoin api key: ",
                "Input kucoin api secret: ",
                "Input kucoin api passphrase: ",
            ],
            "invalid_api_error": "Invalid Kucoin API information:",
        },
        "fetch_user_success": "User {} fetched successfully!",
        "confirm_delete": "Are you sure you want to delete user {}?",
        "delete_success": "User {} deleted",
    },
    "run_task": {
        "yes": "y",
        "n": "n",
        "confirm": "Confirm?",
        "confirm_task": "Running task {} with following configuration",
        "starting_task": "Starting Task: ",
        "info": (
            "Press CTRL+C at anytime to cancel bot run.\n"
            "If canceled, trades may remain open in kucoin\n"
        ),
        "insufficient_balance": "Insufficient balance to start bot.\nAdd balance to your kucoin to continue",
        "task_menu": {
            "options": ["Create Task", "Select Task", "View Tasks", "Delete Task"],
            "select_titles": [
                "Select an option",
                "Select a task to run",
                "Select a task to view",
                "Select a task to delete",
            ],
            "create_task": {
                "form_name": "Task Creation Form.",
                "info": [
                    "The trade size is the amount in {} that will be used for each buy.",
                    "Maximum buys is the maximum number of unsold buy orders.",
                    "The buy percent is the percent decrease from the reference price to place a buy order.",
                    "The sell percent is the percent increase from the buy price to place a sell order.",
                    "If you choose to keep your profits invested, your profits will stay in {}.",
                ],
                "inputs": [
                    "Trade Size",
                    "Maximum Buys",
                    "Buy Percent",
                    "Sell Percent",
                ],
                "task_name": "New Task Name: ",
                "confirm_profits": "Keep profits invested? ",
                "yes": "y",
                "no": "n",
                "success_message": "Task {} successfully created",
                "invalid_task": "Invalid task name: {}",
                "task_exists": "Task {} already exists",
                "input_field": "Input {}: ",
                "input_set_message": "{} Set to: {} {}",
                "invalid_input_message": "Invalid Input for {}: {}",
            },
            "copy_task": {
                "info": "Reproducing task {}",
                "success_message": "New task {} successfully created",
                "task_name": "New task name: ",
                "invalid_task": "Invalid task to copy: {}",
                "task_exists": "Task {} already exists",
            },
            "view_task": {
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
                        "Price (ETH/USDT)",
                        "Amount (in ETH)",
                        "Fee (in USDT)",
                    ],
                },
                "profits": "Profits from completed cycles: {} {}",
            },
            "delete_task": {
                "confirm": "Are you sure you want to delete task {}?",
                "yes": "y",
                "no": "n",
                "task_deleted": "Task {} deleted.",
            },
        },
        "user_interrupted": "USER INTERRUPTED TASK",
        "rate_limited": "You have been rate limited. Please wait 6 minutes...",
        "market_info": {
            "market_price": "Market Price",
            "target_price": "Target prices",
            "balance": "Balance",
            "stop_buy": "Maximum buys reached",
            "requests": "Kucoin Requests",
            "time_elapsed": "Time elapsed",
            "buy": "buy",
            "sell": "sell",
            "completed_cycles": "Completed cycles",
        },
        "yes": "y",
        "no": "n",
    },
}
