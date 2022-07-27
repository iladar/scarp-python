from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot
import time


def get_page():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.pepper.ru/')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_items(product):
    page = get_page()
    items = page.findAll('article')
    result = ''
    for item in items:
        item_name = item.find('a', {'class': ['thread-link']})
        item_price = item.find('span', {'class': ['thread-price']})
        if (item_price is not None) and (item_name is not None) and (item_name.text.lower().find(product) > -1):
            result = result + item_name.text + ' ' + item_price.text
    if result != '':
        return result
    else:
        return 'Ничего не найдено'


search_dict = {}

bot = telebot.TeleBot('5314388500:AAGwA8104RVnn_GsH7Glay-Qiz_iK0MTVWQ')


@bot.message_handler(commands=["start"])
def start(message, res=False):
    msg = bot.reply_to(message, 'Что ищете?')
    bot.register_next_step_handler(msg, process_item_step)


def process_item_step(message):
    item = message.text.lower()
    search_dict['item'] = item
    msg = bot.reply_to(message, 'Как часто?')
    bot.register_next_step_handler(msg, process_interval_step)


def process_interval_step(message):
    search_dict['interval'] = int(message.text)
    while True:
        bot.send_message(message.chat.id, get_items(search_dict['item']))
        time.sleep(search_dict['interval'])
        

bot.polling(none_stop=True, interval=0)
