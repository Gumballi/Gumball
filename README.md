# Շђคภ๏ร-קг๏ (Thanos-Pro)

[![GitHub Stars](https://img.shields.io/github/stars/Gumballi/Gumball?style=social)](https://github.com/Gumballi/Gumball)
[![GitHub Forks](https://img.shields.io/github/forks/Gumballi/Gumball?style=social)](https://github.com/Gumballi/Gumball)
[![License](https://img.shields.io/github/license/Gumballi/Gumball)](LICENSE)

**Thanos-Pro** is a high-performance, feature-rich Telegram Userbot based on the [Telethon](https://github.com/LonamiWebs/Telethon) library. It allows you to automate your personal Telegram account with a modular plugin system, providing tools for group management, media processing, and account security.

---

## 🚀 Features

- **Multi-Client Support:** Run up to 5 Telegram sessions simultaneously.
- **Group Management:** Automated tools for moderation (ban, mute, promote, anti-flood).
- **Security:** Built-in PM Permit system to protect your private messages.
- **Media Tools:** Downloaders for YouTube, Instagram, and more; image editing and file conversion.
- **Extensible:** Easily add new features via the modular plugin system.

---

## 🛠 Installation

### 1. Prerequisites
- Python 3.9 or higher
- A Telegram `APP_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org)
- A `DATABASE_URL` (PostgreSQL recommended)

### 2. Deployment

#### Local / VPS
```bash
git clone https://github.com/Gumballi/Gumball.git
cd Gumball
pip3 install -r requirements.txt
# Fill your variables in config.py
python3 -m THANOSPRO
```

#### Docker
```bash
docker build -t thanospro .
docker run thanospro
```

---

## ⚙️ Configuration

Create a `config.py` file or set the following environment variables:

| Variable | Description |
| :--- | :--- |
| `APP_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API Hash |
| `BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `THANOSPRO_SESSION` | Telethon String Session |
| `DATABASE_URL` | PostgreSQL Database URI |

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

---

## ⚖️ Disclaimer

- This project is for educational and fun purposes only.
- The developers are not responsible for any account bans or misuse of this bot.
- **Self-botting is against Telegram's Terms of Service.** Use at your own risk.

---

## 📜 Credits

Developed with ❤️ by [Gumballi](https://github.com/Gumballi).
Special thanks to the Telethon community and contributors.
