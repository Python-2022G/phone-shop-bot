from flask import Flask, request
import os
from telegram import Bot, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler, Filters,
    CallbackQueryHandler,
    Dispatcher
)
from callback_functions import (
    start, brands,
    send_products, send_product_detail,
    remove_cart, add_cart
)
from db import DB

# create flask app
app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')

# create bot
bot = Bot(TOKEN)

# create db obj
db = DB(file_name='db.json')

# create webhook
@app.route('/webhook/', methods=["POST"])
def webhook():
    # create dp obj
    dp = Dispatcher(bot, None, workers=0)

    # convert json to Update obj
    data = request.get_json(force=True)
    update = Update.de_json(data=data, bot=bot)

    dp.add_handler(handler=CommandHandler('start',start))
    dp.add_handler(handler=CallbackQueryHandler(brands, pattern="mavjud brendlar"))
    dp.add_handler(handler=CallbackQueryHandler(send_products, pattern="brend:"))
    dp.add_handler(handler=CallbackQueryHandler(send_product_detail, pattern="product:"))
    dp.add_handler(handler=CallbackQueryHandler(remove_cart, pattern="remove"))
    dp.add_handler(handler=CallbackQueryHandler(add_cart, pattern="add-cart:"))

    dp.process_update(update)

    return 'ok'



# create home test view
@app.route('/')
def home():
    return "working!"


# set webhook
@app.route('/set-webook/')
def set_hook():
    r = bot.set_webhook('https://echobotdeploy.pythonanywhere.com/webhook/')

    return f"info: {r}"
