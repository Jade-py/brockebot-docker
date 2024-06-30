import logging
import os
from g4f.client import Client
from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


env = Env()
env.read_env()

logger = logging.getLogger(__name__)

client = Client()

# Store bot screaming status
screaming = True


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """
    a = "Answer only in the context of Brock from pokemon under 200 words and avoid any other question irrelevant to Brock by responding - Does not seem relevant to Brock. Here is the question: " + update.message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": a}],
    )
    b = response.choices[0].message.content

    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')
    print(b)

    if screaming and update.message.text:
        context.bot.send_message(
            update.message.chat_id,
            text=f"{b}",
            # To preserve the markdown, we attach entities (bold, italic...)
            entities=update.message.entities
        )
    else:
        print('no answer')
        # This is equivalent to forwarding, without the sender's name
        update.message.copy(update.message.chat_id)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(text="Hi there.. I'm here to help with any information related to Brock. Ask away!", chat_id=update.message.chat_id)


def main() -> None:
    updater = Updater(os.getenv('BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()