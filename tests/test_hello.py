import asyncio
import os

import example
import mock
import sqlalchemy
from example.server import DATABASE_URL, app, database, metadata, packages
from fastapi import FastAPI
from starlette.testclient import TestClient

os.environ['DATABASE_URL'] = 'sqlite:///./test.db'


loop = asyncio.get_event_loop()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.drop_all(engine)  # FIXME: do this before each test to prevent state?
metadata.create_all(engine)
client = TestClient(app)


def test_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}


def test_no_packages():
    response = client.get('/api/v1/packages')
    assert response.status_code == 200
    assert response.json() == []


def test_create_package():
    response = client.post('/api/v1/packages', data='{"name":"hello","version":"2.10"}')
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['status'] == 'created'


def test_list_packages():
    response = client.get('/api/v1/packages')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'name': 'hello', 'version': '2.10', 'status': 'created'}
    ]

def test_retrieve_package():
    response = client.get('/api/v1/package/1')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1, 'name': 'hello', 'version': '2.10', 'status': 'created'
    }


def test_download_package():
    with mock.patch.object(example.server, 'download_task', return_value=None) as task:
        response = client.post('/api/v1/package/1/download')
    assert response.status_code == 200
    assert response.json()['status'] == 'created'
    assert task.called


def test_download_package_doesnt_redownload():
    query = packages.update().where(packages.c.id == 1).values(status='downloaded')
    loop.run_until_complete(database.execute(query)) # TODO: async tests
    with mock.patch.object(example.server, 'download_task', return_value=None) as task:
        response = client.post('/api/v1/package/1/download')
    assert response.status_code == 200
    assert response.json()['status'] == 'downloaded'
    assert not task.called


def test_activate_package():
    response = client.post('/api/v1/package/1/activate')
    assert response.status_code == 200
    assert response.json() == {'status': 'activated'}


def test_activate_package_multiple_times():
    response = client.post('/api/v1/package/1/activate')
    assert response.status_code == 200
    assert response.json() == {'status': 'activated'}
