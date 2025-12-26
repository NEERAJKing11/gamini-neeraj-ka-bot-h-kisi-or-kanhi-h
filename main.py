import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. BOT AUR AI KI SETTING ---
# Render ki setting se keys lena
TOKEN_MERA_BOT = os.getenv("BOT_TOKEN")
KEY_MERA_GEMINI = os.getenv("GOOGLE_API_KEY")
ALLOWED_USER_ID = os.getenv("AUTHORIZED_USERS")

# Gemini AI ko shuru karna
genai.configure(api_key=KEY_MERA_GEMINI)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Bot ko shuru karna
bot = telebot.TeleBot(TOKEN_MERA_BOT)

# --- 2. RENDER PAR BOT KO ZINDA RAKHNE KA JUGAAD ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Chal Raha Hai!"

def run_server():
    # Render port 8080 use karta hai
    app.run(host='0.0.0.0', port=8080)

def hamesha_zinda_rakho():
    t = Thread(target=run_server)
    t.start()

# --- 3. BOT KYA KAAM KAREGA ---

@bot.message_handler(commands=['start'])
def swagat(message):
    bot.reply_to(message, "Namaste! Main Neeraj ka AI Bot hu. Mujhse sawaal puchiye.")

@bot.message_handler(func=lambda message: True)
def jawab_do(message):
    # Sirf aapki ID check karna
    if str(message.from_user.id) != ALLOWED_USER_ID:
        bot.reply_to(message, "Maaf kijiye, aap is bot ko use nahi kar sakte.")
        return

    try:
        # AI se jawaab mangna
        ai_ka_jawab = ai_model.generate_content(message.text)
        bot.reply_to(message, ai_ka_jawab.text)
    except Exception as e:
        bot.reply_to(message, "Kuch galti ho gayi hai.")

# --- 4. BOT KO CHALANA ---
if __name__ == "__main__":
    hamesha_zinda_rakho() # Pehle web server chalega
    print("Bot shuru ho gaya hai...")
    bot.infinity_polling() # Fir bot chalega
