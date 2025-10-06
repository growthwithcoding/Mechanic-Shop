from http import HTTPStatus

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == HTTPStatus.OK
    assert rv.get_json()["status"] == "ok"

def test_customers_crud_flow(client):
    # 1) Empty list
    rv = client.get("/customers")
    assert rv.status_code == HTTPStatus.OK
    assert rv.get_json() == []

    # 2) Create
    payload = {
        "first_name": "Avery",
        "last_name": "Shah",
        "email": "avery@example.com",
        "phone": "555-111-2222",
        "city": "Chicago"
    }
    rv = client.post("/customers", json=payload)
    assert rv.status_code == HTTPStatus.CREATED
    created = rv.get_json()
    cid = created["customer_id"]
    assert created["email"] == payload["email"]

    # 3) List -> shows our one customer
    rv = client.get("/customers")
    assert rv.status_code == HTTPStatus.OK
    data = rv.get_json()
    assert len(data) == 1 and data[0]["customer_id"] == cid

    # 4) Get single
    rv = client.get(f"/customers/{cid}")
    assert rv.status_code == HTTPStatus.OK
    assert rv.get_json()["first_name"] == "Avery"

    # 5) Update
    rv = client.put(f"/customers/{cid}", json={
        "first_name": "Avery",
        "last_name": "Shah",
        "email": "avery@example.com",
        "phone": "555-333-4444",
        "city": "Evanston"
    })
    assert rv.status_code == HTTPStatus.OK
    assert rv.get_json()["phone"] == "555-333-4444"

    # 6) Duplicate email rejected
    rv = client.post("/customers", json={
        "first_name": "Jordan",
        "last_name": "Lee",
        "email": "avery@example.com"  # duplicate
    })
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert "Email already associated" in rv.get_json()["error"]

    # 7) Delete
    rv = client.delete(f"/customers/{cid}")
    assert rv.status_code == HTTPStatus.OK

    # 8) Not found after delete
    rv = client.get(f"/customers/{cid}")
    assert rv.status_code == HTTPStatus.NOT_FOUND
