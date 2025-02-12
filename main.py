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
        "🤖 /gpt [pertanyaan] → ChatGPT API\n"
        "📸 /ig [link IG] → Download Instagram\n"
        "🌐 /ssweb [url] → Screenshot Web\n"
        "🕰 /runtime → Info Runtime Bot\n"
        "🔠 /sunda [teks] → Konversi Latin ↔ Aksara Sunda\n"
        "╔══════════════════╗\n"
        "     *By DatxzzXploit* \n"
        "╚══════════════════╝"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")

@bot.message_handler(commands=["gpt"])
def handle_gpt(message):
    text = message.text.replace("/gpt", "").strip()

    if not text:
        bot.reply_to(message, "🤖 *Halo! Ada yang bisa saya bantu?*\n\n*Contoh:* `/gpt Apa itu AI?`", parse_mode="Markdown")
        return

    bot.reply_to(message, "⏳ *Memproses...*", parse_mode="Markdown")

    try:
        url = f"https://api-rest-rizzkyofc.vercel.app/api/ai/gpt-3-5-turbo?text={quote(text)}"
        response = requests.get(url).json()
        ai_response = response.get('result', 'Maaf, saya tidak dapat menjawab saat ini.')
    except Exception:
        ai_response = "⚠️ *Error:* Tidak dapat menghubungi server ChatGPT."

    bot.reply_to(message, ai_response)

@bot.message_handler(commands=["ig"])
def download_instagram(message):
    text = message.text.replace("/ig", "").strip()

    if not text or not text.startswith("https://"):
        bot.reply_to(message, "⚠️ *Contoh:* `/ig https://www.instagram.com/reel/xyz/`", parse_mode="Markdown")
        return

    bot.reply_to(message, "⏳ *Mengunduh...*", parse_mode="Markdown")

    try:
        url = f"https://api-rest-rizzkyofc.vercel.app/api/download/igdl?url={quote(text)}"
        response = requests.get(url).json()

        if 'result' in response:
            for media in response['result']:
                if media.endswith(".mp4"):
                    bot.send_video(message.chat.id, media, caption="🎥 *Video Instagram*")
                elif media.endswith(".jpg") or media.endswith(".png"):
                    bot.send_photo(message.chat.id, media, caption="📸 *Foto Instagram*")
        else:
            bot.reply_to(message, "⚠️ *Error:* Tidak dapat mengunduh media Instagram.")
    except Exception:
        bot.reply_to(message, "⚠️ *Error:* Terjadi kesalahan saat menghubungi server.")

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

if __name__ == "__main__":
    print("Bot sedang berjalan...")
    bot.infinity_polling()
