import os
from google import genai
import telebot

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(BOT_TOKEN)

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
        bot.reply_to(message, "Erreur technique, veuillez reessayer.")

bot.infinity_polling()
