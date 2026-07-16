from mcstatus import JavaServer
from config import MINECRAFT_IP, MINECRAFT_PORT


def get_status():

    try:

        server = JavaServer.lookup(
            f"{MINECRAFT_IP}:{MINECRAFT_PORT}"
        )

        status = server.status()


        players = []

        if status.players.sample:

            players = [
                p.name
                for p in status.players.sample
            ]


        return {
            "online": True,
            "players": f"{status.players.online}/{status.players.max}",
            "player_list": players,
            "version": status.version.name,
            "ping": round(status.latency)
        }


    except Exception:

        return {
            "online": False
        }
