from pydantic import BaseModel, Field


class Envs(BaseModel):
    frontend_url: str | None = Field(default=None)
    gateway_url: str | None = Field(default=None)
    auth_url: str | None = Field(default=None)
    auth_secret: str | None = Field(default=None)  # Теперь может быть None
    spend_db_url: str | None = Field(default=None)
    test_username: str | None = Field(default=None)
    test_password: str | None = Field(default=None)
    kafka_address: str | None = Field(default=None)
    userdata_db_url: str | None = Field(default=None)  # Теперь может быть None
    soap_address: str | None = Field(default=None)  # Теперь может быть None
