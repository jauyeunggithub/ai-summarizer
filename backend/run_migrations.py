from alembic import command
from alembic.config import Config
import os


db_url = os.getenv('DATABASE_URL')
config = Config("alembic.ini")
config.set_main_option("sqlalchemy.url", db_url)

revision = "head"


def run_migrations_online():
    command.upgrade(config, revision)


if __name__ == "__main__":
    run_migrations_online()
