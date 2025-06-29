
import json
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes

BOT_TOKEN = "7585170845:AAHdsY0_eBGSUab13LwqlzgcY7D3GVHShc8"
ADMIN_IDS = ["7902569445"]  # replace with your actual Telegram user ID
DATA_FILE = "users.json"

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) + "-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "id": update.effective_user.id,
            "access_key": generate_key(),
            "balance": 0,
            "status": "limited"
        }
        save_users(users)

    u = users[user_id]
    keyboard = [
        [InlineKeyboardButton("📋 Copy Key", callback_data="copy")],
        [InlineKeyboardButton("💵 Buy Credit", url="https://t.me/CPMKaitoToolBot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"🔐 *Welcome to CPMKaitoToolBot*\n\n" \
           f"🔑 Access Key: `{u['access_key']}`\n" \
           f"🆔 Telegram ID: `{u['id']}`\n" \
           f"💰 Balance: `{u['balance']}`\n" \
           f"⚙️ Status: `{u['status']}`"
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def balance(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()

    if user_id in users:
        bal = users[user_id]["balance"]
        await update.message.reply_text(f"💰 Your balance: {bal}")
    else:
        await update.message.reply_text("❌ You are not registered. Use /start first.")

async def block(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ Admins only.")
        return

    try:
        target_id = context.args[0]
    except:
        await update.message.reply_text("Usage: /block <user_id>")
        return

    users = load_users()
    if target_id in users:
        users[target_id]["status"] = "blocked"
        save_users(users)
        await update.message.reply_text(f"⛔ User {target_id} blocked.")
    else:
        await update.message.reply_text("❌ User not found.")

async def unblock(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ Admins only.")
        return

    try:
        target_id = context.args[0]
    except:
        await update.message.reply_text("Usage: /unblock <user_id>")
        return

    users = load_users()
    if target_id in users:
        users[target_id]["status"] = "limited"
        save_users(users)
        await update.message.reply_text(f"✅ User {target_id} unblocked.")
    else:
        await update.message.reply_text("❌ User not found.")

async def unlimited(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ Admins only.")
        return

    try:
        target_id = context.args[0]
    except:
        await update.message.reply_text("Usage: /unlimited <user_id>")
        return

    users = load_users()
    if target_id in users:
        users[target_id]["status"] = "unlimited"
        save_users(users)
        await update.message.reply_text(f"🔓 {target_id} is now UNLIMITED.")
    else:
        await update.message.reply_text("❌ User not found.")

async def limited(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ Admins only.")
        return

    try:
        target_id = context.args[0]
    except:
        await update.message.reply_text("Usage: /limited <user_id>")
        return

    users = load_users()
    if target_id in users:
        users[target_id]["status"] = "limited"
        save_users(users)
        await update.message.reply_text(f"🔐 {target_id} is now LIMITED.")
    else:
        await update.message.reply_text("❌ User not found.")

async def broadcast(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ Admins only.")
        return

    msg = ' '.join(context.args)
    users = load_users()
    count = 0

    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 {msg}")
            count += 1
        except:
            pass
    await update.message.reply_text(f"📬 Sent to {count} users.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("block", block))
    app.add_handler(CommandHandler("unblock", unblock))
    app.add_handler(CommandHandler("unlimited", unlimited))
    app.add_handler(CommandHandler("limited", limited))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("🤖 CPMKaitoToolBot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
