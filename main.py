import telebot
import requests
import time
from urllib.parse import quote
from datetime import datetime, timedelta

# Membaca token dari file
with open("token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()

bot = telebot.TeleBot(TOKEN)

# Waktu bot pertama kali dijalankan
start_time = time.time()

# Peta konversi Latin ke Aksara Sunda
latin_to_sundanese = {
    'a': 'ᮃ', 'b': 'ᮘ', 'c': 'ᮎ', 'd': 'ᮓ', 'e': 'ᮄ',
    'f': 'ᮖ', 'g': 'ᮌ', 'h': 'ᮠ', 'i': 'ᮤ', 'j': 'ᮏ',
    'k': 'ᮊ', 'l': 'ᮜ', 'm': 'ᮙ', 'n': 'ᮔ', 'o': 'ᮇ',
    'p': 'ᮕ', 'q': 'ᮢ', 'r': 'ᮛ', 's': 'ᮞ', 't': 'ᮒ',
    'u': 'ᮥ', 'v': 'ᮗ', 'w': 'ᮝ', 'x': 'ᮞ', 'y': 'ᮚ',
    'z': 'ᮐ', ' ': ' '
}
sundanese_to_latin = {v: k for k, v in latin_to_sundanese.items()}

def convert_to_sundanese(text):
    return ''.join(latin_to_sundanese.get(char, char) for char in text.lower())

def convert_from_sundanese(text):
    return ''.join(sundanese_to_latin.get(char, char) for char in text)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Halo! Gunakan /menu untuk melihat fitur bot.")

@bot.message_handler(commands=["menu"])
def menu_command(message):
    menu_text = (
        "╔══════════════════╗\n"
        "      ✨ *MENU BOT* ✨\n"
        "╚══════════════════╝\n"
        "📌 /ai [pertanyaan] → AI Blackbox\n"
        "🌐 /ssweb [url] → Screenshot Web\n"
        "🕰 /runtime → Info Runtime Bot\n"
        "🔠 /sunda [teks] → Konversi Latin ↔ Aksara Sunda\n"
        "🎵 /tt [link TikTok] → Download Video TikTok\n"
        "╔══════════════════╗\n"
        "          *By DatxzzXploit* \n"
        "╚══════════════════╝"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")

@bot.message_handler(commands=["ai"])
def blackbox_ai(message):
    text = message.text.replace("/ai", "").strip()

    if not text:
        bot.reply_to(message, "⚠️ *Contoh:* `/ai Apa itu AI Blackbox?`", parse_mode="Markdown")
        return

    bot.reply_to(message, "⏳ *Memproses...*", parse_mode="Markdown")

    try:
        url = f"https://api.siputzx.my.id/api/ai/blackboxai?content={quote(text)}"
        response = requests.get(url).json()
        ai_response = response.get('data', 'Maaf, AI tidak bisa menjawab saat ini.')
    except Exception:
        ai_response = "⚠️ *Error:* Tidak dapat menghubungi server AI."

    bot.reply_to(message, ai_response)

@bot.message_handler(commands=["ssweb"])
def screenshot_website(message):
    text = message.text.replace("/ssweb", "").strip()

    if not text:
        bot.reply_to(message, "⚠️ *Contoh:* `/ssweb https://github.com/Yuta-Okkotsu`", parse_mode="Markdown")
        return

    if not text.startswith("http"):
        url = f"https://image.thum.io/get/width/1900/crop/1000/fullpage/https://{text}"
    else:
        url = f"https://image.thum.io/get/width/1900/crop/1000/fullpage/{text}"

    try:
        bot.send_photo(message.chat.id, url, caption="✅ *Screenshot berhasil!*", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "⚠️ *Error:* Tidak dapat mengambil screenshot.")

@bot.message_handler(commands=["runtime"])
def runtime_command(message):
    current_time = time.time()
    elapsed_time = current_time - start_time
    runtime = str(timedelta(seconds=int(elapsed_time)))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    runtime_text = (
        f"⏳ *Bot Runtime Info:*\n"
        f"──────────────────────\n"
        f"🖥️ *Server:* Unknown\n"
        f"⏰ *Waktu Berjalan:* {runtime}\n"
        f"📅 *Waktu Sekarang:* {now}\n"
        f"──────────────────────"
    )
    
    bot.reply_to(message, runtime_text, parse_mode="Markdown")

@bot.message_handler(commands=["sunda"])
def sunda_converter(message):
    text = message.text.replace("/sunda", "").strip()

    if not text:
        bot.reply_to(message, "⚠️ *Contoh:* `/sunda halo`", parse_mode="Markdown")
        return

    if any(char in latin_to_sundanese for char in text.lower()):
        converted_text = convert_to_sundanese(text)
    else:
        converted_text = convert_from_sundanese(text)

    bot.reply_to(message, f"🔠 *Hasil Konversi:*\n`{converted_text}`", parse_mode="Markdown")

@bot.message_handler(commands=["tt"])
def download_tiktok(message):
    text = message.text.replace("/tt", "").strip()

    if not text or not text.startswith("https://"):
        bot.reply_to(message, "⚠️ *Contoh:* `/tt https://vt.tiktok.com/ZS6qRB5Dm/`", parse_mode="Markdown")
        return

    bot.reply_to(message, "⏳ *Mengunduh...*", parse_mode="Markdown")

    try:
        response = requests.get(f"https://api.diioffc.web.id/api/download/tiktok?url={text}").json()

        if 'images' in response['result']:
            for i in response['result']['images']:
                bot.send_photo(message.chat.id, i)
        else:
            bot.send_video(
                message.chat.id, response['result']['play'], 
                caption=f"🎵 {response['result']['title']}", parse_mode="Markdown"
            )
            time.sleep(3)
            bot.send_audio(
                message.chat.id, response['result']['music_info']['play'], 
                title=response['result']['music_info']['title']
            )
    except Exception:
        bot.reply_to(message, "⚠️ *Error:* Gagal mengunduh video TikTok.")

if __name__ == "__main__":
    print("Bot sedang berjalan...")
    bot.infinity_polling()