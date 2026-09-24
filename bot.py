import discord
from discord.ext import commands
import asyncio
import os
import yt_dlp
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ---- CONFIGURATION ----
VOICE_CHANNEL_ID = 1552806625939689472  
LAVENDER_URL = "https://youtube.com" 
# -----------------------

async def loop_audio(vc):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    
    ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

    while vc.is_connected():
        if not vc.is_playing():
            print("Extracting stream from YouTube...")
            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(LAVENDER_URL, download=False))
                audio_url = data['url']
                
                print("Streaming your custom Lavender Town loop!")
                vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
            except Exception as e:
                print(f"Streaming error: {e}")
        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print(f"Success! {bot.user.name} is online and connected.")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
            bot.loop.create_task(loop_audio(vc))
        except Exception as e:
            print(f"Failed to connect to Voice Channel: {e}")

# Fake web server server to satisfy Render's port checks
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Pulls the port Render expects dynamically
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server trick running on port {port}")

async def main():
    async with bot:
        bot.loop.create_task(start_web_server())
        await bot.start(os.environ.get('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
