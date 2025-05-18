from alembic import command
from alembic.config import Config


with open("/run/secrets/db_password.txt", "r") as secret_file:
    db_password = secret_file.read().strip()

db_url = f"postgresql://postgres:{db_password}@db:5432/postgres"

config = Config("alembic.ini")
config.set_main_option("sqlalchemy.url", db_url)

revision = "head"


def run_migrations_online():
    command.upgrade(config, revision)


if __name__ == "__main__":
    run_migrations_online()
