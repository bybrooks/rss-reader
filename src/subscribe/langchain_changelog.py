import feedparser
from pydantic import BaseModel
from pydantic_core import ArgsKwargs

from const import LANGCHAIN_CHANGELOG
from custom_types import ChannelType


class LangchainMetaData(BaseModel):
    """記事の本数から新着記事を判定"""

    num_read_article: int

    def __str__(self) -> str:
        return f"{self.num_read_article}"


async def retrieve_langchain_changelog(
    channel: ChannelType, metadata: LangchainMetaData
) -> LangchainMetaData:
    """
    記事本数が変わった場合、新しい記事を取得して Discord チャンネルに送信します。

    Args:
        channel (ChannelType): 新しい記事を送信するチャンネル。
        metadata (LangchainMetaData): 既に読んだ記事の数を含むメタデータ。

    Return:
        LangchainMetaData: 読んだ記事の新しい数で更新されたメタデータ。
    """
    rss = feedparser.parse(LANGCHAIN_CHANGELOG)
    all_articles = rss["entries"]

    if metadata.num_read_article < len(all_articles):
        new_articles = all_articles[: (len(all_articles) - metadata.num_read_article)]

        for article in new_articles:
            await channel.send(article["link"])
            metadata.num_read_article += 1

        return metadata

    return metadata
