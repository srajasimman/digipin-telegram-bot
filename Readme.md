## 📍 DIGIPIN Telegram Bot

A **Telegram bot** that encodes and decodes [DIGIPIN](https://www.indiapost.gov.in/vas/Pages/digipin.aspx) – an open-source, geo-coded addressing system developed by **India Post** in collaboration with **IIT Hyderabad** and **NRSC, ISRO**.

DIGIPIN enables **Address-as-a-Service (AaaS)** by linking precise geographic locations to a unique 10-character digital identifier. This bot provides a simple chat interface for encoding and decoding DIGIPINs.


## 🧠 What is DIGIPIN?

DIGIPIN is a **10-digit alphanumeric code** that represents a geographic point (latitude & longitude). Unlike traditional postal codes or addresses, DIGIPIN is **location-precise, digital-first, and unambiguous**.

| Feature | Description |
| --- | --- |
| 📡 Geo-Precision | Based on latitude & longitude grid division |
| 🔄 Bidirectional | Encode coordinates → DIGIPIN, Decode DIGIPIN → coordinates |
| 🌐 Open & Offline | No need for network lookup or third-party services |
| 🛰 Backed by | India Post, IIT Hyderabad, and NRSC, ISRO |

> 🔗 Learn more: India Post - [DIGIPIN](https://www.indiapost.gov.in/vas/Pages/digipin.aspx)
> 


## 🧭 Bot Features

### ✅ Supported Commands

| Command | Description |
| --- | --- |
| `/encode <lat> <lon>` | Encode coordinates to DIGIPIN |
| `/decode <digipin>` | Decode DIGIPIN into latitude/longitude |
| 📍 Location Share | Send GPS location, get back a DIGIPIN |


## 📦 Local Setup (Python)

### 1. Clone & Setup

```bash
git clone https://github.com/srajasimman/digipin-telegram-bot.git
cd digipin-telegram-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create `.env`

```bash
# .env
BOT_TOKEN=your_telegram_bot_token_here
```

### 3. Run the bot

```bash
python digipin_bot.py
```


## 🐳 Dockerized Deployment

### 📁 Dockerfile

A minimal image built from `python:3.11-slim`.

### 🔨 Build and Run

```bash
docker build -t digipin-bot .
docker run -d --env-file .env --name digipin_bot digipin-bot
```

### 🔒 Environment

`.env` is used to inject the bot token securely:

```bash
BOT_TOKEN=your_bot_token
```


## 📡 Example Usage

### Encoding a location:

```bash
/encode 28.6139 77.2090
```

🔁 Output:

```yaml
DIGIPIN: J5C-K3F-PM8
```


### Decoding a DIGIPIN:

```bash
/decode J5C-K3F-PM8
```

🔁 Output:

```yaml
Latitude: 28.613875
Longitude: 77.209375
```


### Shared Location:

Just drop your 📍 location in chat — the bot returns your DIGIPIN.


## 📁 Project Structure

```
.
├── digipin_bot.py       # Main bot logic
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker container setup
└── .env                 # Bot secret token (not checked in)
```


## ⚖️ License

This project is licensed under the [MIT License](/LICENSE).


## 🙏 Acknowledgements

- 🇮🇳 **India Post** for DIGIPIN concept and implementation
- 🛰 **IIT Hyderabad** & **NRSC, ISRO** for geospatial tech support
- 💬 Built using [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)