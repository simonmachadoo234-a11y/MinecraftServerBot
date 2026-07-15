import os
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
from dotenv import load_dotenv

# ================== CARGAR .ENV ==================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ ERROR: No se encontró el token en el archivo .env")
    exit()

# ================== CONFIGURACIÓN ==================
MINECRAFT_IP = "Krypt_server.aternos.me"
MINECRAFT_PORT = 43787
# ===================================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

server = JavaServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    if not check_minecraft.is_running():
        check_minecraft.start()


@tasks.loop(seconds=30)
async def check_minecraft():
    try:
        # Comprueba si el servidor responde
        server.ping()

        status = server.status()

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{status.players.online}/{status.players.max} jugadores"
            )
        )

    except Exception as e:
        print(f"Servidor offline: {e}")

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Minecraft | OFFLINE"
            )
        )


@bot.command(name="mc")
async def minecraft_status(ctx):
    mensaje = await ctx.send("🔄 Verificando servidor...")

    try:
        # Comprueba si responde
        server.ping()

        status = server.status()

        embed = discord.Embed(
            title="🟢 Servidor ONLINE",
            color=0x00ff00
        )

        embed.add_field(
            name="👥 Jugadores",
            value=f"{status.players.online}/{status.players.max}",
            inline=True
        )

        embed.add_field(
            name="📦 Versión",
            value=status.version.name,
            inline=True
        )

        embed.add_field(
            name="🌐 IP",
            value=f"`{MINECRAFT_IP}:{MINECRAFT_PORT}`",
            inline=False
        )

        if status.description:
            embed.add_field(
                name="📝 MOTD",
                value=str(status.description),
                inline=False
            )

        await mensaje.edit(content="", embed=embed)

    except Exception as e:
        print(f"Error: {e}")

        embed = discord.Embed(
            title="🔴 Servidor OFFLINE",
            description="El servidor no está encendido o no responde.",
            color=0xff0000
        )

        embed.add_field(
            name="🌐 IP",
            value=f"`{MINECRAFT_IP}:{MINECRAFT_PORT}`",
            inline=False
        )

        await mensaje.edit(content="", embed=embed)


bot.run(TOKEN)
