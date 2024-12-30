# app/main.py

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.config import Config
from app.utils.terabox import TeraboxDownloader
from app.utils.media_player import MediaPlayerHandler
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(
        'Welcome to Terabox Link Converter Bot!\n'
        'Send me a Terabox link to convert it for streaming.'
    )

def handle_link(update, context):
    try:
        url = update.message.text
        message = update.message.reply_text("Processing your link...")
        
        # Convert Terabox link
        downloader = TeraboxDownloader()
        result = downloader.get_direct_link(url)
        
        # Generate player links
        player_handler = MediaPlayerHandler()
        mx_link = player_handler.get_player_url(result['url'], 'mxplayer', result['filename'])
        vlc_link = player_handler.get_player_url(result['url'], 'vlc', result['filename'])
        playit_link = player_handler.get_player_url(result['url'], 'playit', result['filename'])
        
        response = (
            f"✅ Link Converted Successfully!\n\n"
            f"📁 File: {result['filename']}\n"
            f"📦 Size: {result['size']}\n\n"
            f"🎬 Streaming Links:\n"
            f"▫️ MX Player: {mx_link}\n"
            f"▫️ VLC Player: {vlc_link}\n"
            f"▫️ Playit: {playit_link}\n\n"
            f"🔄 Direct Link: {result['url']}"
        )
        
        message.edit_text(response, disable_web_page_preview=True)
        
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(Config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    
    # Message handlers
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        handle_link
    ))

    # Start the Bot
    if Config.WEBHOOK_URL:
        updater.start_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=Config.BOT_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.BOT_TOKEN}"
        )
    else:
        updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()
