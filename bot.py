import discord
from discord import app_commands
from discord.ext import commands
from config import DISCORD_TOKEN
from permissions import (
    has_permission,
    add_user,
    remove_user,
    get_users
)
from minecraft import get_status
from aternos import start_server, stop_server


# ==========================
# BOT CONFIG
# ==========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)



# ==========================
# EVENTOS
# ==========================


@bot.event
async def on_ready():

    print(f"✅ Conectado como {bot.user}")

    try:

        synced = await bot.tree.sync()

        print(
            f"✅ {len(synced)} comandos sincronizados"
        )

    except Exception as e:

        print(
            f"Error sincronizando comandos: {e}"
        )



# ==========================
# /mc
# ==========================


@bot.tree.command(
    name="mc",
    description="Ver estado del servidor Minecraft"
)
async def mc(interaction: discord.Interaction):

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


    await interaction.response.send_message(
        embed=embed
    )



# ==========================
# /start
# ==========================


@bot.tree.command(
    name="start",
    description="Encender servidor"
)
async def start(interaction: discord.Interaction):


    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return



    await interaction.response.send_message(
        "▶️ Iniciando servidor..."
    )


    result = await start_server()


    await interaction.followup.send(
        result
    )



# ==========================
# /stop
# ==========================


@bot.tree.command(
    name="stop",
    description="Apagar servidor"
)
async def stop(interaction: discord.Interaction):


    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return



    await interaction.response.send_message(
        "⏹️ Apagando servidor..."
    )


    result = await stop_server()


    await interaction.followup.send(
        result
    )



# ==========================
# /restart
# ==========================


@bot.tree.command(
    name="restart",
    description="Reiniciar servidor"
)
async def restart(interaction: discord.Interaction):


    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return



    await interaction.response.send_message(
        "🔄 Reiniciando..."
    )


    stop = await stop_server()

    await interaction.followup.send(
        stop
    )


    import asyncio

    await asyncio.sleep(10)


    start = await start_server()


    await interaction.followup.send(
        start
    )

# ==========================
# /adduser
# ==========================

@bot.tree.command(
    name="adduser",
    description="Dar permisos a un usuario"
)
@app_commands.describe(
    user="Usuario que tendrá permisos"
)
async def adduser(
    interaction: discord.Interaction,
    user: discord.Member
):

    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return


    added = add_user(user.id)


    if added:

        msg = f"✅ {user.mention} ahora puede usar comandos de control."

    else:

        msg = "⚠️ Ese usuario ya tenía permisos."


    await interaction.response.send_message(msg)



# ==========================
# /removeuser
# ==========================


@bot.tree.command(
    name="removeuser",
    description="Quitar permisos a un usuario"
)
@app_commands.describe(
    user="Usuario a quitar"
)
async def removeuser(
    interaction: discord.Interaction,
    user: discord.Member
):

    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return


    removed = remove_user(user.id)


    if removed:

        msg = f"✅ {user.mention} eliminado."

    else:

        msg = "⚠️ Ese usuario no estaba en la lista."


    await interaction.response.send_message(msg)



# ==========================
# /listusers
# ==========================


@bot.tree.command(
    name="listusers",
    description="Ver usuarios autorizados"
)
async def listusers(interaction: discord.Interaction):


    if not has_permission(interaction.user.id):

        await interaction.response.send_message(
            "❌ No tienes permisos.",
            ephemeral=True
        )

        return


    users = get_users()


    if not users:

        text = "No hay usuarios autorizados."

    else:

        text = "\n".join(
            f"<@{u}>"
            for u in users
        )


    await interaction.response.send_message(
        f"👥 Usuarios autorizados:\n{text}"
    )

# ==========================
# RUN
# ==========================


bot.run(DISCORD_TOKEN)