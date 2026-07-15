import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import os
from dotenv import load_dotenv

# Cargar el .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ ERROR: No se encontró el token en el archivo .env")
    print("Asegurate de que el archivo se llame '.env' y esté en la misma carpeta")
    input("Presiona ENTER para salir...")
    exit()

# ================== CONFIGURACIÓN ==================
MINECRAFT_IP = "Krypt_server.aternos.me"   # ← Cambia esto
MINECRAFT_PORT = 43787

MSG_ONLINE = "✅ **El servidor de Minecraft está ONLINE**"
MSG_OFFLINE = "❌ **El servidor de Minecraft está OFFLINE**"
# ===================================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

server = JavaServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    check_minecraft.start()

@tasks.loop(seconds=30)
async def check_minecraft():
    try:
        status = server.status()
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{status.players.online} en Minecraft"
        ))
    except:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Minecraft | OFFLINE"
        ))

@bot.command(name="mc")
async def minecraft_status(ctx):
    await ctx.send("🔄 Verificando servidor...")
    try:
        status = server.status()
        embed = discord.Embed(title="🟢 Servidor ONLINE", color=0x00ff00)
        embed.add_field(name="Jugadores", value=f"{status.players.online}/{status.players.max}", inline=True)
        embed.add_field(name="Versión", value=status.version.name, inline=True)
        embed.add_field(name="IP", value=f"`{MINECRAFT_IP}`", inline=False)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="🔴 Servidor OFFLINE", color=0xff0000)
        embed.add_field(name="IP", value=f"`{MINECRAFT_IP}`", inline=False)
        await ctx.send(embed=embed)

bot.run(TOKEN)