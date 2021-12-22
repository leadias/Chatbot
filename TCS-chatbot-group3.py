import logging
import Scrapy_BS
import constants
import telegram
import os
import sys
from telegram.ext import Updater, MessageHandler, Filters

# Configuracion de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Obtener token
#TOKEN = "5079732120:AAHDOpA50FOKLDETwg7YMVaJViiaZbEPVRE"
TOKEN="5035946334:AAHzHpE-xydiEwPkNGwtDD8OJPMx36wDGzA"
#Especifica el 
mode= os.getenv("MODE")

if mode == "dev":
    def run(updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle()
elif mode == "prod":
    def run(updater):
        PORT =int(os.environ.get("PORT","8483"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
    logging.info("NO se especifico Ambiente")
    sys.exit()

def validate_initial_msjs(msj):
    boolean = False
    for m in constants.INITIAL_MSJS:
        boolean = m in msj.lower()
        if boolean:
            return True
    return boolean


def answer(update, context):
    scrapp = Scrapy_BS.ScrapMercadoLibre()
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id} ha enviado un mensaje de texto.")
    text = update.message.text
    if validate_initial_msjs(text):
        context.bot.sendMessage(
            chat_id=user_id,
            text=constants.WELLCOME_MSJ
        )
    if '*' in text:
        text = text.replace('*', '').strip()
        links = scrapp.scrapper(text.replace(' ', '-'))
        if links:
            context.bot.sendMessage(chat_id=user_id, text=constants.RESPONSE_MSJ)
            for l in links:
                context.bot.sendMessage(chat_id=user_id, text=l)
        else:
            context.bot.sendMessage(chat_id=user_id, text=constants.NO_RESULTS)
        context.bot.sendMessage(chat_id=user_id, text=constants.QUESTION)
    if text.lower() == 'no':
        context.bot.sendMessage(chat_id=user_id, text=constants.BYE_MSJ)


if __name__ == "__main__":
    # Obtener informacion de bot
    bot = telegram.Bot(token=TOKEN)
    # print(bot.getMe())

# Enlazar updater con bot
updater = Updater(bot.token, use_context=True)

# Creacion de despachador
dp = updater.dispatcher

# Creacion de manejadores
dp.add_handler(MessageHandler(Filters.text, answer))

run(updater)

