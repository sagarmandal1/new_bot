# 🌟 দৈনিক রুটিন আপডেট বট | Daily Routine Update Bot

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

একটি সম্পূর্ণ বাংলা টেলিগ্রাম বট যা আপনার দৈনিক, সাপ্তাহিক এবং মাসিক রুটিন পরিচালনায় সাহায্য করবে। JSON ভিত্তিক ডেটা স্টোরেজ এবং সম্পূর্ণ বাংলা ভাষা সাপোর্ট সহ।

*A complete Bengali Telegram bot for managing daily, weekly, and monthly routines with JSON-based storage and full Bengali language support.*

## 🎯 বৈশিষ্ট্যসমূহ | Features

### 👤 ব্যবহারকারী ব্যবস্থাপনা | User Management
- ✅ সহজ নিবন্ধন প্রক্রিয়া
- ✅ ব্যক্তিগত প্রোফাইল ব্যবস্থাপনা
- ✅ ভাষা নির্বাচন (বাংলা/ইংরেজি)
- ✅ নোটিফিকেশন সেটিংস

### 📋 রুটিন ব্যবস্থাপনা | Routine Management
- ✅ রুটিন তৈরি, সম্পাদনা, মুছে ফেলা
- ✅ দৈনিক, সাপ্তাহিক, মাসিক রুটিন
- ✅ স্বয়ংক্রিয় রিমাইন্ডার
- ✅ রুটিন সক্রিয়/নিষ্ক্রিয় করা
- ✅ সময় নির্ধারণ ও ট্র্যাকিং

### 🔔 বিজ্ঞপ্তি ও রিমাইন্ডার | Notifications & Reminders
- ✅ রিয়েল-টাইম নোটিফিকেশন
- ✅ কাস্টমাইজেবল রিমাইন্ডার
- ✅ দৈনিক সারসংক্ষেপ
- ✅ ইন্টারঅ্যাক্টিভ রিস্পন্স বোতাম

### 📊 রিপোর্ট ও পরিসংখ্যান | Reports & Statistics
- ✅ দৈনিক রিপোর্ট
- ✅ সাপ্তাহিক রিপোর্ট
- ✅ মাসিক রিপোর্ট
- ✅ সর্বকালের পরিসংখ্যান
- ✅ সফলতার হার গণনা

### 🔧 অ্যাডমিন প্যানেল | Admin Panel
- ✅ সিস্টেম পরিসংখ্যান
- ✅ ব্রডকাস্ট মেসেজিং
- ✅ ব্যবহারকারী তালিকা
- ✅ ট্রাবলশুটিং টুলস

### 💾 ব্যাকআপ ও পুনরুদ্ধার | Backup & Restore
- ✅ স্বয়ংক্রিয় দৈনিক ব্যাকআপ
- ✅ ম্যানুয়াল ব্যাকআপ তৈরি
- ✅ ডেটা রিস্টোর
- ✅ JSON ভিত্তিক ডেটা স্ট্রাকচার

## 🚀 ইনস্টলেশন | Installation

### ১. রিপোজিটরি ক্লোন করুন | Clone Repository
```bash
git clone https://github.com/sagarmandal1/new_bot.git
cd new_bot
```

### ২. নির্ভরতা ইনস্টল করুন | Install Dependencies
```bash
pip install -r requirements.txt
```

### ৩. কনফিগারেশন সেটআপ | Configuration Setup

`config.json` ফাইলটি সম্পাদনা করুন:

```json
{
    "bot_token": "আপনার_বট_টোকেন_এখানে",
    "admin_user_ids": [123456789],
    "timezone": "Asia/Dhaka",
    "backup_interval_hours": 24,
    "reminder_check_interval_minutes": 5,
    "default_language": "bengali",
    "supported_languages": ["bengali", "english"]
}
```

### ৪. বট চালান | Run Bot
```bash
python main.py
```

## 📁 প্রজেক্ট স্ট্রাকচার | Project Structure

```
daily-routine-bot/
│
├── main.py                 # মূল বট ফাইল
├── config.json            # কনফিগারেশন
├── requirements.txt       # নির্ভরতা তালিকা
│
├── bot/                   # বট মডিউল
│   ├── __init__.py
│   ├── handlers/          # হ্যান্ডলার মডিউল
│   │   ├── user_handlers.py
│   │   ├── routine_handlers.py
│   │   ├── report_handlers.py
│   │   └── admin_handlers.py
│   ├── services/          # সার্ভিস মডিউল
│   │   ├── user_service.py
│   │   ├── routine_service.py
│   │   ├── notification_service.py
│   │   └── backup_service.py
│   └── utils/            # ইউটিলিটি মডিউল
│       ├── database.py
│       ├── helpers.py
│       └── validators.py
│
├── data/                 # ডেটা ফাইল
│   ├── users.json
│   ├── routines.json
│   ├── reports.json
│   └── backups/
│
└── locales/              # ভাষা ফাইল
    └── bengali.py
```

## 🎮 ব্যবহারের নির্দেশনা | Usage Guide

### বেসিক কমান্ডসমূহ | Basic Commands

| কমান্ড | বর্ণনা | Description |
|---------|---------|-------------|
| `/start` | বট শুরু করুন | Start the bot |
| `/register` | নিবন্ধন করুন | Register account |
| `/menu` | মূল মেনু | Main menu |
| `/help` | সাহায্য | Help |

### রুটিন কমান্ড | Routine Commands

| কমান্ড | বর্ণনা | Description |
|---------|---------|-------------|
| `/create_routine` | নতুন রুটিন | Create routine |
| `/my_routines` | আমার রুটিন | My routines |
| `/today` | আজকের রুটিন | Today's routine |

### রিপোর্ট কমান্ড | Report Commands

| কমান্ড | বর্ণনা | Description |
|---------|---------|-------------|
| `/daily_report` | দৈনিক রিপোর্ট | Daily report |
| `/weekly_report` | সাপ্তাহিক রিপোর্ট | Weekly report |
| `/monthly_report` | মাসিক রিপোর্ট | Monthly report |

### সেটিংস | Settings

| কমান্ড | বর্ণনা | Description |
|---------|---------|-------------|
| `/settings` | সেটিংস মেনু | Settings menu |
| `/profile` | প্রোফাইল দেখুন | View profile |
| `/language` | ভাষা পরিবর্তন | Change language |

### অ্যাডমিন কমান্ড | Admin Commands

| কমান্ড | বর্ণনা | Description |
|---------|---------|-------------|
| `/admin` | অ্যাডমিন প্যানেল | Admin panel |

## 📊 ডেটা স্ট্রাকচার | Data Structure

### ব্যবহারকারী ডেটা | User Data
```json
{
  "123456789": {
    "name": "জন ডো",
    "age": 25,
    "username": "johndoe",
    "language": "bengali",
    "notifications_enabled": true,
    "created_at": "2024-01-01T00:00:00",
    "is_active": true
  }
}
```

### রুটিন ডেটা | Routine Data
```json
{
  "123456789": {
    "routine_id": {
      "name": "সকালের ব্যায়াম",
      "description": "৩০ মিনিট ব্যায়াম",
      "time": "07:00",
      "frequency": "daily",
      "is_active": true,
      "completed_count": 15,
      "created_at": "2024-01-01T00:00:00"
    }
  }
}
```

## ⚙️ কনফিগারেশন | Configuration

### বট টোকেন সেটআপ | Bot Token Setup
1. [@BotFather](https://t.me/botfather) এ যান
2. `/newbot` কমান্ড দিন
3. বট নাম ও ইউজারনেম দিন
4. প্রাপ্ত টোকেন `config.json` এ যোগ করুন

### অ্যাডমিন সেটআপ | Admin Setup
`config.json` এ আপনার ইউজার আইডি যোগ করুন:
```json
{
    "admin_user_ids": [আপনার_ইউজার_আইডি]
}
```

### টাইমজোন সেটআপ | Timezone Setup
```json
{
    "timezone": "Asia/Dhaka"
}
```

## 🔧 ট্রাবলশুটিং | Troubleshooting

### সাধারণ সমস্যা | Common Issues

#### ১. বট সাড়া দিচ্ছে না
- বট টোকেন চেক করুন
- ইন্টারনেট সংযোগ নিশ্চিত করুন
- `/start` কমান্ড পাঠান

#### ২. নোটিফিকেশন আসছে না
- `/settings` থেকে নোটিফিকেশন চালু করুন
- সময় সঠিকভাবে সেট করুন
- বট ব্লক করা আছে কিনা চেক করুন

#### ৩. ডেটা হারিয়ে গেছে
- `data/backups/` ফোল্ডার চেক করুন
- অ্যাডমিন প্যানেল থেকে ব্যাকআপ রিস্টোর করুন

#### ৪. রুটিন তৈরি হচ্ছে না
- প্রথমে `/register` দিয়ে নিবন্ধন করুন
- সঠিক ফরম্যাট অনুসরণ করুন

## 🤝 অবদান | Contributing

অবদান রাখতে চান? স্বাগতম! অনুগ্রহ করে:

1. Fork করুন
2. নতুন ব্র্যাঞ্চ তৈরি করুন (`git checkout -b feature/amazing-feature`)
3. পরিবর্তন commit করুন (`git commit -m 'Add amazing feature'`)
4. Push করুন (`git push origin feature/amazing-feature`)
5. Pull Request খুলুন

## 📝 লাইসেন্স | License

এই প্রজেক্টটি MIT লাইসেন্সের অধীনে লাইসেন্সপ্রাপ্ত। বিস্তারিত দেখুন [LICENSE](LICENSE) ফাইলে।

## 📞 সাহায্য ও সহায়তা | Support

- 📧 ইমেইল: support@dailyroutinebot.com
- 💬 টেলিগ্রাম: @DailyRoutineSupport
- 🐛 ইস্যু: [GitHub Issues](https://github.com/sagarmandal1/new_bot/issues)

## 🌟 স্বীকৃতি | Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) লাইব্রেরি
- [APScheduler](https://apscheduler.readthedocs.io/) স্কিডিউলিং এর জন্য
- সকল কন্ট্রিবিউটর ও ব্যবহারকারী

---

<div align="center">

**দৈনিক রুটিন আপডেট বট দিয়ে আপনার জীবনকে আরো সংগঠিত করুন! 🌟**

*Made with ❤️ for Bengali community*

</div>