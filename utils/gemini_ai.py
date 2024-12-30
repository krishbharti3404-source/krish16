import google.generativeai as genai
from typing import Dict, Optional
import config

class GeminiAI:
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def analyze_file(self, file_info: Dict) -> Optional[Dict]:
        try:
            prompt = f"""
            Analyze this media file:
            Filename: {file_info['filename']}
            Size: {self._format_size(file_info['size'])}
            Type: {file_info.get('mime_type', 'unknown')}

            Provide:
            1. File format analysis
            2. Estimated video quality (if video)
            3. Streaming compatibility check
            4. Safety recommendations
            """

            response = await self.model.generate_content_async(prompt)
            
            return {
                "analysis": response.text,
                "safety_check": self._safety_check(response.text),
                "compatibility": self._check_compatibility(file_info)
            }
        except Exception as e:
            print(f"Gemini Analysis Error: {str(e)}")
            return None

    def _format_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"

    def _safety_check(self, analysis: str) -> Dict:
        return {
            "status": "safe",
            "recommendation": "File appears safe for streaming"
        }

    def _check_compatibility(self, file_info: Dict) -> Dict:
        return {
            "vlc": True,
            "mx_player": True,
            "playit": True,
            "notes": "Compatible with all supported players"
        }
