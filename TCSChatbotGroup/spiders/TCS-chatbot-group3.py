import logging

from telegram import  Update 

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


def start(update: Update, context: CallbackContext):
    global execute
    user = update.message.from_user 
    update.message.reply_text(
        "Hola {}, bienvenido al Chat Sugerencias de Market Place. "
        "Si desea sugerencias acerca de un producto por favor especifique el nombre o categoría.".format(user['first_name']))
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
            context.bot.send_message(chat_id=update.effective_chat.id, text="Estos son los productos relacionados a su búsqueda {}".format(response))
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
    return 'Aca van los resultados o el link relacionado a {}'.format(productoOrCategoryTxt)

def main() -> None:
    """Run bot."""
    #create the Updater and pass it your bot's token.
    updater = Updater("5074260439:AAGufztidGmGn7dF2YrltpEAfg_I8GOKY1M")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, getMessageText))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()