# services/socamas/manage.py

import pytest
from flask.cli import FlaskGroup

from project import create_app
from project.api.models import db


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('test')
def test():
    """Runs the tests."""
    # pytest.main(["-s", "project/tests/func/test_users.py::TestUser::test_update_with_invalid_params"])
    # pytest.main(["-s", "project/tests"])
    pytest.main(["-s", "project/tests"])


if __name__ == '__main__':
    cli()
