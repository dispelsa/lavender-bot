import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

VOICE_CHANNEL_ID = 1552806625939689472  # <-- Replace with your Voice Channel ID
AUDIO_FILE = "lavender.mp3"

async def loop_audio(vc):
    while vc.is_connected():
        if not vc.is_playing():
            # Plays the local MP3 and loops it automatically
            vc.play(discord.FFmpegPCMAudio(AUDIO_FILE))
        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect()
            bot.loop.create_task(loop_audio(vc))
        except Exception as e:
            print(f"Failed to connect to VC: {e}")

# This reads your secure token from your hosting environment
bot.run(os.environ.get('DISCORD_TOKEN'))
