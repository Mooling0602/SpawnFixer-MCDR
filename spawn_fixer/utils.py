import glob
import os
import re
import requests
import traceback
import spawn_fixer.runtime as rt

from mcdreforged.api.types import PluginServerInterface, ServerInterface
from mcdreforged.api.rtext import RTextMCDRTranslation
from typing import Any, Callable, Optional
from uuid import UUID
from spawn_fixer.config import load_from_json

psi = ServerInterface.psi()


def execute_if(condition: bool | Callable[[], bool]):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            actual_condition = condition() if callable(condition) else condition
            if actual_condition:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


def tr(server: PluginServerInterface, key: str, to_str: Optional[bool] = None, **kwargs) -> RTextMCDRTranslation|str:
    try:
        plugin_id = server.get_self_metadata().id
        if not key.startswith("#"):
            result = server.rtr(plugin_id + "." + key, **kwargs)
        else:
            result = server.rtr(key[1:], **kwargs)
        if to_str:
            if to_str is True:
                result = str(result)
        return result
    except Exception as e:
        server.logger.error(e)


def is_uuid(uuid: str | UUID) -> bool:
    match uuid:
        case uuid if isinstance(uuid, UUID):
            return True
        case uuid if isinstance(uuid, str):
            pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
            match = re.match(pattern, uuid)
            if match:
                return True
    return False


def get_uuid_from_usercache(name: str) -> Optional[UUID]:
    if rt.config.server_path.use_mcdr_config:
        mcdr_config = psi.get_mcdr_config()
        server_path = mcdr_config["working_directory"]
    else:
        server_path = rt.config.server_path.path
    usercache = load_from_json(os.path.join(server_path, 'usercache.json'))
    for i in usercache:
        if i.get('name', None) == name:
            uuid = UUID(i.get('uuid', None))
            return uuid
    return None


def get_uuid_from_whitelist(name: str) -> Optional[UUID]:
    if rt.config.server_path.use_mcdr_config:
        mcdr_config = psi.get_mcdr_config()
        server_path = mcdr_config["working_directory"]
    else:
        server_path = rt.config.server_path.path
    whitelist = load_from_json(os.path.join(server_path, 'whitelist.json'))
    for i in whitelist:
        if i.get('name', None) == name:
            uuid = UUID(i.get('uuid', None))
            return uuid


def get_uuid_from_mojang(name: str) -> Optional[UUID]:
    try:
        resp = requests.get("https://api.mojang.com/users/profiles/minecraft/" + name)
        result = resp.json()
        uuid = result["id"]
        uuid = UUID(uuid)
    except Exception:
        error = traceback.format_exc()
        psi.logger.error(error)
        uuid = None
    return uuid


def get_uuid(name: str) -> Optional[UUID]:
    uuid_mapped = rt.uuid_map.get(name, None)
    if uuid_mapped:
        return uuid_mapped
    uuid_from_wl = get_uuid_from_whitelist(name)
    if uuid_from_wl:
        return uuid_from_wl
    uuid_from_uc = get_uuid_from_usercache(name)
    if uuid_from_uc:
        return uuid_from_uc
    uuid_from_mj = get_uuid_from_mojang(name)
    if uuid_from_mj:
        return uuid_from_mj
    return None


def get_existing_players() ->set[str]:
    world_name = rt.config.server_path.world_name
    server_path = rt.config.server_path.path
    playerdata_dir = os.path.join(server_path, world_name, "playerdata")
        
    if not os.path.isdir(playerdata_dir):
        rt.msg(f"Playerdata directory not found: {playerdata_dir}")
        return set()
        
    pattern = os.path.join(playerdata_dir, "*.dat")
    dat_files = glob.glob(pattern)
    valid_players = set()
    for file in dat_files:
        basename = os.path.basename(file)
        name_without_ext = os.path.splitext(basename)[0]
        if is_uuid(name_without_ext):
            valid_players.add(name_without_ext)
    return valid_players