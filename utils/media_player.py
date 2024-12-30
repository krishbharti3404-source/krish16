from typing import Dict
from urllib.parse import quote

class MediaPlayerHandler:
    @staticmethod
    def generate_stream_urls(file_info: Dict) -> Dict[str, str]:
        filename = quote(file_info['filename'])
        direct_url = quote(file_info['direct_url'])
        
        return {
            "direct_url": file_info['direct_url'],
            "players": {
                "vlc": f"vlc://{direct_url}",
                "mx_player": (
                    f"intent:{direct_url}#Intent;"
                    f"package=com.mxtech.videoplayer.ad;"
                    f"S.title={filename};end"
                ),
                "playit": f"playit://{direct_url}"
            },
            "filename": file_info['filename'],
            "size": file_info['size'],
            "mime_type": file_info['mime_type']
        }

    @staticmethod
    def check_format_support(mime_type: str) -> bool:
        supported_types = [
            'video/mp4',
            'video/x-matroska',
            'video/x-msvideo',
            'video/quicktime',
            'video/x-ms-wmv'
        ]
        return mime_type in supported_types
