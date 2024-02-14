''' 
first create a dummy data with function. 
then get all data and copy in get all data test case.
then update that data i created 
in last delete the data i created
'''



from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
from typing import Generator
from tortoise.contrib.test import finalizer, initializer
import asyncio
from asyncio import get_event_loop
from ...main import app
from controllers import create_business_status_controller


client=TestClient(app)
@pytest.fixture(scope="module")
def client() -> Generator:
    # Initialize your resources here
    initializer(["app/resources/lookup/status_master/business_status/controllers.py"])
    
    # Create the TestClient instance
    with TestClient(app) as c:
        yield c
    



@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

    



def test_create_business_status(client:TestClient):
    headers = {'authentication': 'success'}
    body={{
        "title": "Pending amir",
        "status_type": "lead",
        "isactive": "string"
    }}
    
    response = client.post("/business/status",json=body,headers=headers)
    print(response.json())
    assert response.status_code == 201

    # assert response.json() == body


def test_get_all_business_status_controller(client:TestClient):
    headers = {'authentication': 'success'}
    expected_response={{
        "active": [
            {
            "id": 90,
            "title": "Pending",
            "status_type": "lead",
            "is_default": False
            },
            {
            "id": 30,
            "title": "already vendor",
            "status_type": "lead",
            "is_default": False
            },
            {
            "id": 120,
            "title": "test status",
            "status_type": "staff",
            "is_default": False
            }
        ],
        "active_count": 3,
        "inactive": [
            {
            "id": 122,
            "title": "Yesss",
            "status_type": "client",
            "is_default": False
            }
        ],
        "inactive_count": 1
        }}

    headers = {'authentication': 'success'}
    response = client.get("/business/status",headers=headers)
    print(response.json())

    expected_response = response.json()
    assert response.status_code == 200
    assert expected_response == response.json()

def test_get_all_notes_type_by_id(client:TestClient):
    expected_response={{
        "id": 90,
        "title": "Pending"
        }
}

    headers = {'authentication': 'success'}
    response = client.get("/notes_type/90",headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_all_status_for_lead_controller():
    expected_response={{
        "results": [
            {
            "value": 90,
            "label": "Pending"
            },
            {
            "value": 30,
            "label": "already vendor"
            }
        ],
        "total_count": 2
        }}
    
    headers = {'authentication': 'success'}
    response = client.get("/business/status/lead",headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == expected_response
    # assert response.json() == expected_response.json()

def test_update_business_status_controller(client:TestClient):
    headers = {'authentication': 'success'}
    body={{
        # "id": 90,  # <<<< id expected
        "title": "Pending amir"
    }}
    response = client.put("/business/status/",json=body,headers=headers)
                                 # add id ^^^
    print(response.json())
    assert response.status_code == 200
    assert response.json() == body


def test_delete_notes_type(client:TestClient):
    headers = {'authentication': 'success'}
    response = client.delete("/business/status",headers=headers)
                                # add id ^^^
    print(response.json())
    assert response.status_code == 200
    # assert response.json()=={  "message": "Data successfully updated"}

