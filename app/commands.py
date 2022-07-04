import os
import traceback

import click
from flask.cli import with_appcontext
from flask import current_app

from app.models import Role, User, Setting, Pooja
from app.services import db, india_time
from app.tasks import send_email


def create() -> None:
    """Creates the database."""
    db.create_all()
    db.session.commit()
    print('Database Created!')


def clear(confirm=None) -> None:
    """Clears the database."""
    if not confirm:
        confirm = input('Are you sure you want to clear the database? [y/n]: ')
    if confirm == 'y':
        db.drop_all()
        db.session.commit()
        print('Database Cleared!')
    else:
        print('command aborted')


def add_data() -> None:
    """Adds admin and users for testing."""
    admin_role = Role.create(name='admin')
    user_role = Role.create(name='user')

    User.create(role=admin_role, email='creatixdevelopers@gmail.com', password='password')
    User.create(role=user_role, email=f'test@test.com', password='password')
    User.create(role=user_role, email=f'test1@test.com', password='password')
    Pooja.create(temple='temple1', name='pooja1', amount=100)
    Setting.create(key='goushala', value='20')
    Setting.create(key='annadaana', value='50')
    Setting.create(key='cultural events', value='8')
    Setting.create(key='samuhika pooja', value='12')
    Setting.create(key='home video', value='https://www.youtube.com/watch?v=DdsYlKJmd_4')
    print('Data Added!')


def reset() -> None:
    """Removes any changes made to the database and resets it with test entries."""
    confirm = input('Are you sure you want to reset the database? [y/n]: ')
    if confirm == 'y':
        clear(confirm)
        create()
        add_data()
    else:
        print('command aborted')


def backup() -> None:
    try:
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        backup_file, mime = '', ''
        if 'sqlite' in db_uri:
            backup_file, mime = f'app/{db_uri.split("/")[-1]}', 'application/x-sqlite3'
        elif 'postgresql' in db_uri:
            os.system(f'pg_dump {db_uri.split("/")[-1]} > backup.sql')
            backup_file, mime = 'backup.sql', 'application/sql'

        if backup_file and mime and os.path.exists(backup_file):
            if os.path.getsize(backup_file) / 1048576 < 25:
                send_email.delay(
                    recipients=current_app.config['BACKUP_EMAILS'],
                    subject=f'{current_app.config["APPLICATION_NAME"]} - Backup ({india_time().strftime("%d/%m/%Y")})',
                    body='PFA the backup file.', attachments={backup_file: mime}
                )
            else:
                current_app.logger('Backup Failed! Backup file too large.')
        current_app.logger('Backup Failed! Incorrect database URI or backup file not found.')
    except Exception as e:
        current_app.logger.critical(f"{str(e)} \n {traceback.format_exc()}\n\n")


@click.command(name='dev')
@click.argument('command')
@with_appcontext
def dev_commands(command: str) -> None:
    """CLI to execute the specified dev command.
    :param command: The command to be executed.
    """
    commands = {'create': create, 'clear': clear, 'add_data': add_data, 'reset': reset, 'backup': backup}
    if func := commands.get(command):
        func()
    else:
        print('Invalid command.')


@click.command(name='test')
@click.argument('file', required=False)
@with_appcontext
def test_command(file: str = None) -> None:
    """CLI command to run unit tests.
    :param file: The specific file from which tests must be run.
    """
    os.system('python -m pytest -W ignore::DeprecationWarning -p no:cacheprovider -s tests/' + (f'test_{file}.py' if file else ''))
