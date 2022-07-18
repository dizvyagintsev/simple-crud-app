from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str = "postgres"
    db_password: str
    db_server: str = "db"
    db_name: str = "postgres"
    driver: str = "postgresql+asyncpg"

    @property
    def db_url(self):
        return f"{self.driver}://{self.db_user}:{self.db_password}@{self.db_server}/{self.db_name}"


settings = Settings()
