import aiohttp
import json
import re
from typing import Dict, Optional
import logging
import config

class TeraboxDownloader:
    def __init__(self):
        self.headers = {
            "User-Agent": config.TERABOX_USER_AGENT,
            "Accept": "application/json"
        }

    async def process_url(self, url: str) -> Optional[Dict]:
        try:
            # Extract share ID from URL
            share_id = self._extract_share_id(url)
            if not share_id:
                raise ValueError("Invalid Terabox URL")

            # Get file info
            file_info = await self._get_file_info(share_id)
            if not file_info:
                raise ValueError("Failed to get file info")

            # Get download URL
            download_url = await self._get_download_url(file_info)
            
            return {
                "filename": file_info.get("filename", ""),
                "size": file_info.get("size", 0),
                "mime_type": self._get_mime_type(file_info.get("filename", "")),
                "direct_url": download_url
            }

        except Exception as e:
            logging.error(f"Terabox Error: {str(e)}")
            return None

    async def _get_file_info(self, share_id: str) -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.terabox.com/api/share/list?shareid={share_id}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("list", [{}])[0]
        return None

    def _extract_share_id(self, url: str) -> Optional[str]:
        patterns = [
            r"terabox\.com/s/([a-zA-Z0-9_-]+)",
            r"teraboxapp\.com/s/([a-zA-Z0-9_-]+)"
        ]
        for pattern in patterns:
            if match := re.search(pattern, url):
                return match.group(1)
        return None

    def _get_mime_type(self, filename: str) -> str:
        ext_map = {
            'mp4': 'video/mp4',
            'mkv': 'video/x-matroska',
            'avi': 'video/x-msvideo',
            'mov': 'video/quicktime',
            'wmv': 'video/x-ms-wmv'
        }
        ext = filename.lower().split('.')[-1]
        return ext_map.get(ext, 'application/octet-stream')
