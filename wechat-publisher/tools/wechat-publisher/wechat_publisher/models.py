from pydantic import BaseModel


class Article(BaseModel):
    title: str
    author: str = ""
    content: str
    thumb_media_id: str | None = None
    digest: str | None = None
    content_source_url: str | None = None
    show_cover_pic: int = 0
    need_open_comment: int = 0
    only_fans_can_comment: int = 0


class CreateDraftRequest(BaseModel):
    articles: list[Article]


class CreateDraftResponse(BaseModel):
    media_id: str = ""


class UpdateDraftRequest(BaseModel):
    media_id: str
    index: int = 0
    articles: Article


class UpdateDraftResponse(BaseModel):
    media_id: str = ""


class UploadImageResponse(BaseModel):
    url: str = ""
