import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from minecraft import get_status
from aternos import start_server, stop_server
from permissions import (
    has_permission,
    add_user,
    remove_user,
    get_users
)

import asyncio


# ==========================
# CONFIG BOT
# ==========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==========================
# EVENTO INICIO
# ==========================

@bot.event
async def on_ready():

    print(f"✅ Bot conectado como {bot.user}")



# ==========================
# COMANDO !mc
# ==========================

@bot.command()
async def mc(ctx):

    status = get_status()


    if status["online"]:

        embed = discord.Embed(
            title="🟢 Servidor ONLINE",
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


    else:

        embed = discord.Embed(
            title="🔴 Servidor OFFLINE",
            color=0xff0000
        )


    await ctx.send(embed=embed)



# ==========================
# COMANDO !start
# ==========================

@bot.command()
async def start(ctx):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos para iniciar el servidor."
        )
        return


    msg = await ctx.send(
        "▶️ Iniciando servidor..."
    )


    result = await start_server()


    await msg.edit(
        content=result
    )



# ==========================
# COMANDO !stop
# ==========================

@bot.command()
async def stop(ctx):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos para apagar el servidor."
        )
        return


    msg = await ctx.send(
        "⏹️ Apagando servidor..."
    )


    result = await stop_server()


    await msg.edit(
        content=result
    )



# ==========================
# COMANDO !restart
# ==========================

@bot.command()
async def restart(ctx):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos."
        )
        return


    await ctx.send(
        "🔄 Reiniciando servidor..."
    )


    stop = await stop_server()

    await ctx.send(stop)


    await asyncio.sleep(10)


    start = await start_server()

    await ctx.send(start)



# ==========================
# ADMINISTRACIÓN USUARIOS
# ==========================


@bot.command()
async def adduser(ctx, member: discord.Member):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos."
        )
        return


    if add_user(member.id):

        await ctx.send(
            f"✅ {member.mention} ahora puede controlar el servidor."
        )

    else:

        await ctx.send(
            "⚠️ Ese usuario ya tiene permisos."
        )



@bot.command()
async def removeuser(ctx, member: discord.Member):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos."
        )
        return


    if remove_user(member.id):

        await ctx.send(
            f"✅ {member.mention} eliminado."
        )

    else:

        await ctx.send(
            "⚠️ Ese usuario no estaba autorizado."
        )



@bot.command()
async def listusers(ctx):

    if not has_permission(ctx.author.id):

        await ctx.send(
            "❌ No tienes permisos."
        )
        return


    users = get_users()


    if not users:

        await ctx.send(
            "No hay usuarios autorizados."
        )
        return


    lista = "\n".join(
        f"<@{user}>"
        for user in users
    )


    await ctx.send(
        f"👥 Usuarios autorizados:\n{lista}"
    )



# ==========================
# RUN
# ==========================

bot.run(DISCORD_TOKEN)
