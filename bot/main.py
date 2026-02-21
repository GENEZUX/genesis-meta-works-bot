import os
import asyncio
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 FETCH REWARDS (97V2RT)", callback_data='fetch')],
        [InlineKeyboardButton("2 MODA & SNEAKERS", callback_data='moda')],
        [InlineKeyboardButton("3 TECH & B2B", callback_data='tech')],
        [InlineKeyboardButton("4 DISENO GRAFICO", callback_data='diseno')],
        [InlineKeyboardButton("5 AGENCIA BARBOSA", callback_data='agencia')],
        [InlineKeyboardButton("6 ATENCION AL CLIENTE", callback_data='soporte')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "Bienvenido al cerebro de Genesis MetaWorks!\nSoy el sistema unificado. Que area quieres activar?"
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    responses = {
        'fetch': "FETCH REWARDS\nUsa el codigo 97V2RT para ganar puntos. Dinero gratis!",
        'moda': "MODA & SNEAKERS\nAcceso a lanzamientos exclusivos de Nike, Adidas y mas.",
        'tech': "TECH & B2B\nSoluciones empresariales y servicios de Alibaba Cloud.",
        'diseno': "DISENO GRAFICO\nServicios profesionales desde $25. Necesitas un flyer RUSH?",
        'agencia': "AGENCIA BARBOSA\nAutomatizacion e Inteligencia Artificial para tu negocio.",
        'soporte': "ATENCION AL CLIENTE\nDejanos tu mensaje y un humano Pro te contactara pronto."
    }
    text = responses.get(query.data, "Opcion no valida.")
    keyboard = [[InlineKeyboardButton("Volver al Menu", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def process_update(token, data):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^(?!back$).*'))
    application.add_handler(CallbackQueryHandler(start, pattern='^back$'))
    async with application:
        update = Update.de_json(data, application.bot)
        await application.process_update(update)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        asyncio.run(process_update(TOKEN, data))
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return jsonify({'ok': True})

@app.route('/')
def index():
    return jsonify({'status': 'running', 'bot': 'Genesis MetaWorks Mega-Bot'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
