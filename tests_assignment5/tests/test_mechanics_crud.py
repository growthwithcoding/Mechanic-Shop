from http import HTTPStatus

def test_mechanics_crud(client):
    # create
    r = client.post("/mechanics/", json={"full_name":"Unit Tester","email":"unit@test.local","salary_cents":5000000})
    assert r.status_code == HTTPStatus.CREATED
    me = r.get_json()
    mid = me.get("mechanic_id") or me.get("id") or 1

    # list
    r = client.get("/mechanics/")
    assert r.status_code == HTTPStatus.OK
    assert any(m["email"]=="unit@test.local" for m in r.get_json())

    # update
    r = client.put(f"/mechanics/{mid}", json={"full_name":"Unit Tester II"})
    assert r.status_code == HTTPStatus.OK
    assert r.get_json()["full_name"] == "Unit Tester II"

    # delete
    r = client.delete(f"/mechanics/{mid}")
    assert r.status_code == HTTPStatus.OK
