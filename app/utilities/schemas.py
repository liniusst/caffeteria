# pylint: disable= missing-docstring

reservation_validation = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["reservation_id", "client_name", "time", "table_id"],
            "properties": {
                "reservation_id": {"bsonType": "int"},
                "client_name": {"bsonType": "string"},
                "time": {"bsonType": "string"},
                "table_id": {"bsonType": "int"},
            },
        }
    }
}

table_validation = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["table_id", "table_seats", "reserved"],
            "properties": {
                "table_id": {"bsonType": "int"},
                "table_seats": {"bsonType": "int"},
                "reserved": {"bsonType": "bool"},
            },
        }
    }
}
