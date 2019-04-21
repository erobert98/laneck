import os
import tempfile

import pytest

from app.app import app


@pytest.fixture
def client():
    db_fd, app.app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['SQLALCHEMY_DATABASE_URI'])