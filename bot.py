import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ISI_TOKEN_KAMU")
GROUP_ID = int(os.environ.get("GROUP_ID", "-1001234567890"))
GROUP_LINK = "https://t.me/+d-W_foAg0AthNTU1x"
FILE_TO_SEND = "FILE_ID_ATAU_URL_FILE"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(GROUP_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text("✅ Kamu sudah join! Ini file-nya:")
            await context.bot.send_document(update.effective_chat.id, FILE_TO_SEND)
            return
    except Exception:
        pass

    keyboard = [
        [InlineKeyboardButton("📥 Masuk Grup Telegram", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ Saya Sudah Join, Verifikasi!", callback_data="verify")]
    ]
    await update.message.reply_text(
        "Halo! Untuk dapat file, wajib join grup dulu ya.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        member = await context.bot.get_chat_member(GROUP_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text("✅ Verifikasi berhasil! File dikirim:")
            await context.bot.send_document(query.message.chat_id, FILE_TO_SEND)
        else:
            await query.edit_message_text("❌ Kamu belum join. Join dulu lalu klik verifikasi lagi.")
    except Exception:
        await query.edit_message_text("❌ Belum terdeteksi join. Coba lagi setelah join grup.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
    app.run_polling()

if __name__ == "__main__":
    main()
