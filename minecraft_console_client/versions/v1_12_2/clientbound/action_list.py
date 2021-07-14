"""Provide action_list with references to functions to run when \
received given packet ID."""

from versions.v1_12_2.clientbound import login, play

action_list = {
    "login": {
        0: login.disconnect,
        # 1: Clientbound._encryption_request,
        2: login.login_success,
        3: login.set_compression,
    },
    "play": {
        # 0x00: play.spawn_object,
        # 0x01: play.spawn_experience_orb,
        # 0x02: play.spawn_global_entity,
        # 0x03: play.spawn_mob,
        # 0x04: play.spawn_painting,
        # 0x05: play.spawn_player,
        # 0x06: play.animation,
        # 0x07: play.statistics,
        # 0x08: play.block_break_animation,
        # 0x09: play.update_block_entity,
        # 0x0A: play.block_action,
        0x0B: play.block_change,
        # 0x0C: play.boss_bar,
        0x0D: play.server_difficulty,
        # 0x0E: play.tab_complete,
        0x0F: play.chat_message,  # TODO: improve or sth
        # 0x10: play.multi_block_change,
        # 0x11: play.confirm_transaction,
        # 0x12: play.close_window,
        # 0x13: play.open_window,
        # 0x14: play.window_items,
        # 0x15: play.window_property,
        # 0x16: play.set_slot,
        # 0x17: play.set_cooldown,
        # 0x18: play.plugin_message,
        # 0x19: play.named_sound_effect,
        0x1A: play.disconnect,
        0x1B: play.entity_status,
        # 0x1C: play.explosion,
        # 0x1D: play.unload_chunk,
        0x1E: play.change_game_state,
        0x1F: play.keep_alive,
        0x20: play.chunk_data,
        # 0x21: play.effect,
        # 0x22: play.particle,
        0x23: play.join_game,
        # 0x24: play.map,
        # 0x25: play.entity,
        # 0x26: play.entity_relative_move,
        # 0x27: play.entity_look_and_relative_move,
        # 0x28: play.entity_look,
        # 0x29: play.vehicle_move,
        # 0x2A: play.open_sign_editor,
        # 0x2B: play.craft_recipe_response,
        0x2C: play.player_abilities,
        0x2D: play.combat_event,
        # 0x2E: play.player_list_item,
        0x2F: play.player_position_and_look,
        # 0x30: play.use_bed,
        # 0x31: play.unlock_recipes,
        # 0x32: play.destroy_entities,
        # 0x33: play.remove_entity_effect,
        # 0x34: play.resource_pack_send,
        0x35: play.respawn,
        # 0x36: play.entity_head_look,
        # 0x37: play.select_advancement_tab,
        # 0x38: play.world_border,
        # 0x39: play.camera,
        # 0x3A: play.held_item_change,
        # 0x3B: play.display_scoreboard,
        # 0x3C: play.entity_metadata,
        # 0x3D: play.attach_entity,
        # 0x3E: play.entity_velocity,
        # 0x3F: play.entity_equipment,
        # 0x40: play.set_experience,
        0x41: play.update_health,
        # 0x42: play.scoreboard_objective,
        # 0x43: play.set_passengers,
        # 0x44: play.teams,
        # 0x45: play.update_score,
        0x46: play.spawn_position,
        # 0x47: play.time_update,
        # 0x48: play.title,
        # 0x49: play.sound_effect,
        # 0x4A: play.player_list_header_and_footer,
        # 0x4B: play.collect_item,
        # 0x4C: play.entity_teleport,
        # 0x4D: play.advancements,
        # 0x4E: play.entity_properties,
        # 0x4F: play.entity_effect,
    }
}
