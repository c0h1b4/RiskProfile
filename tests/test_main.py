import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../service'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

user = {
    "age": 35,
    "dependents": 2,
    "house": {"ownership_status": "owned"},
    "income": 0,
    "marital_status": "married",
    "risk_questions": [0, 1, 0],
    "vehicle": {"year": 2018}
}
output = {
    "auto": "regular",
    "disability": "ineligible",
    "home": "economic",
    "life": "regular"
}


def test_calculate_user_risk_with_default_data():
    response = client.post("/api/risk/", json=user)
    assert response.status_code == 200
    assert response.json() == output

def test_force_validation_error():
    bad_user = {
        "dependents": 2,
        "house": {"ownership_status": "none"},
        "income": 0,
        "marital_status": "widow",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    bad_output = {
      "detail": [
        {
          "loc": [
            "body",
            "age"
          ],
          "msg": "field required",
          "type": "value_error.missing"
        },
        {
          "loc": [
            "body",
            "house",
            "ownership_status"
          ],
          "msg": "value is not a valid enumeration member; permitted: 'owned', 'mortgaged'",
          "type": "type_error.enum",
          "ctx": {
            "enum_values": [
              "owned",
              "mortgaged"
            ]
          }
        },
        {
          "loc": [
            "body",
            "marital_status"
          ],
          "msg": "value is not a valid enumeration member; permitted: 'single', 'married'",
          "type": "type_error.enum",
          "ctx": {
            "enum_values": [
              "single",
              "married"
            ]
          }
        }
      ]
    }
    response = client.post("/api/risk/", json=bad_user)
    assert response.status_code == 422
    assert response.json() == bad_output
