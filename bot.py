import discord
from discord.ext import commands, tasks

from config import (
    DISCORD_TOKEN,
    STATUS_CHANNEL,
    MINECRAFT_IP,
    MINECRAFT_PORT
)

from minecraft import get_status


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


ultimo_estado = None


@bot.event
async def on_ready():

    print(f"✅ Bot conectado como {bot.user}")

    actualizar_estado.start()



# ==========================
# CANAL AUTOMATICO
# ==========================

@tasks.loop(minutes=5)
async def actualizar_estado():

    global ultimo_estado


    canal = bot.get_channel(
        STATUS_CHANNEL
    )


    if canal is None:
        return


    status = get_status()


    if status["online"]:

        nombre = (
            f"🟢 Krypt "
            f"{status['players']}"
        )

        estado = True


    else:

        nombre = "🔴 Krypt OFFLINE"

        estado = False



    await canal.edit(
        name=nombre
    )


    if ultimo_estado != estado:

        if estado:

            await canal.send(
                "🟢 El servidor de Minecraft está ONLINE"
            )

        else:

            await canal.send(
                "🔴 El servidor de Minecraft está OFFLINE"
            )


    ultimo_estado = estado




# ==========================
# !mc
# ==========================

@bot.command()
async def mc(ctx):

    status = get_status()


    if not status["online"]:

        await ctx.send(
            "🔴 El servidor está offline"
        )

        return



    embed = discord.Embed(
        title="🟢 Minecraft ONLINE",
        color=0x00ff00
    )


    embed.add_field(
        name="👥 Jugadores",
        value=status["players"]
    )


    embed.add_field(
        name="📦 Versión",
        value=status["version"]
    )


    embed.add_field(
        name="🏓 Ping",
        value=f"{status['ping']}ms"
    )


    await ctx.send(
        embed=embed
    )



# ==========================
# !ip
# ==========================

@bot.command()
async def ip(ctx):

    await ctx.send(
        f"🌐 IP del servidor:\n"
        f"`{MINECRAFT_IP}:{MINECRAFT_PORT}`"
    )



# ==========================
# !players
# ==========================

@bot.command()
async def players(ctx):

    status = get_status()


    if not status["online"]:

        await ctx.send(
            "🔴 Servidor offline"
        )

        return


    if not status["player_list"]:

        await ctx.send(
            "👥 No hay jugadores conectados"
        )

        return


    lista = "\n".join(
        status["player_list"]
    )


    await ctx.send(
        f"👥 Jugadores online:\n```{lista}```"
    )



# ==========================
# !ping
# ==========================

@bot.command()
async def ping(ctx):

    status = get_status()


    if status["online"]:

        await ctx.send(
            f"🏓 Ping: `{status['ping']}ms`"
        )

    else:

        await ctx.send(
            "🔴 Servidor offline"
        )



# ==========================
# !info
# ==========================

@bot.command()
async def info(ctx):

    status = get_status()


    embed = discord.Embed(
        title="📌 Krypt Server",
        color=0x3498db
    )


    embed.add_field(
        name="🌐 IP",
        value=f"{MINECRAFT_IP}:{MINECRAFT_PORT}",
        inline=False
    )


    if status["online"]:

        embed.add_field(
            name="🟢 Estado",
            value="Online"
        )

        embed.add_field(
            name="👥 Jugadores",
            value=status["players"]
        )

        embed.add_field(
            name="📦 Versión",
            value=status["version"]
        )

    else:

        embed.add_field(
            name="🔴 Estado",
            value="Offline"
        )


    await ctx.send(
        embed=embed
    )



# ==========================
# !status
# ==========================

@bot.command()
async def status(ctx):

    data = get_status()


    if data["online"]:

        await ctx.send(
            f"🟢 Online | "
            f"{data['players']}"
        )

    else:

        await ctx.send(
            "🔴 Offline"
        )



# ==========================
# AYUDA
# ==========================

@bot.command()
async def help(ctx):

    embed = discord.Embed(
        title="🤖 Comandos Krypt Bot",
        color=0x7289da
    )


    embed.description = """
`!mc` - Estado completo
`!ip` - IP del servidor
`!players` - Jugadores online
`!ping` - Ping
`!info` - Información
`!status` - Estado rápido
"""


    await ctx.send(embed=embed)



bot.run(DISCORD_TOKEN)
