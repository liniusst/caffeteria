# pylint: disable= missing-docstring

reservation_validation = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["reservation_id", "client_name", "time", "table_id"],
            "properties": {
                "reservation_id": {
                    "type": "string",
                    "description": "Reservation ID must be a string.",
                },
                "client_name": {
                    "type": "string",
                    "description": "Client name must be a string.",
                },
                "time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Time must be a valid date and time string.",
                },
                "table_id": {
                    "type": "string",
                    "description": "Table ID must be a string.",
                },
            },
        }
    }
}
