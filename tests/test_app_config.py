import os
import tempfile

import pytest

import mini_shopping


@pytest.fixture
def client():
    db_fd, mini_shopping.app.config['DATABASE'] = tempfile.mkstemp()
    mini_shopping.app.config['TESTING'] = True
    client = mini_shopping.app.test_client()

    with mini_shopping.app.app_context():
        mini_shopping.init_db()

    yield client

    os.close(db_fd)
    os.unlink(mini_shopping.app.config['DATABASE'])