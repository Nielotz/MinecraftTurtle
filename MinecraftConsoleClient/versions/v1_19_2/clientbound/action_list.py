"""Provide action_list with references to functions to run when received given packet ID."""

from versions.v1_19_2.clientbound import login, play

action_list = {
    "login": {
        # 0x00: login.disconnect,
        # 0x01: Clientbound._encryption_request,
        # 0x02: login.login_success,
        # 0x03: login.set_compression,
        # 0x04: login.login_plugin_request,
    },
    "play": {
        # 0x00: play.spawn_entity,
        # 0x01: play.spawn_experience_orb,
        # 0x02: play.spawn_player,
        # 0x03: play.entity_animation,
        # 0x04: play.award_statistics,
        # 0x05: play.acknowledge_block_change,
        # 0x06: play.set_block_destroy_stage,
        # 0x07: play.block_entity_data,
        # 0x08: play.block_action,
        # 0x09: play.block_update,
        # 0x0A: play.boss_bar,
        # 0x0B: play.change_difficulty,
        # 0x0C: play.chat_preview,
        # 0x0D: play.clear_titles,
        # 0x0E: play.command_suggestions_response,
        # 0x0F: play.commands,
        # 0x10: play.close_container,
        # 0x11: play.set_container,
        # 0x12: play.set_container_property,
        # 0x13: play.set_container_slot,
        # 0x14: play.set_cooldown,
        # 0x15: play.chat_suggestion,
        # 0x16: play.plugin_message,
        # 0x17: play.custom_sound_effect,
        # 0x18: play.hide_message,
        # 0x19: play.disconnect,
        # 0x1A: play.entity_event,
        # 0x1B: play.explosion,
        # 0x1C: play.unload_chunk,
        # 0x1D: play.game_event,
        # 0x1E: play.open_horse_screen,
        # 0x1F: play.initialize_world_border,
        # 0x20: play.keep_alive,
        # 0x21: play.chunk_data_and_update_light,
        # 0x22: play.world_data,
        # 0x23: play.particle,
        # 0x24: play.update_light,
        # 0x25: play.login,
        # 0x26: play.map_data,
        # 0x27: play.merchant_offers,
        # 0x28: play.update_entity_position,
        # 0x29: play.update_entity_position_and_rotation,
        # 0x2A: play.update_entity_rotation,
        # 0x2B: play.move_vehicle,
        # 0x2C: play.open_book,
        # 0x2D: play.open_screen,
        # 0x2E: play.open_sign_editor,
        # 0x2F: play.ping,
        # 0x30: play.place_ghost_recipe,
        # 0x31: play.player_abilities,
        # 0x32: play.message_header,
        # 0x33: play.player_chat_message,
        # 0x34: play.end_combat,
        # 0x35: play.enter_combat,
        # 0x36: play.combat_death,
        # 0x37: play.player_info,
        # 0x38: play.look_at,
        # 0x39: play.synchronize_player_position,
        # 0x3A: play.update_recipe_book,
        # 0x3B: play.remove_entities,
        # 0x3C: play.remove_entity_effect,
        # 0x3D: play.resource_pack,
        # 0x3E: play.respawn,
        # 0x3F: play.set_head_rotation,
        # 0x40: play.update_section_blocks,
        # 0x41: play.select_advancements_tab,
        # 0x42: play.server_data,
        # 0x43: play.set_action_bar_text,
        # 0x44: play.set_border_center,
        # 0x45: play.set_border_lerp_size,
        # 0x46: play.set_border_size,
        # 0x47: play.set_border_warning_delay,
        # 0x48: play.set_border_warning_distance,
        # 0x49: play.set_camera,
        # 0x4A: play.set_held_item,
        # 0x4B: play.set_center_chunk,
        # 0x4C: play.set_render_distance,
        # 0x4D: play.set_default_spawn_position,
        # 0x4E: play.set_display_chat_preview,
        # 0x4F: play.display_objective,
        # 0x50: play.set_entity_metadata,
        # 0x51: play.link_entities,
        # 0x52: play.set_entity_velocity,
        # 0x53: play.set_equipment,
        # 0x54: play.set_experience,
        # 0x55: play.set_health,
        # 0x56: play.update_objectives,
        # 0x57: play.set_passengers,
        # 0x58: play.update_teams,
        # 0x59: play.update_score,
        # 0x5A: play.set_simulation_distance,
        # 0x5B: play.set_subtitle_text,
        # 0x5C: play.update_time,
        # 0x5D: play.set_title_text,
        # 0x5E: play.set_title_animation_times,
        # 0x5F: play.entity_sound_effect,
        # 0x60: play.sound_effect,
        # 0x61: play.stop_sound,
        # 0x62: play.system_chat_message,
        # 0x63: play.set_tab_list_header_and_footer,
        # 0x64: play.tag_query_response,
        # 0x65: play.pickup_item,
        # 0x66: play.teleport_entity,
        # 0x67: play.update_advancements,
        # 0x68: play.update_attributes,
        # 0x69: play.entity_effect,
        # 0x6A: play.update_recipes,
        # 0x6B: play.update_tags,
    }
}
