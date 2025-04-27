# DnD Discord Bot

A Discord bot for running Dungeons & Dragons games. It provides dice rolling, reminders, custom weapons, lookups, character management, and combat features—all accessible via slash commands.

---

## 🔗 Installation

1. **Invite the bot** to your server using the following link:
   
   https://discord.com/oauth2/authorize?client_id=1359588199910871060

2. **Clone the repository**:
   ```bash
   git clone https://github.com/YourUsername/your-dnd-bot.git
   cd your-dnd-bot
   ```

3. **Set up environment variables**:
   - Create an empty `.env` file in the project root.
   - Add the bot token provided to you:
     ```ini
     DISCORD_BOT_TOKEN=TheAPIKEYPROVIDED
     ```
    - If you do not have a bot token please reach out to one of the developers on how you can get one or if we need to run the bot for you.

4. **Create and activate a virtual environment**:

   **Linux / macOS**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows (PowerShell)**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the bot**:
   ```bash
   # From the project root:
   python run_api.py
   python run_bot.py
   # or use python3 if needed:
   python3 run_api.py
   python3 run_bot.py
   ```

---

## 🚀 Features & Commands

### Dice Rolling
- **`/roll <dice>`**: Roll any number of dice (e.g., `/roll 1d20`, `/roll 3d6`).

### Reminders
- **`/reminder <date> <time> <message>`**: Schedule a reminder (e.g., `/reminder 2025-05-01 14:00 Check traps`).

### Custom Weapons
- **`/customweapon <name> <damage> <range>`**: Create a custom weapon (e.g., `/customweapon "Elven Longbow" 1d8 150`).

### Lookup
- **`/lookup <name> <type>`**: Lookup weapons, monsters, or custom weapons (e.g., `/lookup dragon monster`).

### Character Management
- **`/create_character <name> <hp> <ac> <level> <race> <class>`**: Create a new character.
- **`/update_character <name> <hp> <ac> <level> <race> <class>`**: Update an existing character (name is immutable).
- **`/delete_character <name>`**: Delete a character by name.
- **`/view_character <name>`**: View character details.

### Combat
- **`/attack <target> <damage_dice>`**: Attack a character; if the HP drops to 0 or below, the bot @mentions the player to notify them of their character's demise.

---

## 🛠️ Local Development

- **API module**: The bot requires a running API. Reach out to the project maintainer to obtain the API source or access details.
- **Environment**: Ensure `DISCORD_BOT_TOKEN` is set in `.env`.
- **Dependencies**: All required packages are listed in `requirements.txt`.
- **Running**: Launch `run_api.py` first to start the API, then `run_bot.py` to connect the Discord client.

---

## ⚠️ Known Issues

- There is a current bug in how the weapons and monsters database displays JSON responses. This issue is tedious to fix and may not be resolved immediately, but all core features remain operational.

---

## 📣 Experimental Status

This bot is in **experimental** stages. It does not yet cover every feature a production-ready Discord bot might offer. Use with caution and feel free to contribute improvements!

---

## 🤝 Contributing

Pull requests, issues, and feature suggestions are welcome! Please open issues on the repository or contact the maintainer directly.

---

*Happy adventuring!*

