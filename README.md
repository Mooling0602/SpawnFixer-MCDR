- English
- [简体中文](README_zh_cn.md)

# SpawnFixer-MCDR
SpawnFixer is a plugin working with MCDR that automatically fixes the global spawn point for each of the players.

## Principle
The principle of this plugin is to use the `/spawnpoint` command to set the spawn point for each player, when they firstly joined the server.

### Player first join detection
Plugin will read filenames of files in `</path/to/server>/<world_name>/playerdata`, and get existing players' UUID list from them.

After server startup, if a player is joining, and there is no UUID matched with his/her name before, plugin will execute the `/spawnpoint <UUID> <x> <y> <z>` to set the spawn point for him/her. And plugin will also refresh the UUID list when command execution is finished.

## Installation
Execute `!!MCDR plg install spawn_fixer [--confirm]` in MCDR console.
> Will available once this plugin is submitted successfully to MCDR PluginCatalogue.

Or download the `SpawnFixer-v*.mcdr` file from [Releases](https://github.com/MCDReforged/SpawnFixer-MCDR/releases) and put it into `</path/to/mcdr>/plugins` directory.

### Dependency
**PyPI packages need**:
- `requirements.txt`
```txt
mcdreforged
javaproperties
```

**MCDR plugins need**:
- MoreCommandNodes | [GitHub](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/more_command_nodes) | [PluginCatalogue](https://mcdreforged.com/en/plugin/more_command_nodes)
> Optional, for pos arguments check like `<x> <y> <z>`.

- AysncRconClient | [GitHub](https://github.com/Mooling0602/AsyncRconClient) | [PluginCatalogue](https://mcdreforged.com/en/plugin/async_rcon)
> Optional, another rcon support.

- Minecraft Data API | [GitHub](https://github.com/Fallen-Breath/MinecraftDataAPI) | [PluginCatalogue](https://mcdreforged.com/en/plugin/minecraft_data_api)
> Optional, get player's data by `/data` easily, and no rcon need.

## Usage
Configuration file is in `<path/to/mcdr>/config/spawn_fixer/config.yml`.
```yaml
server_path:
  - path: server
  - use_mcdr_config: true
  - world_name: world
spawnpoint:
  - x: 0
  - y: 64
  - z: 0
force_dimension: false
target_dimension: minecraft\:overworld
```

After configured, make sure you have installed necessary dependencies, and I recommend you to install other optional dependencies also.

Then, start MCDR server, and after server startup, execute `!!spawn_fixer debug` in MCDR console.

If anything goes well, you will see every check is passed, otherwise, try to fix by following the tips.

## NOTE
Gamerule `spawnRadius` is not longer supported if you use this plugin.

## Credits
- Licensed under GPLv3.
