import versions.defaults.clientbound.action_list as clientbound_action_list
import versions.defaults.serverbound.packet_creator as serverbound_packet_creator


class VersionData:
    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils.

    packet_creator = serverbound_packet_creator
    action_list = clientbound_action_list.action_list
