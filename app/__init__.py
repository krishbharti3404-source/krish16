import logging
from flask import Flask
from telegram.ext import Updater
from app.config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Telegram bot
try:
    updater = Updater(token=Config.BOT_TOKEN, use_context=True)
    bot = updater.bot
    dp = updater.dispatcher
    logger.info("Bot initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize bot: {str(e)}")
    raise

# Rate limiting dictionary
user_requests = {}

def init_bot():
    """Initialize bot commands and handlers"""
    from app.utils import terabox, media_player
    from app import main
    
    # Register bot commands
    commands = [
        ('start', 'Start the bot'),
        ('help', 'Show help message'),
        ('status', 'Check bot status'),
        ('about', 'About the bot')
    ]
    
    try:
        bot.set_my_commands(commands)
        logger.info("Bot commands set successfully!")
    except Exception as e:
        logger.error(f"Failed to set bot commands: {str(e)}")

def create_app():
    """Initialize the core application"""
    try:
        # Initialize bot
        init_bot()
        
        # Register blueprints if any
        # app.register_blueprint(some_blueprint)
        
        logger.info("Application initialized successfully!")
        return app
    except Exception as e:
        logger.error(f"Failed to create application: {str(e)}")
        raise

# Create version info
__version__ = '1.0.0'
__author__ = 'TechRewindEditz'
__license__ = 'MIT'

# Export necessary items
__all__ = [
    'app',
    'bot',
    'dp',
    'updater',
    'user_requests',
    'create_app',
    '__version__',
    '__author__',
    '__license__'
]

# Create the application instance
app = create_app()

@app.after_request
def after_request(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return {
        'error': 'Not Found',
        'status': 404
    }, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Server Error: {error}')
    return {
        'error': 'Internal Server Error',
        'status': 500
    }, 500

# Initialize error handlers
@dp.error_handler
def handle_telegram_error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    # Send message to admin if critical error
    if hasattr(context.error, 'message'):
        error_msg = f"⚠️ Bot Error:\n\n{context.error.message}"
        for admin_id in Config.ADMIN_IDS:
            try:
                bot.send_message(chat_id=admin_id, text=error_msg)
            except Exception as e:
                logger.error(f"Failed to send error message to admin {admin_id}: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT)
