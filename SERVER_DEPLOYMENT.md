# 🚀 راهنمای استقرار سرور - ربات تلگرام هشتونیم

## روش ۱: استقرار خودکار (پیشنهادی)

### قدم ۱: دانلود و اجرای اسکریپت نصب
```bash
# دانلود اسکریپت
wget https://raw.githubusercontent.com/hashtonimco-creator/telegram_bot/main/setup_server.sh

# اجازه اجرا
chmod +x setup_server.sh

# اجرای اسکریپت
sudo ./setup_server.sh
```

### قدم ۲: تنظیم توکن ربات
```bash
# ویرایش فایل bot.py
sudo nano /home/hashtonim/telegram_bot/bot.py

# در فایل، این دو متغیر را تنظیم کنید:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
SUPER_ADMIN_ID = 123456789  # شناسه عددی شما
```

### قدم ۳: راه‌اندازی سرویس
```bash
# شروع سرویس
sudo systemctl start hashtonim_bot.service

# بررسی وضعیت
sudo systemctl status hashtonim_bot.service

# مشاهده لاگ‌ها
sudo journalctl -u hashtonim_bot.service -f
```

---

## روش ۲: نصب دستی

### قدم ۱: آماده‌سازی سرور
```bash
# به‌روزرسانی سیستم
sudo apt update && sudo apt upgrade -y

# نصب ابزارهای مورد نیاز
sudo apt install git python3-pip python3-venv screen -y
```

### قدم ۲: ایجاد کاربر (اختیاری)
```bash
# ایجاد کاربر hashtonim
sudo useradd -m -s /bin/bash hashtonim

# تغییر به کاربر hashtonim
sudo su - hashtonim
```

### قدم ۳: دانلود پروژه
```bash
# کلون کردن پروژه
git clone https://github.com/hashtonimco-creator/telegram_bot.git
cd telegram_bot
```

### قدم ۴: نصب وابستگی‌ها
```bash
# ایجاد محیط مجازی
python3 -m venv .venv

# فعال‌سازی محیط مجازی
source .venv/bin/activate

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### قدم ۵: تنظیمات
```bash
# ویرایش فایل bot.py
nano bot.py

# تنظیم متغیرها:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
SUPER_ADMIN_ID = 123456789
```

### قدم ۶: اجرا

#### روش A: اجرای ساده با screen
```bash
# ایجاد جلسه screen
screen -S hashtonim_bot

# اجرای ربات
python bot.py

# خروج از screen (Ctrl+A, سپس D)
```

#### روش B: اجرا با systemd (پیشنهادی)
```bash
# کپی فایل سرویس
sudo cp hashtonim_bot.service /etc/systemd/system/

# فعال‌سازی سرویس
sudo systemctl daemon-reload
sudo systemctl enable hashtonim_bot.service
sudo systemctl start hashtonim_bot.service
```

---

## 🔧 مدیریت سرویس

### دستورات مفید systemd:
```bash
# شروع سرویس
sudo systemctl start hashtonim_bot.service

# توقف سرویس
sudo systemctl stop hashtonim_bot.service

# راه‌اندازی مجدد
sudo systemctl restart hashtonim_bot.service

# وضعیت سرویس
sudo systemctl status hashtonim_bot.service

# فعال‌سازی خودکار در بوت
sudo systemctl enable hashtonim_bot.service

# غیرفعال‌سازی خودکار
sudo systemctl disable hashtonim_bot.service
```

### مشاهده لاگ‌ها:
```bash
# لاگ‌های زنده
sudo journalctl -u hashtonim_bot.service -f

# لاگ‌های اخیر
sudo journalctl -u hashtonim_bot.service -n 50

# لاگ‌های امروز
sudo journalctl -u hashtonim_bot.service --since today
```

---

## 🔄 به‌روزرسانی

### به‌روزرسانی کد:
```bash
# توقف سرویس
sudo systemctl stop hashtonim_bot.service

# به‌روزرسانی کد
cd /home/hashtonim/telegram_bot
git pull origin main

# راه‌اندازی مجدد
sudo systemctl start hashtonim_bot.service
```

---

## 🛠️ عیب‌یابی

### مشکلات رایج:

#### ۱. خطای "chat not found"
- ربات سعی می‌کند به کاربری پیام بفرستد که ربات را start نکرده
- حل شده با error handling در کد جدید

#### ۲. خطای "ProxyError" یا مشکل اتصال
- مشکل اتصال به اینترنت یا API تلگرام
- ربات خودکار restart می‌شود

#### ۳. خطای "Permission denied"
- مجوزهای فایل را بررسی کنید:
```bash
sudo chown -R hashtonim:hashtonim /home/hashtonim/telegram_bot
chmod +x /home/hashtonim/telegram_bot/bot.py
```

### بررسی وضعیت:
```bash
# بررسی پورت‌های باز
sudo netstat -tlnp | grep python

# بررسی فرآیندهای پایتون
ps aux | grep python

# بررسی فضای دیسک
df -h

# بررسی حافظه
free -h
```

---

## 📞 پشتیبانی

در صورت بروز مشکل:
1. لاگ‌های سرویس را بررسی کنید
2. وضعیت اتصال اینترنت را چک کنید  
3. توکن ربات را مجدداً تأیید کنید
4. با تیم فنی تماس بگیرید
