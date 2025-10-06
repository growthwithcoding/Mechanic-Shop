from http import HTTPStatus
from .conftest import seed_basic_customer_vehicle

def test_service_tickets_flow(client):
    # Ensure a customer + vehicle exist
    seed_basic_customer_vehicle()

    # Create a mechanic to assign
    mr = client.post("/mechanics/", json={"full_name":"Flow Mech","email":"flow@shop.local"})
    assert mr.status_code == HTTPStatus.CREATED
    mech_id = mr.get_json().get("mechanic_id", 1)

    # Create ticket (customer_id=1, vehicle_id=1 from seed)
    tr = client.post("/service-tickets/", json={
        "vehicle_id": 1,
        "customer_id": 1,
        "status": "OPEN",
        "problem_description": "Noise test",
        "priority": 2
    })
    assert tr.status_code == HTTPStatus.CREATED
    ticket_id = tr.get_json().get("ticket_id", 1)

    # Assign mechanic
    ar = client.put(f"/service-tickets/{ticket_id}/assign-mechanic/{mech_id}")
    assert ar.status_code == HTTPStatus.OK

    # List tickets
    lr = client.get("/service-tickets/")
    assert lr.status_code == HTTPStatus.OK
    assert isinstance(lr.get_json(), list)

    # Remove mechanic
    rr = client.put(f"/service-tickets/{ticket_id}/remove-mechanic/{mech_id}")
    assert rr.status_code == HTTPStatus.OK
