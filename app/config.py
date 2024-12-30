import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the Terabox Converter Bot
    Created by: TechRewindEditz
    Last Updated: 2024-12-30
    """
    
    # Basic Bot Configuration
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'YourBotUsername')
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')  # Your Telegram Bot Token
    
    # API Configuration
    API_ID = os.getenv('API_ID', '')  # Your Telegram API ID
    API_HASH = os.getenv('API_HASH', '')  # Your Telegram API Hash
    
    # Channel and Admin Configuration
    CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'YourChannelUsername')
    CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))  # Channel ID for force subscribe
    CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME}"
    ADMIN_IDS = [int(id_) for id_ in os.getenv('ADMIN_IDS', '').split(',') if id_]
    OWNER_ID = int(os.getenv('OWNER_ID', 0))  # Owner's Telegram ID
    
    # Database Configuration (if needed)
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    
    # Terabox Configuration
    TERABOX_COOKIE = os.getenv('TERABOX_COOKIE', '')
    TERABOX_TOKEN = os.getenv('TERABOX_TOKEN', '')
    TERABOX_USER_ID = os.getenv('TERABOX_USER_ID', '')
    
    # User Agent Configuration
    USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
    
    # Media Player Templates
    MXPLAYER_TEMPLATE = (
        "intent://play?link={url}#Intent;"
        "package=com.mxtech.videoplayer.ad;"
        "S.title={title};"
        "end"
    )
    VLC_TEMPLATE = "vlc://{url}"
    PLAYIT_TEMPLATE = (
        "playit://playerv2/video?"
        "url={url}&"
        "title={title}"
    )
    
    # Webhook Configuration (for Koyeb)
    WEBHOOK = os.getenv('WEBHOOK', 'True').lower() == 'true'
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')  # Your Koyeb app URL
    PORT = int(os.getenv('PORT', 8080))
    
    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 2147483648))  # 2GB in bytes
    ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov', 'flv', 'wmv'}
    
    # Rate Limiting
    RATE_LIMIT = {
        'window': 3600,  # 1 hour in seconds
        'max_requests': int(os.getenv('MAX_REQUESTS', 50))
    }
    
    # Cache Configuration
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 3600))  # 1 hour in seconds
    
    # Bot Messages and Text
    START_TEXT = """
👋 Welcome to Terabox Link Converter Bot!

I can help you convert Terabox links to direct streaming links for:
- MX Player
- VLC Media Player
- Playit App

🔐 Make sure to join our channel: {channel_url}
    """
    
    HELP_TEXT = """
📖 **Available Commands:**

/start - Start the bot
/help - Show this help message
/status - Check bot status
/about - About the bot

Simply send me a Terabox link to convert it!
    """
    
    ABOUT_TEXT = """
🤖 **Terabox Link Converter Bot**

Version: 1.0.0
Created by: @TechRewindEditz
Last Updated: 2024-12-30

📢 Updates: {channel_url}
    """
    
    # Error Messages
    ERROR_MESSAGES = {
        'not_subscribed': f"❌ Please join our channel first:\n{CHANNEL_URL}",
        'invalid_link': "❌ Invalid Terabox link! Please send a valid link.",
        'processing_error': "❌ Error processing the link. Please try again later.",
        'rate_limit': "❌ Rate limit exceeded. Please try again later.",
        'file_too_large': "❌ File size too large. Maximum allowed size is 2GB.",
        'maintenance': "🛠️ Bot is under maintenance. Please try again later."
    }
    
    # Maintenance Mode
    MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False').lower() == 'true'
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if user is an admin"""
        return user_id in cls.ADMIN_IDS or user_id == cls.OWNER_ID
    
    @classmethod
    def get_start_text(cls) -> str:
        """Get formatted start text"""
        return cls.START_TEXT.format(channel_url=cls.CHANNEL_URL)
    
    @classmethod
    def get_about_text(cls) -> str:
        """Get formatted about text"""
        return cls.ABOUT_TEXT.format(channel_url=cls.CHANNEL_URL)
    
    # Development/Production mode
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Session Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', 'csrf-secret-key')
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        pass

# For local testing
if __name__ == "__main__":
    print("Bot Configuration:")
    print(f"Bot Username: {Config.BOT_USERNAME}")
    print(f"Channel: {Config.CHANNEL_URL}")
    print(f"Webhook Enabled: {Config.WEBHOOK}")
    print(f"Debug Mode: {Config.DEBUG}")
