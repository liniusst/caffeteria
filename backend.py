# pylint: disable= missing-docstring
import random
from typing import Dict, List
from pymongo.errors import PyMongoError, CollectionInvalid
from database import db_session


class Restaurant:
    def __init__(self) -> None:
        self.database = db_session()
        self.reservation_collection = self.database["reservations"]
        self.tables_collection = self.database["tables"]
        self.menu_collection = self.database["menu"]
        self.collection = None

    def create_collection(self, collection_name: str) -> bool:
        try:
            self.database.create_collection(collection_name)
            return True

        except CollectionInvalid as err:
            print("Collection creation error:", str(err))
            return False

        except PyMongoError as err:
            print("An error occurred:", str(err))
            return False

    def create_tables(self, tables_qty: int):
        try:
            table_id = 1
            for _ in range(tables_qty):
                query = {
                    "table_id": table_id,
                    "table_seats": random.randint(1, 15),
                    "reserved": False,
                }
                self.tables_collection.insert_one(query)
                table_id = table_id + 1

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def create_reservation(self, client_name: str, seats_qty: int, time: str):
        try:
            query = {"table_seats": {"$gte": seats_qty}, "reserved": False}
            table = self.tables_collection.find_one(query)

            add_reservation = {
                "client_name": client_name,
                "time": time,
                "table_id": table["table_id"],
            }

            update_table = {
                "$set": {
                    "reserved": True,
                    "reserved_by": client_name,
                    "reservation_time": time,
                }
            }
            query = {"table_id": table["table_id"]}

            result = self.reservation_collection.insert_one(add_reservation)
            self.tables_collection.update_one(query, update_table)
            return str(result.inserted_id)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def create_menu_elements(self, menu_list: List[Dict]):
        try:
            for element in menu_list:
                self.menu_collection.insert_one(element)

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

    def get_all_tables(self):
        try:
            all_tables = self.tables_collection.find()
            return list(all_tables)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_category_elements(self, category_name: str):
        try:
            query = {"cat": {"$eq": category_name}}
            result = self.menu_collection.find(query)
            return result

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
