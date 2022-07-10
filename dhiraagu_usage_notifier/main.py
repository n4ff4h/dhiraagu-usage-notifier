import os
from dotenv import load_dotenv
import telebot
import dhiraagu_portal

load_dotenv()

API_KEY = os.getenv('API_KEY')
DHIRAAGU_USERNAME = os.getenv('DHIRAAGU_USERNAME')
DHIRAAGU_PASSWORD = os.getenv('DHIRAAGU_PASSWORD')

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['report'])
def get_usage_data(message):
    # Get home page html
    home_page = dhiraagu_portal.login_and_return_html(
        DHIRAAGU_USERNAME, DHIRAAGU_PASSWORD)

    # If incorrect user credentials
    if not home_page:
        bot.send_message(message.chat.id, "Login failed!")
    else:
        # Scrape usage data from website
        usage_data = dhiraagu_portal.get_usage_data(home_page)
        bot.send_message(message.chat.id, usage_data, parse_mode='Markdown')


bot.polling()
