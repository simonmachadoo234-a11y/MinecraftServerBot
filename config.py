import os
from dotenv import load_dotenv

load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MINECRAFT_IP = os.getenv("MINECRAFT_IP")

MINECRAFT_PORT = int(
    os.getenv("MINECRAFT_PORT", 25565)
)

STATUS_CHANNEL = int(
    os.getenv("STATUS_CHANNEL")
)
