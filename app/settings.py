from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    elastic_url: str = "http://127.0.0.1:9200"