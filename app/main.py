# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from .utils.terabox import TeraboxConverter
from .utils.media_player import MediaPlayerHandler
from .config import Settings

app = FastAPI(title="Terabox Converter API")
settings = Settings()
converter = TeraboxConverter()
media_handler = MediaPlayerHandler()

@app.get("/")
async def root():
    return {"status": "active", "message": "Terabox Converter API is running"}

@app.get("/convert")
async def convert_link(url: str):
    try:
        download_info = await converter.process_terabox_link(url)
        if not download_info:
            raise HTTPException(status_code=400, message="Failed to process Terabox link")
        return JSONResponse(content=download_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream")
async def stream_media(file_url: str, player: str):
    try:
        stream_url = await media_handler.prepare_stream(file_url, player)
        return {"stream_url": stream_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
