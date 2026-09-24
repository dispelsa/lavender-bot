import discord
from discord.ext import commands
import asyncio
import os
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ---- CONFIGURATION ----
VOICE_CHANNEL_ID = 1552806625939689472  
AUDIO_FILE = "lavender.mp3"  # Reads the MP3 saved directly in your folder!
# -----------------------

async def loop_audio(vc):
    while vc.is_connected():
        if not vc.is_playing():
            print("Looping local MP3 file...")
            # Automatically replays the local file every time it finishes
            vc.play(discord.FFmpegPCMAudio(AUDIO_FILE))
        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print(f"Success! {bot.user.name} is online.")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
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
        await bot.start(os.environ.get('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
