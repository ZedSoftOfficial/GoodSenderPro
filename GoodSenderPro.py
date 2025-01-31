import os
import time
import requests
import sys

try:
    import tkinter as tk
    from tkinter import filedialog
    GUI_ENABLED = True
except ImportError:
    GUI_ENABLED = False  

def read_config():
    config = {}
    if not os.path.exists("config.txt"):
        print("\033[1;31mError: config.txt not found! Returning to menu...\033[0m")
        time.sleep(2)
        return None

    try:
        with open("config.txt", "r") as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=')
                    config[key] = value
    except Exception as e:
        print(f"\033[1;31mError reading config file: {e}. Returning to menu...\033[0m")
        time.sleep(2)
        return None

    if "TOKEN" not in config or "CHAT_ID" not in config:
        print("\033[1;31mError: config.txt is missing TOKEN or CHAT_ID. Returning to menu...\033[0m")
        time.sleep(2)
        return None

    return config

def send_to_telegram(token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"\033[1;32m good was sent to your telegram\033[0m") 
    except requests.exceptions.RequestException as e:
        print(f"\033[1;31mError sending message: {e}\033[0m")

def find_good_files(directory):
    good_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() == "good.txt":
                good_files.append(os.path.join(root, file))
    return good_files

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;32mGood Sender ZedSoftOfficial\033[0m")  
    print("\033[1;34mT.me/Sirer\033[0m")  
    print("\033[1;34mT.me/ZedSoftOfficial\033[0m")  
    print("\n" + "="*50 + "\n")  

def select_directory():
    if GUI_ENABLED:
        root = tk.Tk()
        root.withdraw()  
        directory = filedialog.askdirectory(title="Select Directory to Monitor")
        return directory
    else:
        directory = input("Enter the directory path manually: ").strip()
        if os.path.exists(directory):
            return directory
        else:
            print("\033[1;31mInvalid directory! Returning to menu...\033[0m")
            time.sleep(2)
            return None

def delete_good_file(file_path):
    try:
        os.remove(file_path)
        print(f"\033[1;32mFile deleted: {file_path}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError deleting file {file_path}: {e}\033[0m")

# تابع اصلی برنامه
def main():
    delete_mode = False 
    sent_lines = set()  

    while True:
        print_header()
        print("Choose an option:")
        print("1 - Use config file (config.txt)")
        print("2 - Enter Token and Chat ID manually")
        print("3 - Delete mode (delete good.txt after sending-Run Administrator)")
        print("4 - Exit")
        
        choice = input("Enter 1, 2, 3 or 4: ").strip()

        if choice == "1":
            config = read_config()
            if not config:
                continue  
            token = config["TOKEN"]
            chat_id = config["CHAT_ID"]
        elif choice == "2":
            token = input("Enter your Telegram Bot Token: ").strip()
            chat_id = input("Enter your Telegram Chat ID: ").strip()
        elif choice == "3":
            delete_mode = True
            print("\033[1;32mDelete mode enabled. Files will be deleted after sending.\033[0m")
            token = input("Enter your Telegram Bot Token: ").strip()
            chat_id = input("Enter your Telegram Chat ID: ").strip()
        elif choice == "4":
            print("\033[1;33mExiting...\033[0m")
            sys.exit()
        else:
            print("\033[1;31mInvalid choice. Please try again.\033[0m")
            time.sleep(2)
            continue  

        print(f"\033[1;32mUsing Token: {token[:6]}...{token[-4:]}\033[0m")  
        print(f"\033[1;32mUsing Chat ID: {chat_id}\033[0m")
        
        os.system('cls' if os.name == 'nt' else 'clear')

        directory = select_directory()
        if not directory:
            print("\033[1;31mNo directory selected. Returning to menu...\033[0m")
            time.sleep(2)
            continue 

        print(f"\033[1;36mMonitoring for good.txt files in {directory}...\033[0m")  

        while True:
            good_files = find_good_files(directory)

            for file_path in good_files:
                try:
                    with open(file_path, "r", encoding="utf-16le") as f:
                        for line in f:
                            line = line.strip()
                            if line and line not in sent_lines:
                                send_to_telegram(token, chat_id, line)
                                sent_lines.add(line)  

                    if delete_mode:
                        delete_good_file(file_path)

                except Exception as e:
                    print(f"\033[1;31mError processing file {file_path}: {e}\033[0m")

            for remaining in range(60, 0, -1):
                sys.stdout.write(f"\r\033[1;33mWaiting {remaining} seconds...\033[0m")  
                sys.stdout.flush()
                time.sleep(1)
            print("\n")

if __name__ == "__main__":
    main()
