def test_get_all_post(auhtorized_client):
    res = auhtorized_client.get("/posts")
    print(res.json())
    assert res.status_code == 200
