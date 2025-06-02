- 简体中文
- [English](README.md)

# SpawnFixer-MCDR
SpawnFixer是一个用于自动修复每个玩家的全局出生点的MCDR插件。

## 原理
当玩家首次加入服务器时，使用`/spawnpoint`命令为每个玩家设置重生点。

### 检测玩家首次加入
插件将读取目录`</path/to/server>/<world_name>/playerdata`下的所有文件名，从中获取已有玩家的UUID列表。

服务器启动完成后，如果有玩家加入且其名字对应的UUID在之前没有记录过，插件将执行命令`/spawnpoint <UUID> <x> <y> <z>`来设置该玩家的重生点，并在命令执行完成后刷新UUID列表。

## 安装
在MCDR控制台执行`!!MCDR plg install spawn_fixer [--confirm]`。
> 将在此插件成功提交到MCDR插件仓库后可用。

或者从[Releases](https://github.com/MCDReforged/SpawnFixer-MCDR/releases)中下载`SpawnFixer-v*.mcdr`文件，然后放到`</path/to/mcdr>/plugins`目录中去。

### 依赖
**需要的PyPI包**:
> 以下依赖将于后续版本中被需要，目前还暂未用到。
- `requirements.txt`
```txt
mcdreforged
javaproperties
```

**需要的MCDR插件**:
> 以下依赖将于后续版本中被需要，目前还暂未用到。
- MoreCommandNodes | [GitHub](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/more_command_nodes) | [PluginCatalogue](https://mcdreforged.com/en/plugin/more_command_nodes)
> 可选，用于像`<x> <y> <z>`这样的坐标参数检查。

- AysncRconClient | [GitHub](https://github.com/Mooling0602/AsyncRconClient) | [PluginCatalogue](https://mcdreforged.com/en/plugin/async_rcon)
> 可选，另外的Rcon支持。

- Minecraft Data API | [GitHub](https://github.com/Fallen-Breath/MinecraftDataAPI) | [PluginCatalogue](https://mcdreforged.com/en/plugin/minecraft_data_api)
> 可选，使用`/data`轻松获取玩家数据，并且不需要Rcon。

## 用法
配置文件应位于`<path/to/mcdr>/config/spawn_fixer/config.yml`.
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

修改完配置后，请安装所有必需依赖，并推荐同时安装所有的可选依赖。

### 调试
> 将于后续版本中实现。

## 注意
如果你使用此插件，游戏规则`spawnRadius`将不再可用。

## 许可
- 使用GPLv3协议。
