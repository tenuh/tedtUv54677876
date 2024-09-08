from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Token bot 
TOKEN = 'YOUR_BOT_TOKEN'
active_chats = {}

# Daftar kata-kata yg ingin di banned
FORBIDDEN_WORDS = ['kata1', 'kata2', 'kata3']

def contains_forbidden_words(text: str) -> bool:
    """Memeriksa apakah teks mengandung kata-kata terlarang."""
    for word in FORBIDDEN_WORDS:
        if re.search(rf'\b{word}\b', text, re.IGNORECASE):
            return True
    return False

def start(update: Update, context: CallbackContext) -> None:
    """Menangani perintah /start."""
    update.message.reply_text('Selamat datang di bot chat anonymous! Kirimkan pesan Anda dan saya akan mencocokkannya dengan pengguna lain.')

def logout(update: Update, context: CallbackContext) -> None:
    """Menangani perintah /logout."""
    user_id = update.message.from_user.id
    if user_id in active_chats:
        del active_chats[user_id]
        update.message.reply_text('Anda telah keluar dari sesi chat anonim.')
    else:
        update.message.reply_text('Anda tidak sedang dalam sesi chat anonim.')

def handle_message(update: Update, context: CallbackContext) -> None:
    """Menangani pesan yang dikirim oleh pengguna."""
    user_id = update.message.from_user.id
    user_message = update.message.text
  
    if contains_forbidden_words(user_message):
        update.message.reply_text('Pesan Anda mengandung kata-kata terlarang dan tidak akan dikirim.')
        return

    if user_id not in active_chats:
        active_chats[user_id] = user_message
        update.message.reply_text('Anda terhubung dengan seseorang. Kirimkan pesan untuk memulai chat.')
    else:
        other_user_id = None
        for uid in active_chats:
            if uid != user_id:
                other_user_id = uid
                break

        if other_user_id is not None:
            context.bot.send_message(chat_id=other_user_id, text=f'Pesan dari pengguna lain: {user_message}')
            del active_chats[user_id]
            update.message.reply_text('Pesan Anda telah dikirim. Tunggu balasan dari pengguna lain.')
        else:
            update.message.reply_text('Tidak ada pengguna lain yang tersedia saat ini. Coba lagi nanti.')

def main() -> None:
    """Menjalankan bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('logout', logout))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
