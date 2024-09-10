from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import random

# Token bot
TOKEN = 'YOUR_BOT_TOKEN'
active_chats = {}
waiting_users = {'male': [], 'female': []}
user_data = {}

# Daftar kata-kata yang ingin di-banned
FORBIDDEN_WORDS = ['fuck', 'hell', 'asshole']

NICKNAMES = ['Beruang', 'Tupai', 'Kucing', 'Panda'] 

def contains_forbidden_words(text: str) -> bool:
    """Memeriksa apakah teks mengandung kata-kata terlarang."""
    for word in FORBIDDEN_WORDS:
        if re.search(rf'\b{word}\b', text, re.IGNORECASE):
            return True
    return False

def start(update: Update, context: CallbackContext) -> None:
    """Menangani perintah /start."""
    user_id = update.message.from_user.id
    
    if user_id in active_chats or user_id in waiting_users['male'] or user_id in waiting_users['female']:
        update.message.reply_text('Anda sudah berada dalam sesi atau dalam antrian. Kirim /skip untuk mencari pengguna baru.')
        return

    update.message.reply_text('Selamat datang di bot chat anonim! Ketik /male jika Anda laki-laki atau /female jika Anda perempuan.')

def set_gender(update: Update, context: CallbackContext, gender: str) -> None:
    """Menangani pemilihan gender oleh pengguna."""
    user_id = update.message.from_user.id
    if user_id in user_data:
        update.message.reply_text('Anda sudah memilih gender. Kirim /skip untuk mencari pengguna baru.')
        return
    
    nickname = random.choice(NICKNAMES)
    NICKNAMES.remove(nickname) 
    user_data[user_id] = {'gender': gender, 'nickname': nickname}
    
    update.message.reply_text(f'Terima kasih telah memilih. Nama samaran Anda adalah {nickname}. Menunggu pengguna lain...')
    waiting_users[gender].append(user_id)
    find_chat_partner(user_id, context)

def male(update: Update, context: CallbackContext) -> None:
    """Menangani pemilihan gender laki-laki."""
    set_gender(update, context, 'male')

def female(update: Update, context: CallbackContext) -> None:
    """Menangani pemilihan gender perempuan."""
    set_gender(update, context, 'female')

def logout(update: Update, context: CallbackContext) -> None:
    """Menangani perintah /logout."""
    user_id = update.message.from_user.id
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id, None)
        if partner_id:
            active_chats.pop(partner_id, None)
            context.bot.send_message(chat_id=partner_id, text="Pengguna lain telah meninggalkan chat.")
        update.message.reply_text('Anda telah keluar dari sesi chat anonim.')
    else:
        remove_from_waiting(user_id)
        update.message.reply_text('Anda telah keluar dari antrian.')

def skip(update: Update, context: CallbackContext) -> None:
    """Menangani perintah /skip untuk melewati sesi chat dan mencari pengguna baru."""
    user_id = update.message.from_user.id
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id, None)
        if partner_id:
            active_chats.pop(partner_id, None)
            context.bot.send_message(chat_id=partner_id, text="Pengguna lain telah melewati sesi chat. Mencari pasangan baru...")
            waiting_users[user_data[partner_id]['gender']].append(partner_id)
            find_chat_partner(partner_id, context)

        update.message.reply_text('Anda telah melewati sesi chat. Menunggu pengguna lain...')
        waiting_users[user_data[user_id]['gender']].append(user_id)
        find_chat_partner(user_id, context)
    else:
        update.message.reply_text('Anda tidak dalam sesi chat. Mencari pengguna lain...')
        waiting_users[user_data[user_id]['gender']].append(user_id)
        find_chat_partner(user_id, context)

def handle_message(update: Update, context: CallbackContext) -> None:
    """Menangani pesan yang dikirim oleh pengguna."""
    user_id = update.message.from_user.id
    user_message = update.message.text

    if contains_forbidden_words(user_message):
        update.message.reply_text('Pesan Anda mengandung kata-kata terlarang dan tidak akan dikirim.')
        return

    if user_id in active_chats:
        partner_id = active_chats.get(user_id)
        if partner_id:
            partner_nickname = user_data[partner_id]['nickname']
            context.bot.send_message(chat_id=partner_id, text=f'{user_data[user_id]["nickname"]}: {user_message}')
        else:
            update.message.reply_text('Pasangan chat Anda tidak ditemukan.')
    else:
        update.message.reply_text('Anda tidak sedang terhubung dengan pengguna lain.')

def find_chat_partner(user_id: int, context: CallbackContext) -> None:
    """Mencari pasangan chat dari lawan jenis."""
    user_gender = user_data[user_id]['gender']
    opposite_gender = 'male' if user_gender == 'female' else 'female'

    if waiting_users[opposite_gender]:
        partner_id = waiting_users[opposite_gender].pop(0) 
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        context.bot.send_message(chat_id=user_id, text=f"Anda terhubung dengan {user_data[partner_id]['nickname']}. Mulailah mengirim pesan.")
        context.bot.send_message(chat_id=partner_id, text=f"Anda terhubung dengan {user_data[user_id]['nickname']}. Mulailah mengirim pesan.")
    else:
        context.bot.send_message(chat_id=user_id, text="Tidak ada pengguna lawan jenis yang tersedia. Menunggu pengguna lain...")

def remove_from_waiting(user_id: int) -> None:
    """Menghapus pengguna dari antrian menunggu."""
    gender = user_data.get(user_id, {}).get('gender')
    if gender and user_id in waiting_users[gender]:
        waiting_users[gender].remove(user_id)

def main() -> None:
    """Menjalankan bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('male', male))
    dispatcher.add_handler(CommandHandler('female', female))
    dispatcher.add_handler(CommandHandler('logout', logout))
    dispatcher.add_handler(CommandHandler('skip', skip))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
