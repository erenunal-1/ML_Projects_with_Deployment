import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture
def valid_input_data():
    return {
       "Person_ID": 1,
       "Gender": "Male",
       "Age": 27,
       "Occupation": "Software Engineer",
       "Sleep_Duration": 6.1,
       "Quality_of_Sleep": 6,
       "Physical_Activity_Level": 42,
       "Stress_Level": 6,
       "BMI_Category": "Overweight",
       "Blood_Pressure": "126/83",
       "Heart_Rate": 77,
       "Daily_Steps": 4200
    }

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ML Model API!"}

def test_predict(client, valid_input_data):
    response = client.post("/predict", json=valid_input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_invalid_input(client):
    invalid_data = {}  # Provide invalid data for testing
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
