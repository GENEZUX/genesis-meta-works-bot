import os
import asyncio
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1️⃣ FETCH REWARDS (97V2RT)", callback_data='fetch')],
        [InlineKeyboardButton("2️⃣ MODA & SNEAKERS", callback_data='moda')],
        [InlineKeyboardButton("3️⃣ TECH & B2B", callback_data='tech')],
        [InlineKeyboardButton("4️⃣ DISEÑO GRÁFICO", callback_data='diseno')],
        [InlineKeyboardButton("5️⃣ AGENCIA BARBOSA", callback_data='agencia')],
        [InlineKeyboardButton("6️⃣ ATENCIÓN AL CLIENTE", callback_data='soporte')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "¡Bienvenido al cerebro de *Genesis MetaWorks*! 🧠
"
        "Soy el sistema unificado que conecta todo tu ecosistema.

"
        "¿Qué área quieres activar hoy?"
    )
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    responses = {
        'fetch': "💰 *FETCH REWARDS*
Usa el código *97V2RT* para ganar puntos al subir tus recibos. ¡Dinero gratis!",
        'moda': "👟 *MODA & SNEAKERS*
Acceso a lanzamientos exclusivos de Nike, Adidas y más.",
        'tech': "☁️ *TECH & B2B*
Soluciones empresariales y servicios de Alibaba Cloud.",
        'diseno': "🎨 *DISEÑO GRÁFICO*
Servicios profesionales desde $25. ¿Necesitas un flyer RUSH?",
        'agencia': "🤖 *AGENCIA BARBOSA*
Automatización e Inteligencia Artificial para tu negocio.",
        'soporte': "📞 *ATENCIÓN AL CLIENTE*
Déjanos tu mensaje y un humano Pro te contactará pronto."
    }
    
    text = responses.get(query.data, "Opción no válida.")
    keyboard = [[InlineKeyboardButton("⬅️ Volver al Menú", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def process_update(token: str, data: dict):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^(?!back$).*'))
    application.add_handler(CallbackQueryHandler(start, pattern='^back$'))
    async with application:
        update = Update.de_json(data, application.bot)
        await application.process_update(update)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    asyncio.run(process_update(TOKEN, data))
    return jsonify({'ok': True})

@app.route('/')
def index():
    return jsonify({'status': 'running', 'bot': 'Genesis MetaWorks Mega-Bot'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
