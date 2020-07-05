import logging
import queue
from typing import Any, TYPE_CHECKING

logger = logging.getLogger('mainLogger')

from versions.version import Version
from connection import Connection
from misc import utils
from data_structures.game_data import GameData
from data_structures.player import Player
from data_structures.host import Host
from action.move_manager import MoveManager
from misc.exceptions import DisconnectedError

if TYPE_CHECKING:
    import versions.defaults


class Bot:
    """
    Manages bot behavior. Highest programmer API level.
    Imitate last stage e.g. "game" in `os->client->GAME`
    """

    version_data: Version = None
    login_packet_creator = None  # Module
    play_packet_creator = None  # Module
    clientbound_action_list: dict = None

    received_queue: queue.Queue = None
    send_queue: queue.Queue = None
    move_manager: MoveManager = None

    game_data: GameData = None
    host: Host = None

    _conn: Connection = None

    def __init__(self, host: Host, version: Version, username: str):
        """
        :param host: host data (Host) to which client connects to
        :param version: Version, tells which version of protocol to use
        :param username: player's username
        """

        self.host = host
        self.version_data: versions.defaults.VersionData = version.value

        self.game_data = GameData()
        self.game_data.player = Player()
        self.game_data.player.username = username

        logger.info(
            f"\n{'Created bot'.center(80, '-')}\n" +
            "|" + f"Username: '{username}'".center(78, " ") + "|\n" +
            "|" + f"Client version: '{self.version_data.release_name}'"
            .center(78, " ") + "|\n" +
            "|" + f"Socket data: {self.host.socket_data}"
            .center(78, " ") + "|\n" +
            "".center(80, "-"))

        if not self.switch_action_packets("login"):
            raise RuntimeError("Not found 'login' in action_packet")

        self.play_packet_creator = self.version_data.packet_creator.play
        self.login_packet_creator = self.version_data.packet_creator.login

        self._conn = Connection()

        self.send_queue: queue.Queue = queue.Queue()
        self.received_queue: queue.Queue = queue.Queue()

        self.move_manager = MoveManager(self.send_queue,
                                        self.play_packet_creator,
                                        self.game_data.player)

    def __del__(self):
        logger.info("Deleting bot")
        if self._conn is not None:
            self._conn.__del__()
            self._conn: None = None

    def start(self) -> str:
        """
        Starts bot.
        Returns error message, or - when everything worked as expected - "".

        :return error message
        :rtype str
        """

        logger.info(f"Starting bot: '{self.game_data.player.username}'.")

        if not self.connect_to_server():
            return "Can't connect to the server"
        logger.info("Successfully connected to the server.")

        if not self.start_listening():
            return "Cannot start listener"
        logger.debug("Successfully started listening thread")

        if not self.start_sending():
            return "Cannot start sender"
        logger.debug("Successfully started sending thread")

        if not self.login_non_premium():
            return "Can't connect to the server"
        logger.info("Successfully logged in to server.")

        if not self.switch_action_packets("play"):
            return "Can't assign 'play' action packet."

        if not self.move_manager.start():
            return "Can't start move manager."

        while True:
            data = self.received_queue.get(timeout=10)

            if len(data) == 0:
                return "Received 0 bytes"
            packet_id, packet = utils.extract_varint(data)
            self._interpret_packet(packet_id, packet)

    def start_sending(self) -> bool:
        """ See Connection.start_sender(). """
        return self._conn.start_sender(self.send_queue)

    def start_listening(self):
        """ See Connection.start_listener(). """
        return self._conn.start_listener(self.received_queue)

    def exit(self, reason="not defined"):
        """ Exits bot stopping stuff and others. """
        logger.info(f"Stopping bot '{self.game_data.player.username}'. "
                    f"Reason: {reason}")
        self._conn.__del__()
        self._conn: None = None

    def login_non_premium(self) -> bool:
        """
        #TODO: when login_premium done, write what da fuk is dat.

        :return success
        :rtype bool
        """

        logger.info("Trying to log in in offline mode (non-premium).")

        self.send_queue.put(
            self.login_packet_creator.handshake(self.host.get_host_data()))

        self.send_queue.put(
            self.login_packet_creator.login_start(
                self.game_data.player.username))

        # Try to log in for 50 sec (10 sec x 5 packets)
        for i in range(5):
            data = self.received_queue.get(timeout=10)
            if data == b'':
                logger.error("Received 0 bytes")
                return False
            packet_id, data = utils.extract_varint(data)

            try:
                if self._interpret_packet(packet_id, data):
                    return True
            except DisconnectedError:
                self.send_queue.put(b'')
                return False
            except Exception as e:
                logger.critical(f"<bot#1>Uncaught exception "
                                f"[{e.__class__.__name__}] occurred:  {e} ")
                print("FOUND UNEXPECTED EXCEPTION\n" * 20)
                self.send_queue.put(b'')
                return False

        return False

    def connect_to_server(self, timeout=5) -> bool:
        """
        Establishes connection with the server.
        Not raises exceptions.

        :param timeout: connection timeout
        :returns: success
        :rtype: bool
        """

        try:
            self._conn.connect(self.host.get_host_data(), timeout)
        except OSError as e:
            logger.critical(
                f"Can't connect to: {self.host.socket_data}, reason: {e}")
            return False

        logger.info(f"Established connection with: {self.host.socket_data}")
        return True

    def switch_action_packets(self, actions_type: str = "login") -> bool:
        """
        Switches between different action types.
        To see possible action types see:
            versions.<version>.clientbound.action_list.py

        Based on V1_12_2:
            Possible types: login, play, status.

        :return success
        :rtype bool
        """

        self.clientbound_action_list = \
            self.version_data.action_list.get(actions_type)
        return self.clientbound_action_list is not None

    def _interpret_packet(self, packet_id: int, payload: bytes) -> Any:
        """
        Interprets given packet and calls function assigned to packet_id
        in action_list.

        :param packet_id: int representing packet id e.g 0,1,2,3,4...
        :param payload: uncompressed data
        :return: whatever action_list[packet_id]() returns
        """

        if packet_id in self.clientbound_action_list:
            return self.clientbound_action_list[packet_id](self, payload)
        else:
            logger.debug(f"Packet with id: {packet_id} is not implemented yet")
            return None

    def on_death(self):
        """ Defines what to do when player died. """
        logger.info("Player has dead. Respawning.")
        self.send_queue.put(self.play_packet_creator.client_status(0))
