"""Apply pending database migrations.

`flask db upgrade` can't load this app (the CLI imports it as backend.main, which breaks the
`import models` style imports), so run this instead:

    python db_upgrade.py                              # locally, from backend/
    heroku run python backend/db_upgrade.py           # production
"""
import os

from flask_migrate import upgrade

from config import ProdConfig
from main import create_app

MIGRATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')

app = create_app(ProdConfig)

if __name__ == '__main__':
    with app.app_context():
        upgrade(directory=MIGRATIONS)
        print('Database is up to date.')
