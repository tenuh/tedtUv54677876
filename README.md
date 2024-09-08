```markdown
# Anonymous Chat Bot for Telegram

## Deskripsi

Anonymous Chat Bot adalah bot Telegram yang memungkinkan pengguna untuk berbicara secara anonim dengan orang lain. Bot ini menghubungkan pengguna yang aktif secara acak dan memantau pesan untuk kata-kata terlarang. Pengguna juga dapat keluar dari sesi chat anonim kapan saja menggunakan perintah `/logout`.

## Fitur

- **Anonymous Chat**: Mencocokkan pengguna dengan orang lain secara acak untuk percakapan anonim.
- **Pemantauan Kata-Kata Terlarang**: Memeriksa pesan untuk kata-kata terlarang sebelum mengirimkannya.
- **Logout**: Memungkinkan pengguna untuk keluar dari sesi chat anonim kapan saja.

## Prasyaratan

- Python 3.x
- Library `python-telegram-bot`

## Instalasi

1. **Clone Repository** (Opsional):
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```

2. **Instal Dependensi**:
   Pastikan Anda memiliki `pip` terinstal. Jalankan perintah berikut untuk menginstal library yang diperlukan:
   ```bash
   pip install python-telegram-bot
   ```

3. **Konfigurasi Token Bot**:
   Gantilah `YOUR_BOT_TOKEN` pada kode dengan token API yang Anda dapatkan dari BotFather di Telegram.

## Cara Menggunakan

1. **Simpan Kode**:
   Salin kode Python ke dalam file bernama `anonymous_chat_bot.py`.

2. **Jalankan Bot**:
   Jalankan bot dengan perintah:
   ```bash
   python anonymous_chat_bot.py
   ```

3. **Interaksi dengan Bot**:
   - Kirimkan perintah `/start` untuk memulai chat anonymous.
   - Kirimkan pesan teks untuk berinteraksi dengan pengguna lain.
   - Gunakan perintah `/logout` untuk keluar dari sesi chat anonim.

## Contoh Perintah

- **/start**: Memulai sesi chat anonim.
- **/logout**: Menghapus sesi chat anonim Anda dan keluar dari percakapan saat ini.

## Daftar Kata-Kata Terlarang

Edit daftar `FORBIDDEN_WORDS` dalam kode untuk menambahkan atau menghapus kata-kata yang dianggap tidak pantas. Daftar ini digunakan untuk memfilter pesan yang dikirim oleh pengguna.

## Mengembangkan Lebih Lanjut

Anda dapat mengembangkan bot ini dengan menambahkan fitur tambahan seperti:
- **Matchmaking**: Mencocokkan pengguna berdasarkan minat atau preferensi.
- **Multi-Chat**: Menyediakan opsi chat dengan beberapa orang secara bersamaan.
- **Statistik**: Menyediakan statistik penggunaan bot seperti jumlah pengguna aktif atau jumlah pesan.

## Lisensi

Proyek ini tidak memiliki lisensi resmi. Silakan gunakan dan modifikasi kode ini sesuai kebutuhan Anda.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, Anda dapat membuat pull request atau mengajukan isu melalui [GitHub Issues](https://github.com/username/repository/issues).

## Kontak

Jika Anda memiliki pertanyaan atau membutuhkan bantuan, Anda dapat menghubungi saya melalui email di [your-email@example.com](mailto:your-email@example.com).

---

Selamat menggunakan Anonymous Chat Bot!
```
