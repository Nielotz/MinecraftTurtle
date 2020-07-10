import logging

# TODO: improve logger.
logger = logging.getLogger("mainLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# fh = logging.FileHandler()
# fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

from game import Game
from data_structures.host import Host
from player import Player
from versions.version import Version

if __name__ == "__main__":

    # host: Host = Host("188.68.236.16", 25565)
    host: Host = Host("51.83.170.185", 9250)
    # host: Host = Host("nssv.pl", 25565)

    player: Player = Player(username="Bob")

    game_version: Version = Version.v1_12_2

    game = Game(host, player, game_version)
    error = game.start()

    if error is not None:
        logger.error("Game has been abruptly stopped. Reason: %r", error)
    else:
        logger.info("Game has been closed.")

