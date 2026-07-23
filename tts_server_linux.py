#!/usr/bin/env python3
"""TTS 音频服务 — Linux 版，基于 edge-tts (Azure 免费神经网络语音)"""
import asyncio, os, tempfile, time
from aiohttp import web

VOICE = 'en-US-JennyNeural'
PORT = 8081
CACHE_DIR = '/tmp/tts_cache'

os.makedirs(CACHE_DIR, exist_ok=True)

# 清理超过 24h 的缓存
def clean_cache():
    now = time.time()
    for f in os.listdir(CACHE_DIR):
        fp = os.path.join(CACHE_DIR, f)
        if os.path.isfile(fp) and now - os.path.getmtime(fp) > 86400:
            os.remove(fp)

async def handle_tts(request):
    text = request.query.get('text', '')
    rate_str = request.query.get('rate', '0')
    if not text:
        return web.Response(status=400, text='missing text')

    # 用 text+rate 做缓存 key
    import hashlib
    cache_key = hashlib.md5(f"{text}|{rate_str}".encode()).hexdigest() + '.mp3'
    cache_path = os.path.join(CACHE_DIR, cache_key)

    if os.path.exists(cache_path):
        return web.FileResponse(cache_path, headers={
            'Content-Type': 'audio/mpeg',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'public, max-age=86400',
        })

    # 生成音频
    try:
        rate = int(rate_str)
        rate_str_fmt = f"{'+' if rate >= 0 else ''}{rate}%"
    except:
        rate_str_fmt = '+0%'

    import edge_tts
    tts = edge_tts.Communicate(text, VOICE, rate=rate_str_fmt)
    await tts.save(cache_path)

    clean_cache()
    return web.FileResponse(cache_path, headers={
        'Content-Type': 'audio/mpeg',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=86400',
    })

async def handle_health(request):
    return web.Response(text='OK')

app = web.Application()
app.router.add_get('/tts', handle_tts)
app.router.add_get('/health', handle_health)

if __name__ == '__main__':
    print(f"TTS 服务启动: http://0.0.0.0:{PORT}/tts?text=hello")
    web.run_app(app, host='0.0.0.0', port=PORT)
