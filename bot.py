import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ---- CONFIGURATION ----
VOICE_CHANNEL_ID = 1552806625939689472  
# Uses a clean, direct audio stream URL to bypass heavy library requirements
LAVENDER_URL = "https://www.youtube.com/watch?v=hYutjYdFc7I&list=RDhYutjYdFc7I&start_radio=1"
# -----------------------

async def loop_audio(vc):
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    while vc.is_connected():
        if not vc.is_playing():
            print("Streaming Lavender Town theme...")
            vc.play(discord.FFmpegPCMAudio(LAVENDER_URL, **FFMPEG_OPTIONS))
        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print(f"Success! {bot.user.name} is now streaming live.")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect(reconnect=True, timeout=60.0, self_deaf=True)
            bot.loop.create_task(loop_audio(vc))
        except Exception as e:
            print(f"Failed to connect to Voice Channel: {e}")

bot.run(os.environ.get('DISCORD_TOKEN'))
