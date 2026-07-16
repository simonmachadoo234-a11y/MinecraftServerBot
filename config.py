import os
from dotenv import load_dotenv

load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

STATUS_CHANNEL = int(
    os.getenv("STATUS_CHANNEL", "0")
)


# Minecraft
MINECRAFT_IP = "Krypt_server.aternos.me"
MINECRAFT_PORT = 43787
