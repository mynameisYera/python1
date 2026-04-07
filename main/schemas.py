"""
Pydantic-схемы для входящего JSON (тело запросов).

BaseModel — «контракт» полей: типы, значения по умолчанию, алиасы имён из JSON.
Документация: https://docs.pydantic.dev/latest/
"""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator


class RegisterBody(BaseModel):
    """
    Тело POST /register/.

    В JSON можно писать firstName/lastName (как на фронте) или first_name/last_name.
    """

    model_config = ConfigDict(str_strip_whitespace=True, extra='ignore')

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: str = ''
    first_name: str = Field(
        validation_alias=AliasChoices('firstName', 'first_name'),
        min_length=1,
    )
    last_name: str = Field(
        validation_alias=AliasChoices('lastName', 'last_name'),
        min_length=1,
    )

    @field_validator('email', mode='before')
    @classmethod
    def empty_email_to_str(cls, v):
        if v is None:
            return ''
        return v


class ItemCreate(BaseModel):
    """POST /items/ — создание строки."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    content: str = ''


class ItemUpdate(BaseModel):
    """PATCH /items/<id>/ — частичное обновление."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None

    @model_validator(mode='after')
    def at_least_one_field(self):
        if self.title is None and self.content is None:
            raise ValueError('provide at least one of: title, content')
        return self
