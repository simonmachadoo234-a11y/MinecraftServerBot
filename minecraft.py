from mcstatus import JavaServer
from config import MINECRAFT_IP, MINECRAFT_PORT


server = JavaServer.lookup(
    f"{MINECRAFT_IP}:{MINECRAFT_PORT}"
)


def get_status():

    try:
        server.ping()

        status = server.status()

        return {
            "online": True,
            "players": f"{status.players.online}/{status.players.max}",
            "version": status.version.name
        }

    except:

        return {
            "online": False
        }