# pylint: disable= missing-docstring

reservation_validation = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "name",
                "age",
                "email",
            ],
            "properties": {
                "name": {"bsonType": "string", "description": "Name must be a string."},
                "age": {
                    "bsonType": "int",
                    "minimum": 18,
                    "maximum": 99,
                    "description": "Age must be an integer between 18 and 99.",
                },
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "description": "Email must be a valid email address.",
                },
            },
        }
    }
}
