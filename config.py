import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

MINECRAFT_IP = os.getenv("MINECRAFT_IP")
MINECRAFT_PORT = int(os.getenv("MINECRAFT_PORT", 25565))