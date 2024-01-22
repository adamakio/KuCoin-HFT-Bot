# KuCoin High Frequency Trading Grid Bot

## Introduction
Welcome to the Kucoin Simple Bot repository, a high-frequency grid trading bot designed for the Kucoin platform. This Python bot is tailored for traders seeking to automate their trading strategies and is accessible for both English and Spanish speakers.

## Features
- **Multi-Language Support**: The bot is bilingual, with complete functionality in both English and Spanish.
- **User Management**: Users can create, select, and delete user profiles within the bot to manage multiple trading strategies or accounts.
- **Task Handling**: Each user can create, view, and manage tasks, which include individual trading strategies and executions.
- **Executables**: The bot is compiled into executables for macOS and Windows, ensuring ease of use across platforms without the need for a Python environment.

## Directory Structure
.
├── README.md  
├── SimpleBot.py  
├── Task.py  
├── User.py  
├── ascii_atprofit.txt  
├── english_text.py  
├── executable.py  
├── exec_eng/  
├── exec_esp/  
├── pyinstaller_commands.py  
├── spanish_text.py  
└── working_exec/  

- `SimpleBot.py`: The core bot logic and operations.
- `User.py`: Handles user profile creation, selection, and deletion.
- `Task.py`: Manages trading tasks, allowing users to set up individual trading strategies.
- `executable.py`: The entry point for the packaged executables, containing the user and task menus.
- `english_text.py` & `spanish_text.py`: Language modules for English and Spanish support.
- `exec_eng/` & `exec_esp/`: Folders containing the English and Spanish executables, respectively.

## Usage
To start using the Kucoin Simple Bot:
- On Windows, navigate to either the `exec_eng/` or `exec_esp/` directory and run the executable that matches your operating system and language preference.
- On MacOS, you must first create the executable by running `executable.py`
## Contributions
Contributions to the Kucoin Simple Bot are welcome. Please ensure that you update tests as appropriate and adhere to the existing coding style.

Thank you for your interest in the Kucoin Simple Bot. This bot represents a significant effort in automating trading strategies and providing a user-friendly interface for traders worldwide.