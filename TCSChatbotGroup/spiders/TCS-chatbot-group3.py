import logging
import constants
from Scrapy import SuperSpider
import scrapy
from scrapy.crawler import CrawlerProcess



from telegram import Update

from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

execute = False
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def validate_initial_msjs(msj):
    boolean = False
    for m in constants.INITIAL_MSJS:
        boolean = m in msj.lower()
        if boolean:
            return True
    return boolean


def answer(update, context):
    # scrapp = scrapping.ScrapMercadoLibre()
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
        # for l in scrapp.scrapper(text.replace(' ', '-')):
        #     context.bot.sendMessage(chat_id=user_id, text=l)
        a= getProductSuggestions(text)

        context.bot.sendMessage(chat_id=user_id, text=a)
    if text.lower() == 'no':
        context.bot.sendMessage(chat_id=user_id, text=constants.BYE_MSJ)


def start(update: Update, context: CallbackContext):
    global execute
    user = update.message.from_user
    update.message.reply_text(
        "Hola {}, bienvenido al Chat Sugerencias de Market Place. "
        "Si desea sugerencias acerca de un producto por favor especifique el nombre o categoría.".format(
            user['first_name']))
    execute = True


def getMessageText(update: Update, context: CallbackContext):
    global execute
    text = update.message.text
    validate(text)

    if execute == False:
        ConversationHandler.END
    else:
        if text != 'si':
            response = getProductSuggestions(text)
            logger.info(f"RESPUESTA {response}")
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Estos son los productos relacionados a su búsqueda {}".format(response))
            update.message.reply_text("¿Desea realizar una nueva búsqueda?")
            execute = False
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="ingrese el nombre del produto o categoria")


def validate(text):
    global execute
    if text == 'si':
        execute = True

    if text == 'no':
        execute = False


def getProductSuggestions(productoOrCategoryTxt):
    logger.info(f"Inicio la araña")
    try:
        spider = SuperSpider(productoOrCategoryTxt)
        process = CrawlerProcess()
        process.crawl(spider)
        process.start()
        logger.info(f"Final la araña")
        return('www.mercadolibre.com/')
    except Exception as e:
        logger.info(f"error al ejecutar la araña {e.message}")
        return('www.amazon.com')



def main() -> None:
    """Run bot."""
    # create the Updater and pass it your bot's token.
    #updater = Updater("5074260439:AAGufztidGmGn7dF2YrltpEAfg_I8GOKY1M")
    updater= Updater("5082826605:AAFLrkhCFjDMjTc1imQ48TuEbtU8gssi0XY")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
