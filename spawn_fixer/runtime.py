from spawn_fixer.config import PluginConfig


config: PluginConfig | None = None
uuid_map: dict[str, str] = {}
existing_uuids: set[str] = set()