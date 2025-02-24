import asyncio

import discord
from discord.abc import Messageable

from const import CHANNEL_ID, DISCORD_TOKEN
from custom_types import ChannelType
from subscribe import LangchainMetaData, retrieve_langchain_changelog

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def publish_new_article(channel: ChannelType, content: str) -> None:
    """
    指定されたチャンネルに新しい記事を投稿します。
    各行は、"<subscribe name>:<trigger info>"の形式で構成されている
    - subscribe name: 購読名
    - trigger info: 新着記事かどうかを判定するための情報

    Args:
    - channel (ChannelType): 記事を投稿するチャンネル。
    - content (str): すでに取得した記事のポインタ情報。
    """
    rss_subscribe_list = content.split("\n")

    read_status = {}
    for rss_object in rss_subscribe_list:
        subscribe_name, metadata = rss_object.split(":")
        read_status[subscribe_name] = metadata

        match subscribe_name:
            case "LangChain":
                metadata = LangchainMetaData(num_read_article=int(metadata))
                new_meatadata = await retrieve_langchain_changelog(channel, metadata)

                read_status[subscribe_name] = str(new_meatadata)

    new_content = "\n".join([f"{k}:{v}" for k, v in read_status.items()])
    await channel.send(new_content)


@client.event
async def on_ready() -> None:
    """
    'on_ready' イベントのイベントハンドラー。

    クライアントが正常に起動したときに呼び出されます。
    この関数は、新着記事を取得して Discord チャンネルに投稿します。
    """
    channel: ChannelType = client.get_channel(CHANNEL_ID)
    if channel and isinstance(channel, Messageable):
        async for message in channel.history(limit=1):
            try:
                await publish_new_article(channel=channel, content=message.content)
            except Exception as error:
                print(f"エラーが発生しました: {error}")
                raise RuntimeError("新着記事の取得に失敗しました") from error
    else:
        raise RuntimeError("チャンネルの型が正しくありません")
    await client.close()  # 処理が終わったらBotを閉じる


async def main() -> None:
    async with client:
        await client.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
