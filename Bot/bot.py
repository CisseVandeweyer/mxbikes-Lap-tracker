import discord
from discord import Option, Embed, Color
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests


load_dotenv()
TOKEN = os.getenv('TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')  # bv. http://127.0.0.1:8000/api

bot = discord.Bot()

# In-memory mapping van Discord ID → username (kan ook via backend)
usernames = {}

def format_lap_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    msec = int((seconds - int(seconds)) * 1000)
    if minutes == 0:
        return f"{sec}.{msec:03d}"
    return f"{minutes}:{sec:02d}.{msec:03d}"


@bot.event
async def on_ready():    
    await bot.sync_commands()
    print(f'Logged in als {bot.user}')

    # Bericht sturen in eerste kanaal
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels)
        if channel:
            try:
                await channel.send("Hey, ik ben weer online! 🚀")
            except discord.Forbidden:
                print(f"Geen permissies in {channel.name} van {guild.name}")

# Command om username in te stellen
@bot.slash_command(name="setusername", description="Stel je username in")
async def set_username(ctx, username: Option(str, "Je username")):
    discord_id = str(ctx.author.id)
    try:
        response = requests.post(f"{BACKEND_URL}/users/{discord_id}/set_username/", json={"username": username})
        if response.status_code == 201:
            usernames[ctx.author.id] = username
            await ctx.respond(f"Username ingesteld op **{username}**")
        else:
            await ctx.respond(f"Fout bij instellen username: {response.json().get('error')}")
    except Exception as e:
        await ctx.respond(f"Er is een fout opgetreden: {e}")


@bot.slash_command(name="editname", description="Edit your username")
async def edit_name(ctx, new_username: Option(str, "Your new username")):
    discord_id = str(ctx.author.id)
    try:
        response = requests.put(f"{BACKEND_URL}/users/{discord_id}/edit_username/", json={"username": new_username})
        if response.status_code == 200:
            usernames[ctx.author.id] = new_username
            await ctx.respond(f"Username aangepast naar **{new_username}**")
        else:
            await ctx.respond(f"Fout bij aanpassen username: {response.json().get('error')}")
    except Exception as e:
        await ctx.respond(f"Er is een fout opgetreden: {e}")


# Command om een lap tijd toe te voegen
@bot.slash_command(name="addlap", description="Voeg een rondetijd toe")
async def add_lap(ctx, track: Option(str, "Naam van het circuit"), time: Option(str, "Rondetijd in MM:SS.mmm")):
    discord_id = str(ctx.author.id)
    username = usernames.get(ctx.author.id)

    if not username:
        await ctx.respond("Je moet eerst je username instellen met /setusername!")
        return

    payload = {
        "username": username,
        "discord_id": discord_id,
        "track_name": track,
        "time_string": time
    }

    try:
        response = requests.post(f"{BACKEND_URL}/laps/create/", json=payload)
        if response.status_code in [200, 201]:
            await ctx.respond(f"Rondetijd **{time}** voor **{track}** toegevoegd!")
        else:
            await ctx.respond(f"Fout bij toevoegen rondetijd: {response.json().get('error')}")
    except Exception as e:
        await ctx.respond(f"Er is een fout opgetreden: {e}")



@bot.slash_command(name="laps", description="Bekijk rondetijden van een gebruiker")
async def laps(
    ctx,
    username: Option(str, "Username van de speler", required=False)
):
    # Bepaal welke gebruiker
    if username is None:
        discord_id = str(ctx.author.id)
        username = usernames.get(ctx.author.id)
        if not username:
            await ctx.respond("Geen username gevonden voor jou. Stel eerst je username in met /setusername!")
            return

    try:
        r = requests.get(f"{BACKEND_URL}/laps/user_by_username/{username}/")
        if r.status_code != 200:
            await ctx.respond(f"Fout bij ophalen rondetijden: {r.text}")
            return

        laps_data = r.json()
        if not laps_data:
            await ctx.respond(f"Geen rondetijden gevonden voor **{username}**")
            return

        # Embed met avatar
        embed = discord.Embed(
            title=f"Rondetijden voor {username}",
            color=discord.Color.blurple()
        )

        # Avatar instellen
        embed.set_thumbnail(url=ctx.author.avatar.url)

        # Voeg elke lap toe als veld
        for lap in laps_data:
            track_name = lap.get("track_display")
            lap_time_seconds = lap.get("lap_time")
            lap_time_str = format_lap_time(lap_time_seconds)
            embed.add_field(
                name=f"{track_name}",
                value=f"{lap_time_str}",
                inline=False
            )

        await ctx.respond(embed=embed)

    except Exception as e:
        await ctx.respond(f"Er is een fout opgetreden: {e}")


bot.run(TOKEN)
