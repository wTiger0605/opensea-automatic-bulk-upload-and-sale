#!/usr/bin/python
# app/utils/user.py


"""
@author: Maxime Dréan.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2022 Maxime Dréan. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


# Python internal imports.
from .colors import GREEN, RED, YELLOW, RESET

# Python default imports.
from os.path import abspath, isfile
from requests import get
from glob import glob


def check_version(version) -> str:
    """Check for the new version of the script."""
    try:  # Try ot get the version of the bot.
        last_release = get('https://pastebin.com/raw/kRqGGUkc').text
        return f'\n{YELLOW}Version {last_release} is available!{RESET}' \
            if version != last_release else ''
    except Exception:  #SSL error.
        return f'{YELLOW}Unable to get the latest version.{RESET}'


def choose_wallet() -> int:
    """Ask the user for a wallet to connect to OpenSea."""
    wallets = ['MetaMask', 'Coinbase Wallet']  # New wallets will be added.
    while True:
        print(f'{YELLOW}\nChoose a wallet:')
        [print(f'{wallets.index(wallet) + 1} - {wallet}'
               ) for wallet in wallets]  # Print wallets.
        answer = input('Wallet: ')  # Get the user answer.
        if not answer.isdigit():  # Check if answer is a number.
            print(f'{RED}Answer must be an integer.')
        elif int(answer) > len(wallets) or int(answer) <= 0:
            print(f'{RED}Wallet doesn\'t exist.')
        else:  # Return the name of wallet with a function format.
            return wallets[int(answer) - 1]


def read_file(file_: str, question: str) -> str:
    """Read file or ask for data to write in text file."""
    if not isfile(abspath(f'assets/{file_}.txt')):
        open(abspath(f'assets/{file_}.txt'), 'a')  # If file doesn't exist.
    with open(abspath(f'assets/{file_}.txt'), 'r+', encoding='utf-8') as file:
        text = file.read()  # Read the file.
        if text != '':  # If the file is not empty.
            return text
        text = input(question)  # Ask the question.
        if text != '':  # If answer is not empty.
            if input(f'Do you want to save your {file_.replace("_", " ")}'
                     ' in a text file? (y/n) ').lower() != 'y':
                print(f'{YELLOW}Not saved.{RESET}')
            else:
                file.write(text)  # Write the text in file.
                print(f'{GREEN}Saved.{RESET}')
        return text


def perform_action() -> list:
    """Suggest multiple actions to the user."""
    while True:
        [print(string) for string in [
            f'{YELLOW}\nChoose an action to perform:{RESET}',
            '1 - Upload and sell NFTs (18 details/NFT).',
            '2 - Upload NFTs (12 details/NFT).', '3 - Sell '
            'NFTs (9 details/NFT including 3 autogenerated).',
            '4 - Delete NFTs (1 detail/NFT).']]
        number = input('Action number: ')
        if number.isdigit() and 0 < int(number) <= 4:
            return [[1, 2], [1], [2], [3]][int(number) - 1]
        print(f'{RED}Answer must be a strictly positive integer.{RESET}')


def recaptcha_solver() -> int:
    """Suggest multiple reCAPTCHA solver to the user."""
    while True:
        [print(string) for string in [
            f'{YELLOW}\nChoose a reCAPTCHA solver:{RESET}',
            '1 - Manual solver.', '2 - Automatic solver using Yolov5.',
            '3 - Automatic solver using 2Captcha.',
            '4 - No reCAPTCHA (OpenSea exploit - do not report!).']]
        number = input('Action number: ')
        if number.isdigit() and 0 < int(number) <= 4:
            return int(number), read_file(
                'two_captcha_key', 'What is your 2Captcha API key? '
            ) if number == '3' else ''
        print(f'{RED}Answer must be a strictly positive integer.{RESET}')


def choose_browser(solver: int, password: str, recovery_phrase: str) -> int:
    """Ask the user for a browser."""
    browsers = ['ChromeDriver (Google Chrome)' + (
        ' - No headless mode.\n    Must used in foreground, you see what\'s '
        'happening.' if solver != 1 and password != '' and recovery_phrase
        != '' else '.'), 'GeckoDriver (Mozilla Firefox)' + (
            '- Headless mode.\n    Can be used in background while '
            'doing something else.' if solver != 1 else '.')]
    while True:
        print(f'{YELLOW}\nChoose a browser:')
        [print(f'{browsers.index(browser) + 1} - {browser}'
               ) for browser in browsers]  # Print browsers.
        answer = input('Browser: ')  # Get the user answer.
        if not answer.isdigit():  # Check if answer is a number.
            print(f'{RED}Answer must be an integer.')
        elif int(answer) > len(browsers) or int(answer) <= 0:
            print(f'{RED}Browser doesn\'t exist.')
        else:  # Return the index of browser.
            return int(answer) - 1


def data_file() -> str:
    """Read the data folder and extract JSON, CSV and XLSX files."""
    while True:
        file_number, files_list = 0, []
        print(f'{YELLOW}\nChoose your file:{RESET}\n0 - Browse a file on PC.')
        for files in [glob(f'data/{extension}')  # Files of the data folder.
                      for extension in ['*.json', '*.csv', '*.xlsx']]:
            for file in files:
                file_number += 1
                files_list.append(file)
                print(f'{file_number} - {file}')
        answer = input('File number: ')
        if not answer.isdigit():  # Check if answer is a number.
            print(f'{RED}Answer must be an integer.{RESET}')
        elif int(answer) == 0:  # Browse a file on PC.
            print(f'{YELLOW}Browsing on your computer...{RESET}')
            from tkinter import Tk  # Tkinter module: pip install tk
            from tkinter.filedialog import askopenfilename
            Tk().withdraw()  # Hide Tkinter tab.
            return askopenfilename(filetypes=[('', '.json .csv .xlsx')])
        elif int(answer) <= len(files_list):
            return files_list[int(answer) - 1]  # Return path of file.
