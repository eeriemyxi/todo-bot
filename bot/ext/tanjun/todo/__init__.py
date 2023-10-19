import tanjun

from bot.ext.tanjun.todo.core import component


@tanjun.as_loader
def load_module(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_module(client: tanjun.abc.Client) -> None:
    client.remove_component_by_name(component.name)
