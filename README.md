# 🚀 Telegram Bot + NocoDB Integration

This project is part of the University Racing Team software area selection task. It demonstrates how to:

- Deploy **NocoDB** using Docker
- Import data into it through a Python script
- Manage relational tables
- Interact with the database via a **Telegram bot**

---

## 🧩 Project Structure
```
nocodb-telegram-task/
├── bot/                         # Telegram bot logic
│   ├── bot.py
│   └── handlers/
│       └── add_user_wizard.py   # Wizard to add a new user step-by-step
│
├── services/
│   └── helpers.py               # fetch_id_map + build_inline_keyboard
│   └── validators.py            # Validation of fields of the new user
│
├── scripts/                     # Data import module
│   └── import_data.py
│
├── data/                        # JSON example data used for import
│
├── docker-compose.yml           # Docker setup for NocoDB
├── .env.example                 # Template of environment variables
├── config.py                    # Centralized configuration loader
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔥 1. Clone the repository
```bash
git clone https://github.com/<chiamed>/nocodb-telegram-task1.git
cd nocodb-telegram-task
```

### 🔐 2. Configure Environment Variables
- Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- Fill in your tokens and URLs.

### 🐳 3. Start NocoDB with Docker
This project includes a `docker-compose.yml` that launches a fully working NocoDB instance.

```bash
docker-compose up -d
```

Once running, the NocoDB interface will be available at:
👉 **http://localhost:8080**

### 🎯 4. Import Data into NocoDB
This project includes a Python script that:

- Parses JSON files in the `/data` directory
- Creates rows through NocoDB’s REST API
- Correctly manages the relationships
- Handles record deduplication using unique keys

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the importer:
```bash
python -m scripts.import_data
```

### 🤖 5. Start the Telegram Bot
The Telegram bot communicates directly with NocoDB via its REST API.

Start it using:
```bash
python -m bot.bot
```

### Available Commands
 **`/help`**: Displays all available commands and a short description of what they do.
- **`/odg`**: Retrieves an example **Ordine del Giorno (ODG)** from the dedicated NocoDB table.
- **`/adduser`**: Starts an interactive multi-step wizard to add a new user to NocoDB. The wizard handles attributes such as:
  - Name / Surname
  - Department
  - Area
  - Entry Date
  - Sex
  - Telegram username
  - And more

### 🧪 6. Example Workflow
1. Launch NocoDB with Docker
2. Open the NocoDB UI and create tables
3. Copy `.env.example` → `.env` and fill all variables
4. Import JSON sample data:
   ```bash
   python -m scripts.import_data
   ```
5. Start the Telegram bot:
   ```bash
   python -m bot.bot
   ```
6. Interact via Telegram:
   - `/help`
   - `/odg`
   - `/adduser`

#### Example Interaction:
- **Adding a User**:
  1. Start the wizard with `/adduser`.
  2. Follow the prompts to enter details such as name, surname, email, department, and more.
  3. Confirm the entered data to save the user to the database.

- **Viewing ODG**:
  1. Use `/odg` to fetch and display the latest **Ordine del Giorno** from the database.

This workflow ensures a smooth setup and interaction with the NocoDB and Telegram bot system.

---

## 📎 Useful References

- **NocoDB Documentation**: [https://docs.nocodb.com](https://docs.nocodb.com)
- **NocoDB REST API Reference**: [https://nocodb.com/docs/product-docs/developer-resources/rest-apis](https://nocodb.com/docs/product-docs/developer-resources/rest-apis)
- **NocoDB Relationships Reference**: [https://nocodb.com/docs/product-docs/fields/field-types/links-based/links](https://nocodb.com/docs/product-docs/fields/field-types/links-based/links)
- **Telegram Bot References**:
  - [BotFather](https://core.telegram.org/bots#botfather)
  - [Python Telegram Bot Library](https://python-telegram-bot.org/)
  - [Extensions - Your First Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot)

