# GoodSenderPro
ٌGood Sender ZedSoftOfficial

Description (English)

Good Sender is a Python script that automatically finds good.txt files in a selected directory and its subdirectories. It reads the content of these files and sends each unique line to a Telegram bot. It also includes an optional delete mode to remove good.txt files after sending.

Features:

Automatic search for good.txt files.

Sends unique lines to Telegram.

Supports both manual and config file (config.txt) input for Telegram bot credentials.

GUI directory selection (if tkinter is installed) or manual input.

Optional delete mode to remove files after sending.

Countdown timer for the next scan cycle.

Color-coded console output.

How to Use:

Clone the repository:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

Install dependencies:

pip install -r requirements.txt

Run the script:

python main.py

Select an option:

1 Use config.txt for Telegram credentials.

2 Enter Token & Chat ID manually.

3 Enable delete mode (files will be deleted after sending).

4 Exit the script.

Choose a directory to monitor.

The script will automatically send good.txt contents to Telegram every 60 seconds.

Configuration (config.txt format):

TOKEN=your_bot_token
CHAT_ID=your_chat_id

Build Executable:

To create an executable file:

pyinstaller --onefile --noconsole main.py

The executable will be found in the dist/ directory.

Download EXE:

Download here

توضیحات (فارسی)

Good Sender یک اسکریپت پایتون است که به صورت خودکار فایل‌های good.txt را در یک پوشه و زیرپوشه‌های آن پیدا کرده و هر خط جدید را به ربات تلگرام ارسال می‌کند. همچنین دارای یک حالت حذف است که بعد از ارسال فایل good.txt را پاک می‌کند.

ویژگی‌ها:

جستجوی خودکار فایل‌های good.txt.

ارسال خطوط یکتا به تلگرام.

امکان وارد کردن اطلاعات ربات تلگرام به صورت دستی یا از طریق config.txt.

انتخاب پوشه با رابط گرافیکی (در صورت نصب tkinter) یا ورودی دستی.

حالت حذف برای پاک کردن فایل بعد از ارسال.

تایمر شمارش معکوس برای اسکن‌های دوره‌ای.

خروجی کنسول رنگی.

روش استفاده:

کلون کردن مخزن:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

نصب وابستگی‌ها:

pip install -r requirements.txt

اجرای اسکریپت:

python main.py

انتخاب گزینه:

1 استفاده از config.txt برای اطلاعات ربات تلگرام.

2 وارد کردن توکن و چت آی‌دی به صورت دستی.

3 فعال‌سازی حالت حذف (پاک کردن فایل پس از ارسال).

4 خروج از برنامه.

انتخاب پوشه برای نظارت.

اسکریپت هر 60 ثانیه محتوای good.txt را به تلگرام ارسال می‌کند.

تنظیمات (config.txt):

TOKEN=توکن_ربات_شما
CHAT_ID=چت_آی_دی_شما

ساخت فایل اجرایی (exe):

pyinstaller --onefile --noconsole main.py

فایل exe در پوشه dist/ قرار خواهد گرفت.

دانلود نسخه اجرایی:

دانلود از اینجا

