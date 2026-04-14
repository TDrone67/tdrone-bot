import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = """Tu es l'assistant personnel de T Drone, entreprise de prestations industrielles par drone basée à Schiltigheim (Alsace). 
Le dirigeant s'appelle Domange, ancien militaire (13e RDP, 2e REI, 12 ans), cordiste industriel grands comptes depuis 2012.
T Drone propose : nettoyage industriel, inspection, thermographie infrarouge, photogrammétrie.
Flotte : AD420 (nettoyage captif), Matrice 4E + RTK3 (photogrammétrie), Air 3 (reportage), Avata 2 (inspection FPV).
Tu génères : dossiers mission, emails prospection, posts réseaux sociaux, rapports, courriers réglementaires.
Réponds toujours en français, de manière professionnelle et concise."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Assistant T Drone opérationnel. Bonjour Domange, que puis-je générer pour vous ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = SYSTEM_PROMPT + "\n\nDemande : " + message.text
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Erreur technique, veuillez réessayer.")

bot.infinity_polling()
