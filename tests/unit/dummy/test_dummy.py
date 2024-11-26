def test_api_client(test_client):
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
