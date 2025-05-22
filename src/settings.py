import os

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from os import environ
class OCMSettings(BaseSettings):
    if not Path('.env').exists():
        contents=''
        if os.environ.get('OCM_API_TOKEN'):
            contents += f'OCM_API_TOKEN={os.environ["OCM_API_TOKEN"]}'
        if os.environ.get('OCM_API_URL'):
            contents += f'\nOCM_API_URL={os.environ["OCM_API_URL"]}'
        if contents:
            open('.env', 'w').write(contents)

    model_config = SettingsConfigDict(env_prefix="OCM_", env_file=".env", extra="ignore")

    api_token: str = Field(description="OpenShift Cluster Manager API Token")
    api_url: AnyHttpUrl = Field(
        default=AnyHttpUrl("https://api.openshift.com"),
        description="OpenShift Cluster Manager API base URL",
    )


settings = OCMSettings()