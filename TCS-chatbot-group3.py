import logging
import Scrapy_BS 
import telegram
import os
import sys
from telegram.ext import Updater, MessageHandler, Filters
from constants import Constants 

# Configuracion de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Obtener token
TOKEN = os.getenv("TOKEN")

# Especifica el modo
mode = os.getenv("MODE")

if mode == "dev":
    def run(updater):
        updater.start_polling()
        updater.idle()
        
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", Constants.PORT))
        HEROKU_APP_NAME = os.environ.get(Constants.HEROKU_APP_NAME)
        
        updater.start_webhook(listen=Constants.HOST,
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
        updater.set_webhook()
else:
    logging.info("NO se especifico Ambiente")
    sys.exit()

#Funciona que valida si el mensaje recibido esta en la constante de saludo
def validate_initial_msjs(msj):
    boolean = False
    for m in Constants.INITIAL_MSJS:
        boolean = m in msj.lower()
        if boolean:
            return True
    return boolean

#Funcion que obtiene el mensaje y da respuesta del bot
def answer(update, context):
    scrapp = Scrapy_BS.ScrapMercadoLibre()
    user = update.message.from_user
    user_id = user['id']
    
    logger.info(f"El usuario {user_id} ha enviado un mensaje de texto.")
    text = update.message.text
    if validate_initial_msjs(text):
        context.bot.sendMessage(
            chat_id=user_id,
            text=Constants.WELLCOME_MSJ.format(user['first_name'])
        )
    if '*' in text:
        text = text.replace('*', '').strip()
        links = scrapp.scrapper(text.replace(' ', '-'))
        if links:
            context.bot.sendMessage(chat_id=user_id, text=Constants.RESPONSE_MSJ)
            for l in links:
                context.bot.sendMessage(chat_id=user_id, text=l)
        else:
            context.bot.sendMessage(chat_id=user_id, text=Constants.NO_RESULTS)
        context.bot.sendMessage(chat_id=user_id, text=Constants.QUESTION)
    if text.lower() == 'no':
        context.bot.sendMessage(chat_id=user_id, text=Constants.BYE_MSJ)


if __name__ == "__main__":
    # Obtener informacion de bot
    bot = telegram.Bot(token=TOKEN)

# Enlazar updater con bot
updater = Updater(bot.token, use_context=True)

# Creacion de despachador
dp = updater.dispatcher

# Creacion de manejadores
dp.add_handler(MessageHandler(Filters.text, answer))

run(updater)
