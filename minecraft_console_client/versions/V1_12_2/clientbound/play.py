import logging
logger = logging.getLogger("mainLogger")

from typing import NoReturn

from misc import utils
from versions.V1_12_2.serverbound import packet_creator
from misc.exceptions import DisconnectedError
from data_structures.position import Position

from gui.gui import gui


def combat_event(bot, data: bytes):
    """
    'Now only used to display the game over screen
    (with enter combat and end combat completely ignored by the Notchain client)'
     """

    event, data = utils.unpack_varint(data)

    if event == 2:  # Entity dead
        player_id, data = utils.unpack_varint(data)
        entity_id, data = utils.extract_int(data)
        message = utils.extract_json_from_chat(data)
        """ 
        'Entity ID of the player that died (should match the client's entity ID).'
        """

        if entity_id == bot._game_data.player.entity_id:

            logger.info(f"Player has been killed by: {entity_id}, "
                        f"death message: '{message}' ")

            gui.add_to_hotbar(f"Player has been killed by: {entity_id}, "
                              f"death message: '{message}' ")

            bot.on_death()
        else:
            logger.info(f"Entity: {player_id} has been killed by: {entity_id}, "
                        f"death message: '{message}' ")

            gui.add_to_hotbar(f"Entity: {player_id} has been killed "
                              f"by: {entity_id}, "
                              f"death message: '{message}' ")


def player_list_item(bot, data: bytes):
    pass


def player_position_and_look(bot, data: bytes):
    """
    Auto-sends teleport confirm, and player_position_and_look (serverbound)
    """
    _data = data[::]
    x, data = utils.extract_double(data)
    y, data = utils.extract_double(data)
    z, data = utils.extract_double(data)
    yaw, data = utils.extract_float(data)
    pitch, data = utils.extract_float(data)
    flags, teleport_id = utils.extract_byte(data)

    player = bot._game_data.player

    if player.position is None:
        player.position = Position(x, y, z)
        player_pos = player.position.pos
    else:
        player_pos = player.position.pos

        if flags & 0x01:
            player_pos["x"] += x
        else:
            player_pos["x"] = x

        if flags & 0x02:
            player_pos["y"] += y
        else:
            player_pos["y"] = y

        if flags & 0x04:
            player_pos["z"] += z
        else:
            player_pos["z"] = z

        if flags & 0x08:
            player.look_yaw += yaw
        else:
            player.look_yaw = yaw

        if flags & 0x10:
            player.look_pitch += pitch
        else:
            player.look_pitch = pitch

    logger.info(f"Player pos: {player_pos} "
                f"Look: yaw: {player.look_yaw}, "
                f"pitch: {player.look_pitch}")

    gui.set_labels(("Player position", '------------------'),
                   ("x", player_pos["x"]),
                   ("y", player_pos["y"]),
                   ("z", player_pos["z"]),
                   ("yaw", player.look_yaw),
                   ("pitch", player.look_pitch),
                   ("------------------", '------------------'))

    # Teleport confirm.
    bot.send_queue.put(packet_creator.play.teleport_confirm(teleport_id))
    # Answer player position and look.
    bot.send_queue.put(
        packet_creator.play.player_position_and_look_confirmation(_data))


def use_bed(bot, data: bytes):
    pass


def unlock_recipes(bot, data: bytes):
    pass


def destroy_entities(bot, data: bytes):
    pass


def remove_entity_effect(bot, data: bytes):
    pass


def resource_pack_send(bot, data: bytes):
    pass


def respawn(bot, data: bytes):
    game_data = bot._game_data

    game_data.player.dimension, data = utils.extract_int(data)
    game_data.difficulty = data[0]
    game_data.player.gamemode = data[1]
    game_data.level_type = utils.extract_string(data[2:])[0]

    logger.info(f"Player respawn: "
                f"gamemode: {game_data.player.gamemode}, "
                f"dimension: {game_data.player.dimension}, "
                f"game difficulty: {game_data.difficulty}, "
                f"game level_type: {game_data.level_type}, "
                )

    gui.set_labels(("dimension", game_data.player.dimension),
                   ("game difficulty", game_data.difficulty),
                   ("gamemode", game_data.player.gamemode),
                   ("game level_type", game_data.level_type))


def entity_head_look(bot, data: bytes):
    pass


def select_advancement_tab(bot, data: bytes):
    pass


def world_border(bot, data: bytes):
    pass


def camera(bot, data: bytes):
    pass


def held_item_change(bot, data: bytes):
    player = bot._game_data.player

    player.active_slot = utils.extract_byte(data)[0]
    logger.debug(f"Held slot changed to {player.active_slot}")

    gui.set_labels(("Held slot", player.active_slot))


def display_scoreboard(bot, data: bytes):
    pass


def entity_metadata(bot, data: bytes):
    pass


def attach_entity(bot, data: bytes):
    pass


def entity_velocity(bot, data: bytes):
    pass


def entity_equipment(bot, data: bytes):
    pass


def set_experience(bot, data: bytes):
    pass


def update_health(bot, data: bytes):
    player = bot._game_data.player

    player.health, data = utils.extract_float(data)
    player.food, data = utils.unpack_varint(data)
    player.food_saturation = utils.extract_float(data)[0]

    logger.info(f"Updated player. Health: {player.health} "
                f"Food: {player.food} "
                f"Food_saturation: {player.food_saturation}")

    gui.set_labels(("health", player.health),
                   ("food", player.food),
                   ("food_saturation", player.food_saturation))

    if not player.health > 0:
        bot.on_death()


def scoreboard_objective(bot, data: bytes):
    pass


def set_passengers(bot, data: bytes):
    pass


def teams(bot, data: bytes):
    pass


def update_score(bot, data: bytes):
    pass


def spawn_position(bot, data: bytes):
    position = utils.extract_position(data)[0]
    logger.info(f"Changed player spawn position to {position}")

    gui.set_labels(("Spawn position", position))


def time_update(bot, data: bytes):
    pass


def title(bot, data: bytes):
    pass


def sound_effect(bot, data: bytes):
    pass


def player_list_header_and_footer(bot, data: bytes):
    pass


def collect_item(bot, data: bytes):
    pass


def entity_teleport(bot, data: bytes):
    pass


def advancements(bot, data: bytes):
    pass


def entity_properties(bot, data: bytes):
    """
    entity_id, data = utils.unpack_varint(data)
    n_of_properties, data = utils.extract_int(data)
    for i in range(n_of_properties):
        key, data = utils.extract_string(data)
        value, data = utils.extract_double(data)
        n_of_modifiers, data = utils.unpack_varint(data)
        for j in range(n_of_modifiers):
            pass
    """


def entity_effect(bot, data: bytes):
    pass


def block_break_animation(bot, data: bytes):
    pass


def statistics(bot, data: bytes):
    pass


def animation(bot, data: bytes):
    pass


def spawn_player(bot, data: bytes):
    pass


def spawn_painting(bot, data: bytes):
    pass


def spawn_mob(bot, data: bytes):
    pass


def spawn_global_entity(bot, data: bytes):
    pass


def spawn_experience_orb(bot, data: bytes):
    pass


def spawn_object(bot, data: bytes):
    pass


def unload_chunk(bot, data: bytes):
    pass


def explosion(bot, data: bytes):
    pass


def entity_status(bot, data: bytes):
    entity_id, byte = utils.extract_int(data)
    entity_status = utils.extract_byte(data)[0]
    logger.debug(f"Entity with id: {entity_id} "
                 f"status changed to: {entity_status}")


def named_sound_effect(bot, data: bytes):
    pass


def plugin_message(bot, data: bytes):
    pass


def set_cooldown(bot, data: bytes):
    pass


def set_slot(bot, data: bytes):
    pass


def window_property(bot, data: bytes):
    pass


def window_items(bot, data: bytes):
    pass


def open_window(bot, data: bytes):
    pass


def close_window(bot, data: bytes):
    pass


def confirm_transaction(bot, data: bytes):
    pass


def multi_block_change(bot, data: bytes):
    pass


def chat_message(bot, data: bytes):
    json_data, position = utils.extract_json_from_chat(data)
    gui.add_to_chat(f"{position}: {json_data}")


def tab_complete(bot, data: bytes):
    pass


def update_block_entity(bot, data: bytes):
    pass


def server_difficulty(bot, data: bytes):
    difficulty = utils.extract_unsigned_byte(data)[0]

    bot._game_data.difficulty = difficulty

    logger.debug(f"Server difficulty: {difficulty}")

    gui.set_labels(("game difficulty",
                   {0: "peaceful", 1: "easy", 2: "normal", 3: "hard"}
                   .get(difficulty)))


def boss_bar(bot, data: bytes):
    pass


def block_action(bot, data: bytes):
    pass


def block_change(bot, data: bytes):
    pass


def change_game_state(bot, data: bytes):
    value = utils.extract_float(data[1:])[0]
    # reason = data[0]  # reason = utils.extract_unsigned_byte()[0]
    game_data = bot._game_data

    # TODO: Do sth with this:

    def invalid_bed(value: float):
        logger.info("Invalid bed")
        gui.add_to_hotbar("Invalid bed")

    def end_raining(_):
        game_data.is_raining = False
        logger.info("Stopped raining")
        gui.set_labels(("game: is_raining: ", False))

    def begin_raining(_):
        game_data.is_raining = True
        logger.info("Started raining")
        gui.set_labels(("game: is_raining: ", True))

    def change_gamemode(value: float):
        game_data.player.gamemode = {
            0: "survival",
            1: "creative",
            2: "adventure",
            3: "spectator",
        }.get(round(value))
        logger.info(f"Updated gamemode: {game_data.player.gamemode}")
        gui.set_labels((f"gamemode", game_data.player.gamemode))

    def exit_end(value: float):
        pass

    def demo_message(value: float):
        pass

    def arrow_hitting_player(bot, value: float):
        logger.info("An arrow hit a player")

    def fade_value(value: float):
        pass

    def fade_time(value: float):
        pass

    def play_elder_guardian_mob_appearance(value: float):
        pass

    {
        0: invalid_bed,
        1: end_raining,
        2: begin_raining,
        3: change_gamemode,
        4: exit_end,
        5: demo_message,
        6: arrow_hitting_player,
        7: fade_value,
        8: fade_time,
        10: play_elder_guardian_mob_appearance,
    }.get(data[0])(value)


def keep_alive(bot, data: bytes):
    bot.send_queue.put(packet_creator.play.keep_alive(data))


def chunk_data(bot, data: bytes):
    pass


def effect(bot, data: bytes):
    pass


def particle(bot, data: bytes):
    pass


def join_game(bot, data: bytes):
    game_data = bot._game_data
    player = game_data.player

    player.entity_id, data = utils.extract_int(data)

    gamemode, data = utils.extract_unsigned_byte(data)

    player.gamemode = {
        0: "survival",
        1: "creative",
        2: "adventure",
        3: "spectator",
    }.get(gamemode & 0b00000111)

    player.is_hardcore = bool(gamemode >> 3)

    player.dimension, data = utils.extract_int(data)

    game_data.difficulty, data = \
        utils.extract_unsigned_byte(data)

    """ 
    Was once used by the client to draw the player list, but now is ignored.
    bot.player._server_data["max_players"], data = \
        utils.extract_unsigned_byte(data)
     """
    data = data[1:]

    # default, flat, largeBiomes, amplified, default_1_1
    game_data.level_type = utils.extract_string(data)[0]

    # Reduced Debug Info
    # bot.player._server_data["RDI"], data = utils.extract_boolean(data)
    logger.info(f"Join game read: "
                f"player_id: {player.entity_id}, "
                f"gamemode: {player.gamemode}, "
                f"hardcore: {player.is_hardcore}, "
                f"dimension: {player.dimension}, "
                f"game difficulty: {game_data.difficulty}, "
                f"game level_type: {game_data.level_type}, "
                )

    gui.set_labels(("player_id", player.entity_id),
                   ("gamemode", player.gamemode),
                   ("is_hardcore", player.is_hardcore),
                   ("dimension", player.dimension),
                   ("game difficulty", game_data.difficulty),
                   ("game level_type", game_data.level_type))


def _map(bot, data: bytes):
    pass


def entity(bot, data: bytes):
    pass


def entity_relative_move(bot, data: bytes):
    pass


def entity_look_and_relative_move(bot, data: bytes):
    pass


def entity_look(bot, data: bytes):
    pass


def vehicle_move(bot, data: bytes):
    pass


def open_sign_editor(bot, data: bytes):
    pass


def craft_recipe_response(bot, data: bytes):
    pass


def player_abilities(bot, data: bytes):
    player = bot._game_data.player

    flags, data = utils.extract_byte(data)
    player.is_invulnerable = bool(flags & 0x01)
    player.is_flying = bool(flags & 0x02)
    player.is_allow_flying = bool(flags & 0x04)
    player.is_creative_mode = bool(flags & 0x08)

    player.flying_speed, data = utils.extract_float(data)

    player.fov_modifier = utils.extract_float(data)[0]

    logger.info("Player abilities changed: "
                f"invulnerable: {player.is_invulnerable}, "
                f"flying: {player.is_flying}, "
                f"allow_flying: {player.is_allow_flying}, "
                f"creative_mode: {player.is_creative_mode}")

    gui.set_labels(("invulnerable", player.is_invulnerable),
                   ("flying", player.is_flying),
                   ("allow_flying", player.is_allow_flying),
                   ("creative_mode", player.is_creative_mode))


def disconnect(bot, data: bytes) -> NoReturn:
    player = bot._game_data.player

    reason = utils.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    logger.error(f"{player.username} has been "
                 f"disconnected by server. Reason: '{reason['text']}'")
    raise DisconnectedError("Disconnected by server.")



