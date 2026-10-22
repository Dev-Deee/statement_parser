from fastapi.testclient import TestClient
from statement_parser.main import app

client = TestClient(app)

def test_health_report_database_and_redis_up():
    response = client.get("health")
    assert response.status_code == 200
    assert response.json() == {
        "database": "up",
        "redis": "up"
    }