import logging
import os

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    Dispatcher,
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

def start(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("Start Update %s", update)
    logger.info("Start Message %s", update.message)
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("See my subscriptions", callback_data=str(ONE)),
            InlineKeyboardButton("Add currency to monitor", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Welcome!", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, _: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    logger.info("start_over Update %s", update)
    logger.info("start_over Message %s", update.message)
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return FIRST


def one(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    logger.info("one Update %s", update)
    logger.info("one Message %s", update.message)
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def two(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    logger.info("two Update %s", update)
    logger.info("two Message %s", update.message)
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def three(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    logger.info("three Update %s", update)
    logger.info("three Message %s", update.message)
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def end(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    logger.info("end Update %s", update)
    logger.info("end Message %s", update.message)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


# def main() -> None:
#     """Start the bot."""
#     logger.info('Starting the bot')
#     # Create the Updater and pass it your bot's token.
#     # port = os.getenv('PORT', default=80)
#     # logger.info(f'Listening to port {port}')
#     updater = Updater(os.environ["TG_API_TOKEN"])
#     # updater.start_webhook(port=port)
#
#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher
#
#     logger.info('Adding handlers')
#     # on different commands - answer in Telegram
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("help", help_command))
#
#     # on non command i.e message - echo the message on Telegram
#     dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
#
#     logger.info('Starting polling')
#     # Start the Bot
#     updater.start_polling()
#
#     logger.info('Running the bot in idle mode')
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


def process_telegram_event(update_json):
    logger.info(f'event json: {update_json}')
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def setup_dispatcher(dp: Dispatcher):
    logger.info('Adding handlers')
    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    logger.info('Starting the bot')
    polling_updater = Updater(os.environ["TG_API_TOKEN"], use_context=True)
    setup_dispatcher(polling_updater.dispatcher)

    bot_info = Bot(os.environ["TG_API_TOKEN"]).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    logger.info(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)
    polling_updater.start_polling()
    logger.info('Running the bot in idle mode')
    polling_updater.idle()


bot = Bot(os.environ["TG_API_TOKEN"])
updater = Updater(os.environ["TG_API_TOKEN"], use_context=True)
dispatcher = setup_dispatcher(updater.dispatcher)
