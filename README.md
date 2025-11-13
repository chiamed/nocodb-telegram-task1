# 🚀 NocoDB Telegram Task

This project is part of the University Racing Team software area selection task.  
It demonstrates the ability to deploy and interact with NocoDB using Docker, REST APIs, and a Telegram Bot.

---

## 🧩 Project Structure
nocodb-telegram-task/
├── bot/ # Telegram bot that interacts with NocoDB API
├── scripts/ # Python script to import JSON data into NocoDB
├── data/ # Example data in JSON format
├── docker-compose.yml # NocoDB container setup
├── .env.example # Environment variables (copy to .env)
├── requirements.txt # Python dependencies
└── README.md

---

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/<your-username>/nocodb-telegram-task.git
cd nocodb-telegram-task

### 2. Create .env
Copy .env.example to .env and fill in your tokens and URLs.

### 3. Start NocoDB
docker-compose up -d
Access NocoDB at: http://localhost:8080

### 4. Import example data
python3 scripts/import_data.py

### 5. Start the telegram bot
python3 bot/bot.py

