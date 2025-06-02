# from mcdreforged.api.command import CommandContext, SimpleCommandBuilder
# from mcdreforged.api.types import CommandSource, PluginServerInterface
# from mcdreforged.api.rtext import RText, RTextList, RColor, RAction

# builder = SimpleCommandBuilder()


# def build_command_node_spawnpoint_set(server: PluginServerInterface):
#     try:
#         from more_command_nodes import Position # type: ignore
#     except ModuleNotFoundError:
#         command = "!!spawn_fixer resolve_dependency"
#         rtext = RTextList(
#             RText("Install dependency by "),
#             RText(command, RColor.yellow, RAction.suggest_command(command))
#         )
#         server.logger.error("Missing mcdr plugin dependency: MoreCommandNodes")
#         server.logger.error(rtext)
#         server.broadcast(rtext)
#         return