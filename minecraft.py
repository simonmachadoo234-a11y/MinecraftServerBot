from mcstatus import JavaServer
from mcrcon import MCRcon
from config import MINECRAFT_IP, MINECRAFT_PORT, RCON_PASSWORD


server = JavaServer.lookup(
    f"{MINECRAFT_IP}:{MINECRAFT_PORT}"
)


def get_status():

    try:

        status = server.status()

        return {
            "online": True,
            "players": f"{status.players.online}/{status.players.max}",
            "version": status.version.name,
            "ping": round(status.latency)
        }


    except:

        return {
            "online": False
        }



def send_command(command):

    try:

        with MCRcon(
            MINECRAFT_IP,
            RCON_PASSWORD,
            port=25575
        ) as rcon:

            response = rcon.command(command)

            return response


    except Exception as e:

        return str(e)
