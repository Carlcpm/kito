from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json, os, random, string

TOKEN = "7585170845:AAHdsY0_eBGSUab13LwqlzgcY7D3GVHShc8"
USER_FILE = "users.json"

def load_users():
    return json.load(open(USER_FILE)) if os.path.exists(USER_FILE) else {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def generate_key():
    return "FREE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    users = load_users()

    if user_id not in users:
        key = generate_key()
        users[user_id] = {
            "key": key,
            "status": "active",
            "balance": "Unlimited"
        }
        save_users(users)
        msg = f"🎟️ Welcome! Here's your FREE key:\n\n🔑 Key: `{key}`\nStatus: ✅ Active"
    else:
        user = users[user_id]
        msg = f"🔑 You already have a key:\nKey: `{user['key']}`\nBalance: {user['balance']}"

    update.message.reply_text(msg, parse_mode="Markdown")

def balance(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    users = load_users()
    if user_id not in users:
        update.message.reply_text("❌ You don't have a key yet. Use /start to generate one.")
        return

    user = users[user_id]
    msg = (
        "🧾 Your Account Info\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 ID: {user_id}\n"
        f"🔑 Key: {user['key']}\n"
        f"💰 Balance: {user['balance']}\n"
        f"🛡️ Status: ✅ {user['status']}\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    update.message.reply_text(msg)

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/start - Get your access key\n/balance - Check your balance\n/help - List of commands")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
