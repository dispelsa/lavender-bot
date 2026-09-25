import discord
from discord.ext import commands
import asyncio
import os
import random
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ---- CONFIGURATION ----
VOICE_CHANNEL_ID = 1552806625939689472  
TEXT_CHANNEL_ID = 123456789012345678    # <-- Make sure this is your Text Channel ID!
AUDIO_FILE = "lavender.mp3"  
# -----------------------

async def loop_audio(vc):
    # Optimized arguments to prevent broken pipe disconnect errors
    FFMPEG_OPTIONS = {
        'options': '-vn -loglevel error'
    }
    
    while vc.is_connected():
        if not vc.is_playing():
            print("Looping local MP3 file...")
            try:
                vc.play(discord.FFmpegPCMAudio(AUDIO_FILE, **FFMPEG_OPTIONS))
            except Exception as e:
                print(f"Playback loop error: {e}")
        await asyncio.sleep(2)

async def random_chat_injector():
    await bot.wait_until_ready()
    text_channel = bot.get_channel(TEXT_CHANNEL_ID)
    
    if text_channel:
        print(f"Random chatter activated for channel: {text_channel.name}")
        while not bot.is_closed():
            await asyncio.sleep(1800)  # Rolls every 30 minutes
            if random.randint(1, 3) == 1:  # 33% chance to type
                try:
                    await text_channel.send("lavender rules ?")
                except Exception as e:
                    print(f"Could not send random text: {e}")

@bot.event
async def on_ready():
    print(f"Success! {bot.user.name} is online.")
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
        try:
            # Force standard fallback paths to stabilize the cloud connection
            vc = await voice_channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
            bot.loop.create_task(loop_audio(vc))
        except Exception as e:
            print(f"Failed to connect to Voice Channel: {e}")

async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    async with bot:
        bot.loop.create_task(start_web_server())
        bot.loop.create_task(random_chat_injector())
        await bot.start(os.environ.get('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
