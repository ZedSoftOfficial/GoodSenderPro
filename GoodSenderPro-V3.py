import os
import time
import requests
import sys
import traceback

try:
    import tkinter as tk
    from tkinter import filedialog
    GUI_ENABLED = True
except ImportError:
    GUI_ENABLED = False

def log_error(error_text):
    try:
        with open("error_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {error_text}\n")
    except Exception as e:
        print(f"Cannot write to log file: {e}")

def safe_input(prompt):
    try:
        return input(prompt)
    except Exception as e:
        log_error(f"Input error: {traceback.format_exc()}")
        print("\033[1;31mInput error occurred. Exiting...\033[0m")
        sys.exit(1)

def read_config():
    config = {}
    if not os.path.exists("config.txt"):
        log_error("config.txt not found.")
        print("\033[1;31mWarning: config.txt not found! Returning to menu...\033[0m")
        time.sleep(2)
        return None

    try:
        with open("config.txt", "r", encoding="utf-8") as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    except Exception as e:
        log_error(f"Error reading config file: {traceback.format_exc()}")
        print(f"\033[1;31mError reading config file: {e}. Returning to menu...\033[0m")
        time.sleep(2)
        return None

    if "TOKEN" not in config or "CHAT_ID" not in config:
        print("\033[1;31mError: config.txt is missing TOKEN or CHAT_ID. Returning to menu...\033[0m")
        time.sleep(2)
        return None

    return config

def escape_markdown_v2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

def send_to_telegram(token, chat_id, file_path, content, server_ip):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        message = (
            f"File Update Alert\n"
            f"File: {file_path}\n"
            f"-----------------------------\n"
            f"Content:\n"
            f"<pre>{content}</pre>\n"
            f"-----------------------------\n"
            f"Sent from: {server_ip}"
        )

        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        proxies = {
            "http": None,
            "https": None,
        }

        response = requests.post(url, data=payload, proxies=proxies)
        response.raise_for_status()
        print(f"\033[1;32mMessage was sent to your telegram\033[0m")
    except Exception as e:
        log_error(f"Error sending message: {traceback.format_exc()}")
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
        directory = safe_input("Enter the directory path manually: ").strip()
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
        log_error(f"Error deleting file {file_path}: {traceback.format_exc()}")
        print(f"\033[1;31mError deleting file {file_path}: {e}\033[0m")

def read_file_with_encodings(file_path, encodings=None):
    if encodings is None:
        encodings = ['utf-16le', 'utf-8', 'utf-16be', 'latin1', 'cp1252']

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            lines = content.splitlines()
            return lines
        except Exception:
            continue
    raise UnicodeDecodeError(f"Unable to decode file {file_path} with tried encodings.")

def main():
    print("Starting program... If it closes immediately, check error_log.txt")
    safe_input("Press Enter to continue...")

    delete_mode = False
    sent_lines = set()
    try:
        server_ip = requests.get("https://api.ipify.org").text.strip()
    except Exception:
        server_ip = "Unknown"

    while True:
        print_header()
        print("Choose an option:")
        print("1 - Use config file (config.txt)")
        print("2 - Enter Token and Chat ID manually")
        print("3 - Delete mode (delete good.txt after sending - Run as Administrator)")
        print("4 - Custom file mode (monitor a specific file name)")
        print("5 - Exit")

        choice = safe_input("Enter 1, 2, 3, 4 or 5: ").strip()

        if choice == "1":
            config = read_config()
            if not config:
                continue
            token = config["TOKEN"]
            chat_id = config["CHAT_ID"]
            delete_mode = False

        elif choice == "2":
            token = safe_input("Enter your Telegram Bot Token: ").strip()
            chat_id = safe_input("Enter your Telegram Chat ID: ").strip()
            delete_mode = False

        elif choice == "3":
            delete_mode = True
            print("\033[1;32mDelete mode enabled. Files will be deleted after sending.\033[0m")
            token = safe_input("Enter your Telegram Bot Token: ").strip()
            chat_id = safe_input("Enter your Telegram Chat ID: ").strip()

        elif choice == "4":
            print("Get Token and Chat ID from:")
            print("1 - config.txt file")
            print("2 - Enter manually")
            source_choice = safe_input("Choose 1 or 2: ").strip()

            if source_choice == "1":
                config = read_config()
                if not config:
                    continue
                token = config["TOKEN"]
                chat_id = config["CHAT_ID"]
            elif source_choice == "2":
                token = safe_input("Enter your Telegram Bot Token: ").strip()
                chat_id = safe_input("Enter your Telegram Chat ID: ").strip()
            else:
                print("\033[1;31mInvalid choice. Returning to menu...\033[0m")
                time.sleep(2)
                continue

            delete_choice = safe_input("Delete file after sending? (y/n): ").strip().lower()
            delete_mode = (delete_choice == 'y')
            custom_filename = safe_input("Enter the filename to monitor (e.g. target.txt): ").strip().lower()

        elif choice == "5":
            print("\033[1;33mExiting...\033[0m")
            safe_input("Press Enter to exit...")
            sys.exit()

        else:
            print("\033[1;31mInvalid choice. Please try again.\033[0m")
            time.sleep(2)
            continue

        os.system('cls' if os.name == 'nt' else 'clear')
        directory = select_directory()
        if not directory:
            print("\033[1;31mNo directory selected. Returning to menu...\033[0m")
            time.sleep(2)
            continue

        print(f"\033[1;36mMonitoring in {directory}...\033[0m")

        while True:
            if choice == "4":
                target_files = []
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.lower() == custom_filename:
                            target_files.append(os.path.join(root, file))
            else:
                target_files = find_good_files(directory)

            for file_path in target_files:
                try:
                    lines = read_file_with_encodings(file_path)
                    for line in lines:
                        line = line.strip()
                        if line == '':
                            continue  # رد کردن خطوط خالی
                        # ارسال خط به تلگرام
                        if line not in sent_lines:
                            send_to_telegram(token, chat_id, file_path, line, server_ip)
                            sent_lines.add(line)

                    if delete_mode:
                        delete_good_file(file_path)

                except Exception as e:
                    tb = traceback.format_exc()
                    log_error(f"Error processing file {file_path}:\n{tb}")
                    print(f"\033[1;31mError processing file {file_path}: {e}\033[0m")

            for remaining in range(60, 0, -1):
                sys.stdout.write(f"\r\033[1;33mWaiting {remaining} seconds...\033[0m")
                sys.stdout.flush()
                time.sleep(1)
            print("\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        tb = traceback.format_exc()
        log_error(f"Unexpected error:\n{tb}")
        print(f"\n\033[1;31mUnexpected error:\n{e}\033[0m")
        input("Press Enter to exit...")
