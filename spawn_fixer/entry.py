import re
import spawn_fixer.runtime as rt

from mcdreforged.api.types import PluginServerInterface, Info
from spawn_fixer.config import load_config, PluginConfig, ConfigSpawnpoint, default_config
from spawn_fixer.utils import tr, get_uuid, get_existing_players


def on_load(server: PluginServerInterface, _prev_module):
    server.logger.debug("lifecycle: loading config")
    config: PluginConfig = load_config(server)
    if config == PluginConfig():
        server.logger.warning(tr(server, "on_load.warn"))
    server.logger.debug("lifecycle: config -> module:runtime.config")
    rt.config = config
    if rt.config.spawnpoint == default_config.spawnpoint:
        server.logger.warning(tr(server, "on_default_config"))
    rt.existing_uuids = get_existing_players()
    server.logger.info(tr(server, "on_load.finish"))
    server.logger.debug("lifecycle: exiting on_load stage.")


def on_info(server: PluginServerInterface, info: Info):
    pattern = r'UUID of player (.\w+|\w+) is ([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})'
    match = re.match(pattern, info.content.strip())
    if not match:
        return
    player, uuid = match.groups()
    rt.uuid_map[player] = uuid
    server.logger.debug(f'parser: {{"{player}": "{uuid}"}} -> module:runtime.uuid_map')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    # CleMooling[/117.178.115.59:56466] logged in with entity id 12520 at ([world]47.869686, -51.0, 166.78632)
    uuid = get_uuid(player)
    if not uuid:
        return
    if uuid not in rt.existing_uuids:
        server.logger.info(tr(server, "on_player_joined", player=player))
        set_spawnpoint(server, player)
        rt.existing_uuids.add(uuid)


def set_spawnpoint(server: PluginServerInterface, player: str):
    spawnpoint =  rt.config.spawnpoint
    match spawnpoint:
        case spawnpoint if isinstance(spawnpoint, ConfigSpawnpoint):
            x = spawnpoint.x
            y = spawnpoint.y
            z = spawnpoint.z
        case spawnpoint if isinstance(spawnpoint, list):
            x = spawnpoint[0]
            y = spawnpoint[1]
            z = spawnpoint[2]
        case _:
            raise RuntimeError(tr(server, "on_error"))
    assert None not in (x, y, z)
    for coord in ('x', 'y', 'z'):
        value = locals()[coord]
        if isinstance(value, float) and not value.is_integer():
            locals()[coord] = int(round(value))
    spawn_command = f"spawnpoint {player} {x} {y} {z}"
    tp_command = f"tp {player} {x} {y} {z}"
    if rt.config.force_dimension:
        if rt.config.force_dimension != "minecraft:overworld":
            spawn_command = f"execute in {rt.config.target_dimension} run {spawn_command}"
            tp_command = f"execute in {rt.config.target_dimension} run {tp_command}"
        else:
            spawn_command = f"execute in minecraft:overworld run {spawn_command}"
            tp_command = f"execute in minecraft:overworld run {tp_command}"
    server.execute(spawn_command)
    server.execute(tp_command)
    server.logger.info(tr(server, "on_set_spawnpoint", player=player, spawnpoint=f"{x}, {y}, {z}"))
        