import logging

from scrapy.utils.project import get_project_settings

import constants
from scrapy import signals
from pydispatch import dispatcher
from TCSChatbotGroup.spiders.Scrapy import SuperSpider
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
        # for l in spider_results(text.replace(' ', '-'))['links']:
        #     context.bot.sendMessage(chat_id=user_id, text=l)
        context.bot.sendMessage(chat_id=user_id, text=constants.QUESTION)
    if text.lower() == 'no':
        context.bot.sendMessage(chat_id=user_id, text=constants.BYE_MSJ)


def spider_results(parametro):
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    process = CrawlerProcess(get_project_settings())
    process.crawl(SuperSpider, parameter=parametro)
    process.start()  # the script will block here until the crawling is finished
    return results


def main() -> None:
    """Run bot."""
    # create the Updater and pass it your bot's token.
    # updater = Updater("5074260439:AAGufztidGmGn7dF2YrltpEAfg_I8GOKY1M")
    # updater= Updater("5082826605:AAFLrkhCFjDMjTc1imQ48TuEbtU8gssi0XY")
    updater = Updater("5079732120:AAHDOpA50FOKLDETwg7YMVaJViiaZbEPVRE")
    dispatcher_bot = updater.dispatcher
    dispatcher_bot.add_handler(MessageHandler(Filters.text, answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
