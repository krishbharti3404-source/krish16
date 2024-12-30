"""
Terabox Converter Bot Utilities
Created by: TechRewindEditz
Created at: 2024-12-30
"""

import logging
from typing import Dict, Optional, Any
from datetime import datetime, timezone
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Version information
__version__ = "1.0.0"
__author__ = "TechRewindEditz"
__created_at__ = "2024-12-30"

class UtilsConfig:
    """Configuration class for utilities"""
    SUPPORTED_MEDIA_TYPES = {
        'video/mp4': ['.mp4'],
        'video/x-matroska': ['.mkv'],
        'video/x-msvideo': ['.avi'],
        'video/quicktime': ['.mov'],
        'video/x-ms-wmv': ['.wmv']
    }

    PLAYER_SCHEMES = {
        'vlc': 'vlc://',
        'mx_player': 'intent:',
        'playit': 'playit://'
    }

    @staticmethod
    def get_mime_type(filename: str) -> Optional[str]:
        """Get MIME type from filename extension"""
        ext = os.path.splitext(filename.lower())[1]
        for mime_type, extensions in UtilsConfig.SUPPORTED_MEDIA_TYPES.items():
            if ext in extensions:
                return mime_type
        return None

class ResponseFormatter:
    """Formatter for API responses"""
    
    @staticmethod
    def format_response(
        success: bool,
        data: Optional[Dict] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format API response with consistent structure"""
        return {
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data if data else {},
            "error": error if error else None
        }

class TeraboxValidator:
    """Validator for Terabox URLs and responses"""
    
    @staticmethod
    def is_valid_terabox_url(url: str) -> bool:
        """Validate if URL is a valid Terabox share link"""
        valid_domains = [
            'terabox.com',
            'teraboxapp.com',
            '1024tera.com'
        ]
        return any(domain in url.lower() for domain in valid_domains)

    @staticmethod
    def validate_file_info(file_info: Dict) -> bool:
        """Validate file information from Terabox"""
        required_fields = ['filename', 'size', 'fs_id']
        return all(field in file_info for field in required_fields)

class GeminiHelper:
    """Helper functions for Gemini AI integration"""
    
    @staticmethod
    def prepare_analysis_prompt(file_info: Dict) -> str:
        """Prepare prompt for Gemini AI analysis"""
        return f"""
        Analyze this media file:
        Filename: {file_info.get('filename', 'Unknown')}
        Size: {file_info.get('size', 0)} bytes
        Type: {file_info.get('mime_type', 'Unknown')}

        Please provide:
        1. Content type verification
        2. File format compatibility check
        3. Streaming quality estimation based on file size
        4. Recommended player settings
        5. Security recommendations
        """

    @staticmethod
    def parse_analysis_response(response: str) -> Dict[str, Any]:
        """Parse and structure Gemini AI response"""
        return {
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "content": response,
            "generated_by": "Google Gemini AI"
        }

def get_player_url(player: str, direct_url: str, filename: str) -> Optional[str]:
    """Generate player-specific streaming URLs"""
    if player not in UtilsConfig.PLAYER_SCHEMES:
        return None
        
    if player == 'mx_player':
        return (f"intent:{direct_url}#Intent;"
                f"package=com.mxtech.videoplayer.ad;"
                f"S.title={filename};end")
    elif player == 'vlc':
        return f"vlc://{direct_url}"
    elif player == 'playit':
        return f"playit://{direct_url}"
    
    return None

# Error classes
class TeraboxError(Exception):
    """Base exception for Terabox-related errors"""
    pass

class InvalidTeraboxURL(TeraboxError):
    """Exception for invalid Terabox URLs"""
    pass

class FileProcessingError(TeraboxError):
    """Exception for file processing errors"""
    pass

class UnsupportedMediaType(TeraboxError):
    """Exception for unsupported media types"""
    pass

# Export commonly used functions and classes
__all__ = [
    'UtilsConfig',
    'ResponseFormatter',
    'TeraboxValidator',
    'GeminiHelper',
    'get_player_url',
    'TeraboxError',
    'InvalidTeraboxURL',
    'FileProcessingError',
    'UnsupportedMediaType',
    'logger'
]
