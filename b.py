import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '6552995612:AAGpPJPmKHJBKeSbzNJPxjxM3-8HDXa_rec'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the TikTok User Info Bot! Send /userinfo <username> to get TikTok user data.')

def scrape_tiktok_user_info(username):
    # URL for TikTok user page
    url = f"https://www.tiktok.com/@{username}"

    try:
        # Fetch the TikTok user page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape user data (adjust these selectors based on the actual HTML structure)
        name = soup.find('h1').text if soup.find('h1') else 'N/A'
        followers = soup.find('strong', text='Followers').find_next('span').text if soup.find('strong', text='Followers') else 'N/A'
        likes = soup.find('strong', text='Likes').find_next('span').text if soup.find('strong', text='Likes') else 'N/A'
        videos = soup.find('strong', text='Videos').find_next('span').text if soup.find('strong', text='Videos') else 'N/A'

        return {
            'name': name,
            'followers': followers,
            'likes': likes,
            'videos': videos
        }
    except Exception as e:
        return {'error': str(e)}

def userinfo(update: Update, context: CallbackContext) -> None:
    if context.args:
        username = context.args[0]
        user_data = scrape_tiktok_user_info(username)

        if 'error' in user_data:
            update.message.reply_text(f"Error fetching data: {user_data['error']}")
        else:
            reply_text = (f"User: {user_data['name']}\n"
                          f"Followers: {user_data['followers']}\n"
                          f"Likes: {user_data['likes']}\n"
                          f"Videos: {user_data['videos']}\n")
            update.message.reply_text(reply_text)
    else:
        update.message.reply_text('Please provide a TikTok username. Usage: /userinfo <username>')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("userinfo", userinfo))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
