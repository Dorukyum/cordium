from typing import Literal, TypedDict

EmbedType = Literal["rich", "image", "video", "gifv", "article", "link"]


class _EmbedThumbnailOptional(TypedDict, total=False):
    proxy_url: str
    height: int
    width: int


class EmbedThumbnail(_EmbedThumbnailOptional):
    url: str


EmbedImage = EmbedThumbnail


class EmbedVideo(TypedDict, total=False):  # all optional
    url: str
    proxy_url: str
    height: int
    width: int


class EmbedProvider(TypedDict, total=False):  # all optional
    name: str
    url: str


class _EmbedFooterOptional(TypedDict, total=False):
    icon_url: str
    proxy_icon_url: str


class EmbedFooter(_EmbedFooterOptional):
    text: str


class _EmbedAuthorOptional(TypedDict, total=False):
    url: str
    icon_url: str
    proxy_icon_url: str


class EmbedAuthor(_EmbedAuthorOptional):
    name: str


class _EmbedFieldOptional(TypedDict, total=False):
    inline: bool


class EmbedField(_EmbedFieldOptional):
    name: str
    value: str


class Embed(TypedDict, total=False):  # all optional
    title: str
    type: EmbedType
    description: str
    url: str
    timestamp: int
    color: int
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: list[EmbedField]
