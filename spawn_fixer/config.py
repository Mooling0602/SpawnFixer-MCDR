import os
import json
from typing import Any

from mcdreforged.api.all import PluginServerInterface
from pydantic import BaseModel
from ruamel.yaml import YAML

yaml: YAML = YAML()


class ConfigServerPath(BaseModel):
    path: str = "server"
    use_mcdr_config: bool = True
    world_name: str = "world"


class ConfigSpawnpoint(BaseModel):
    x: float = 0
    y: float = 64
    z: float = 0


class PluginConfig(BaseModel):
    server_path: ConfigServerPath = ConfigServerPath()
    spawnpoint: ConfigSpawnpoint | list[float | int] = ConfigSpawnpoint()
    force_dimension: bool = False
    target_dimension: str = "minecraft:overworld"


default_config: PluginConfig = PluginConfig()


def load_from_json(file_path: str) -> dict|list:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def save_to_json(file_path: str, data: dict|list):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_yml(file_path: str) -> dict|list:
    with open(file_path, 'r') as file:
        return yaml.load(file)


def save_to_yml(file_path: str, data: dict|list):
     with open(file_path, 'w') as f:
        yaml.dump(data, f)


def find_conflict_dict_keys(
    default: dict, actual: dict, prefix: str = ""
) -> tuple[set[Any], set[Any]]:
    missing = set()
    extra = set()
    if not (isinstance(default, dict) and isinstance(actual, dict)):
        return missing, extra
    for key in default:
        if key not in actual:
            missing.add(f"{prefix}{key}")
        else:
            m, e = find_conflict_dict_keys(
                default[key], actual[key], prefix=f"{prefix}{key}."
            )
            missing |= m
            extra |= e
    for key in actual:
        if key not in default:
            extra.add(f"{prefix}{key}")
    return missing, extra


def merge_dict(default: dict, actual: dict) -> dict:
    if not isinstance(default, dict) or not isinstance(actual, dict):
        return actual if actual is not None else default
    merged: dict = dict(default)
    for k, v in actual.items():
        if k in merged:
            merged[k] = merge_dict(merged[k], v)
        else:
            merged[k] = v
    return merged


def load_config(server: PluginServerInterface) -> PluginConfig:
    config_path: str = os.path.join(server.get_data_folder(), "config.yml")
    default_config_dict = PluginConfig().model_dump()
    if not os.path.exists(config_path):
        server.logger.warning("Config file not found, creating a new one...")
        save_to_yml(config_path, default_config_dict)
        return PluginConfig()
    server.logger.info("Loading config file...")
    config_dict: dict = load_from_yml(config_path)
    if not config_dict and os.path.exists(config_path):
        server.logger.error(f"Saved wrong config data: {config_dict}")
    missing_keys, extra_keys = find_conflict_dict_keys(
        PluginConfig().model_dump(), config_dict
    )
    config_format_fine: bool = missing_keys == extra_keys == set()
    if missing_keys:
        config_format_fine = False
        server.logger.warning(
            f"Missing keys in config options: {missing_keys} (will use default values instead.)"
        )
    if extra_keys:
        config_format_fine = False
        server.logger.warning(
            f"Extra keys in config options: {extra_keys} (will be ignored, but you shouldn't keep them.)"
        )
    if config_format_fine:
        return PluginConfig(**config_dict)
    merged_config_dict: dict = merge_dict(default_config_dict, config_dict)
    try:
        server.logger.warning("Merging old config with default one in plugin...")
        save_to_yml(config_path, merged_config_dict)
        return PluginConfig.model_validate(merged_config_dict, strict=False)
    except Exception as e:
        server.logger.error(f"Loading config error: {e}")
        server.logger.warning(
            "Fallback to default config, actual config file is keeping."
        )
        return PluginConfig()