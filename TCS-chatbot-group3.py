import logging
import Scrapy_BS
import constants
import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Configuracion de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Obtener token
TOKEN = "5079732120:AAHDOpA50FOKLDETwg7YMVaJViiaZbEPVRE"


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
        context.bot.sendMessage(chat_id=user_id, text=constants.RESPONSE_MSJ)
        text = text.replace('*', '').strip()
        for l in scrapp.scrapper(text.replace(' ', '-')):
            context.bot.sendMessage(chat_id=user_id, text=l)
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

updater.start_polling()
print("BOT CARGADO")
updater.idle()
