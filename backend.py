# pylint: disable= missing-docstring
from pymongo import MongoClient
from pymongo.errors import (
    OperationFailure,
    PyMongoError,
    CollectionInvalid,
    ConnectionFailure,
)
from typing import Dict
import random


class Restaurant:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)
        self.database = self.client[db_name]
        self.reservation_collection = self.database["reservations"]
        self.tables_collection = self.database["tables"]
        self.collection = None

    def create_tables(self, tables_qty: int):
        try:
            table_id = 1
            for _ in range(tables_qty):
                query = {
                    "table_id": table_id,
                    "table_seats": random.randint(1, 15),
                    "reserved_by": False,
                }
                self.tables_collection.insert_one(query)
                table_id = table_id + 1

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def create_reservation(self, client_name: str, seats_qty: int, time: str):
        try:
            query = {"table_seats": {"$gte": seats_qty}, "reserved_by": False}
            table = self.tables_collection.find_one(query)

            add_reservation = {
                "client_name": client_name,
                "time": time,
                "table_id": table["table_id"],
            }

            update_table = {"$set": {"reserved_by": True}}
            query = {"table_id": table["table_id"]}

            result = self.reservation_collection.insert_one(add_reservation)
            self.tables_collection.update_one(query, update_table)
            return str(result.inserted_id)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_all_reservations(self):
        try:
            all_reservations = self.reservation_collection.find()
            return list(all_reservations)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def filter_client_reservations(self, reserved_by: str):
        try:
            query = {"client_name": {"$eq": reserved_by}}
            result = self.reservation_collection.find(query)
            return list(result)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None


if __name__ == "__main__":
    restaurant = Restaurant("localhost", 27017, "caffee")
    # restaurant.create_collection("reservations")
    # restaurant.create_tables(tables_qty=5)

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. Quit")

        choice = int(input("Enter your choice (1-4): "))

        if choice == 1:
            client_reservations = restaurant.filter_client_reservations(
                reserved_by=name
            )
            for reservation in client_reservations:
                print(
                    f"Table id: {reservation['table_id']}, time: {reservation['client_name']}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            time = input("What time would you like to reserve? Enter time in HH:MM ")
            restaurant.create_reservation(name, seats, time)

        elif choice == 3:
            all_tables = restaurant.tables_collection.find(
                {}, {"table_id": 1, "table_seats": 1, "reserved_by": 1}
            )
            for table in all_tables:
                if table["reserved_by"] is not "":
                    print(
                        f"Table ID: {table['table_id']} with {table['table_seats']} seats. Reserved by: {table['reserved_by']}"
                    )
                else:
                    print(
                        f"Table ID: {table['table_id']} with {table['table_seats']} seats."
                    )

        elif choice == 4:
            break
