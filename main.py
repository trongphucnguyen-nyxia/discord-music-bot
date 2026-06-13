import discord
from discord.ext import commands
from keep_alive import keep_alive
import asyncio
import os
from discord import FFmpegPCMAudio

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

keep_alive()  # Keeps Replit or Flask alive

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ===== JOIN =====
@bot.command()
async def join(ctx):
    """Bot joins the user's current voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            try:
                await channel.connect(timeout=30.0, reconnect=True)
                await ctx.send("🎧 SerenLunia joined your channel!")
            except Exception as e:
                await ctx.send(f"❌ Failed to connect: {e}")
        else:
            await ctx.send("⚠️ I’m already connected!")
    else:
        await ctx.send("❌ You must be in a voice channel first!")

# ===== SING =====
@bot.command()
async def sing(ctx):
    """Plays the uploaded MP3 file once."""
    voice = ctx.voice_client
    if voice is None:
        await ctx.invoke(bot.get_command("join"))
        voice = ctx.voice_client

    if voice:
        try:
            source = FFmpegPCMAudio("hat_bui_nao.mp3")
            voice.play(source)
            await ctx.send("🎶 SerenLunia is singing *Hạt Bụi Nào* 🌙")
        except Exception as e:
            await ctx.send(f"⚠️ Error: {e}")
    else:
        await ctx.send("⚠️ Still can’t connect to voice — Replit might be blocking voice temporarily.")

# ===== LOOP =====
@bot.command()
async def loop(ctx):
    """Loops the song forever."""
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.invoke(bot.get_command("join"))
        voice_client = ctx.voice_client

    if voice_client:
        async def play_loop():
            while True:
                source = FFmpegPCMAudio("hat_bui_nao.mp3")
                voice_client.play(source)
                while voice_client.is_playing():
                    await asyncio.sleep(1)

        await ctx.send("🔁 Looping *Hạt Bụi Nào* forever...")
        bot.loop.create_task(play_loop())
    else:
        await ctx.send("⚠️ Could not connect to a voice channel.")

# ===== VOICE CONTROLS =====
@bot.command()
async def pause(ctx):
    """Pauses the current song."""
    voice = ctx.voice_client
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("⏸️ Paused the song.")
    else:
        await ctx.send("⚠️ Nothing is playing right now!")

@bot.command()
async def resume(ctx):
    """Resumes a paused song."""
    voice = ctx.voice_client
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("▶️ Resumed the song.")
    else:
        await ctx.send("⚠️ Nothing to resume!")

@bot.command()
async def stop(ctx):
    """Stops the song completely."""
    voice = ctx.voice_client
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("⏹️ Stopped the song.")
    else:
        await ctx.send("⚠️ Nothing is playing to stop.")

# ===== LEAVE =====
@bot.command()
async def leave(ctx):
    """Disconnects the bot from voice."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 SerenLunia left the voice channel.")
    else:
        await ctx.send("⚠️ I’m not in a voice channel!")

# ===== TOKEN START =====
token = os.getenv("TOKEN")
if not token:
    print("❌ TOKEN not found! Make sure you set it in Replit Secrets or via 'set TOKEN=...'")
else:
    bot.run(token)
