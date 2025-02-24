from typing import TypeAlias

from discord.abc import GuildChannel, Messageable, PrivateChannel

ChannelType: TypeAlias = GuildChannel | Messageable | PrivateChannel | None
