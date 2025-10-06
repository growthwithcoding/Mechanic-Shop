#!/usr/bin/env python3
"""
run.py - Postman Collection Generator for Mechanic Shop API
Generates a complete Postman collection with tests for all endpoints up to Assignment 5
"""
import json
from datetime import datetime

def create_postman_collection():
    """Generate a comprehensive Postman collection with tests"""
    
    collection = {
        "info": {
            "name": "Mechanic Shop API - Assignment 5",
            "description": "Complete API collection for the Mechanic Shop application with CRUD operations for mechanics and service ticket management",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "_postman_id": "mechanic-shop-api-v5",
            "version": "5.0.0"
        },
        "item": [],
        "variable": [
            {
                "key": "base_url",
                "value": "http://127.0.0.1:5000",
                "type": "string"
            },
            {
                "key": "mechanic_id",
                "value": "1",
                "type": "string"
            },
            {
                "key": "ticket_id",
                "value": "1",
                "type": "string"
            }
        ]
    }
    
    # 1. Health Check Endpoint
    health_folder = {
        "name": "Health Check",
        "item": [
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/health",
                        "host": ["{{base_url}}"],
                        "path": ["health"]
                    },
                    "description": "Check if the API is running"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response has status field', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('status');",
                                "    pm.expect(jsonData.status).to.eql('ok');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            }
        ]
    }
    
    # 2. Mechanics CRUD Operations
    mechanics_folder = {
        "name": "Mechanics CRUD",
        "item": [
            {
                "name": "Create Mechanic",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "full_name": "John Smith",
                            "email": "john.smith@mechanicshop.com",
                            "phone": "555-0123",
                            "address": "123 Main St, Anytown, USA",
                            "salary_cents": 6500000,
                            "is_active": True
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/mechanics",
                        "host": ["{{base_url}}"],
                        "path": ["mechanics"]
                    },
                    "description": "Create a new mechanic"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 201', function () {",
                                "    pm.response.to.have.status(201);",
                                "});",
                                "",
                                "pm.test('Response has mechanic_id', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('mechanic_id');",
                                "    pm.collectionVariables.set('mechanic_id', jsonData.mechanic_id);",
                                "});",
                                "",
                                "pm.test('Mechanic data is correct', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData.full_name).to.eql('John Smith');",
                                "    pm.expect(jsonData.email).to.eql('john.smith@mechanicshop.com');",
                                "    pm.expect(jsonData.is_active).to.be.true;",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "List All Mechanics",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/mechanics",
                        "host": ["{{base_url}}"],
                        "path": ["mechanics"]
                    },
                    "description": "Retrieve all mechanics"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response is an array', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.be.an('array');",
                                "});",
                                "",
                                "pm.test('Array contains mechanic objects', function () {",
                                "    var jsonData = pm.response.json();",
                                "    if (jsonData.length > 0) {",
                                "        pm.expect(jsonData[0]).to.have.property('mechanic_id');",
                                "        pm.expect(jsonData[0]).to.have.property('full_name');",
                                "        pm.expect(jsonData[0]).to.have.property('email');",
                                "    }",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "Get Mechanic by ID",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/mechanics/{{mechanic_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["mechanics", "{{mechanic_id}}"]
                    },
                    "description": "Retrieve a specific mechanic by ID"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response has mechanic data', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('mechanic_id');",
                                "    pm.expect(jsonData).to.have.property('full_name');",
                                "    pm.expect(jsonData).to.have.property('email');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "Update Mechanic",
                "request": {
                    "method": "PUT",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "full_name": "John Smith Sr.",
                            "phone": "555-9999",
                            "salary_cents": 7000000
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/mechanics/{{mechanic_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["mechanics", "{{mechanic_id}}"]
                    },
                    "description": "Update an existing mechanic"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Mechanic data is updated', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData.full_name).to.eql('John Smith Sr.');",
                                "    pm.expect(jsonData.phone).to.eql('555-9999');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "Delete Mechanic",
                "request": {
                    "method": "DELETE",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/mechanics/{{mechanic_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["mechanics", "{{mechanic_id}}"]
                    },
                    "description": "Delete a mechanic by ID"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response confirms deletion', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('message');",
                                "    pm.expect(jsonData.message).to.include('deleted');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            }
        ]
    }
    
    # 3. Service Tickets Operations
    tickets_folder = {
        "name": "Service Tickets",
        "item": [
            {
                "name": "Create Service Ticket",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "vehicle_id": 1,
                            "customer_id": 1,
                            "status": "OPEN",
                            "problem_description": "Engine making strange noise",
                            "odometer_miles": 50000,
                            "priority": 3
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/service-tickets",
                        "host": ["{{base_url}}"],
                        "path": ["service-tickets"]
                    },
                    "description": "Create a new service ticket"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 201', function () {",
                                "    pm.response.to.have.status(201);",
                                "});",
                                "",
                                "pm.test('Response has ticket_id', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('ticket_id');",
                                "    pm.collectionVariables.set('ticket_id', jsonData.ticket_id);",
                                "});",
                                "",
                                "pm.test('Ticket data is correct', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData.status).to.eql('OPEN');",
                                "    pm.expect(jsonData.priority).to.eql(3);",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "List All Service Tickets",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/service-tickets",
                        "host": ["{{base_url}}"],
                        "path": ["service-tickets"]
                    },
                    "description": "Retrieve all service tickets"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response is an array', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.be.an('array');",
                                "});",
                                "",
                                "pm.test('Array contains ticket objects', function () {",
                                "    var jsonData = pm.response.json();",
                                "    if (jsonData.length > 0) {",
                                "        pm.expect(jsonData[0]).to.have.property('ticket_id');",
                                "        pm.expect(jsonData[0]).to.have.property('status');",
                                "        pm.expect(jsonData[0]).to.have.property('vehicle_id');",
                                "    }",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "Assign Mechanic to Ticket",
                "request": {
                    "method": "PUT",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/service-tickets/{{ticket_id}}/assign-mechanic/{{mechanic_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["service-tickets", "{{ticket_id}}", "assign-mechanic", "{{mechanic_id}}"]
                    },
                    "description": "Assign a mechanic to work on a service ticket"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response confirms assignment', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('message');",
                                "    pm.expect(jsonData.message).to.include('assigned');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            },
            {
                "name": "Remove Mechanic from Ticket",
                "request": {
                    "method": "PUT",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/service-tickets/{{ticket_id}}/remove-mechanic/{{mechanic_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["service-tickets", "{{ticket_id}}", "remove-mechanic", "{{mechanic_id}}"]
                    },
                    "description": "Remove a mechanic from a service ticket"
                },
                "response": [],
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('Status code is 200', function () {",
                                "    pm.response.to.have.status(200);",
                                "});",
                                "",
                                "pm.test('Response confirms removal', function () {",
                                "    var jsonData = pm.response.json();",
                                "    pm.expect(jsonData).to.have.property('message');",
                                "    pm.expect(jsonData.message).to.include('removed');",
                                "});"
                            ],
                            "type": "text/javascript"
                        }
                    }
                ]
            }
        ]
    }
    
    # Add all folders to collection
    collection["item"].append(health_folder)
    collection["item"].append(mechanics_folder)
    collection["item"].append(tickets_folder)
    
    return collection


def main():
    """Generate and save the Postman collection"""
    print("🔧 Mechanic Shop API - Postman Collection Generator")
    print("=" * 60)
    
    collection = create_postman_collection()
    
    filename = "Mechanic_Shop_API_Collection.postman_collection.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Postman collection created: {filename}")
    print(f"📦 Collection Name: {collection['info']['name']}")
    print(f"📝 Version: {collection['info']['version']}")
    print(f"🔢 Total Endpoints: {sum(len(folder['item']) for folder in collection['item'])}")
    print("\n📋 Endpoints Included:")
    
    for folder in collection["item"]:
        print(f"\n  📁 {folder['name']}:")
        for item in folder["item"]:
            method = item["request"]["method"]
            print(f"    • [{method:6s}] {item['name']}")
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("  1. Import the collection into Postman")
    print("  2. Start your Flask server: python app_factory_runner.py")
    print("  3. Run the collection to test all endpoints")
    print("  4. Each request includes automated tests!")
    print("\n💡 Tips:")
    print("  • Collection variables are set automatically")
    print("  • mechanic_id and ticket_id are captured from responses")
    print("  • Run requests in order for best results")
    print("=" * 60)


if __name__ == "__main__":
    main()
