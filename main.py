import os
from google import genai
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

SYSTEM_PROMPT = """Tu es l'assistant personnel de T Drone, entreprise de prestations industrielles par drone."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assistant T Drone operationnel. Bonjour Domange, que puis-je faire pour vous ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = SYSTEM_PROMPT + "\n\nDemande : " + message.text
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"ERREUR: {e}")
        bot.reply_to(message, "Erreur technique, veuillez reessayer.")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def health():
    return 'Bot is running!', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + '/' + BOT_TOKEN)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
