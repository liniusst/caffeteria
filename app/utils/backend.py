# pylint: disable= missing-docstring
import random
from typing import Dict, List
from pymongo.errors import PyMongoError, CollectionInvalid, OperationFailure
from utils.database import db_session


class Base:
    def __init__(self) -> None:
        self.database = db_session()
        self.collection = None

    def enable_validation_scheme(self, validation_scheme):
        try:
            self.database.command("collMod", self.collection.name, **validation_scheme)
            print("Schema validation enabled.")

        except OperationFailure as err:
            print(f"Failed to enable schema validation: {err.details['errmsg']}")

        except PyMongoError as err:
            print("An error occurred:", str(err))


class Tables:
    def __init__(self) -> None:
        self.database = db_session()
        self.collection = self.database["tables"]

    def create_tables(self, tables_qty: int):
        try:
            table_id = 1
            for _ in range(tables_qty):
                query = {
                    "table_id": table_id,
                    "table_seats": random.randint(1, 15),
                    "reserved": False,
                }
                self.collection.insert_one(query)
                table_id = table_id + 1

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_all_tables(self):
        try:
            all_tables = self.collection.find()
            return list(all_tables)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None


class Reservation:
    def __init__(self) -> None:
        self.database = db_session()
        self.collection = self.database["reservations"]
        self.tables_collection = Tables().collection

    def create_reservation(self, client_name: str, seats_qty: int, time: str):
        try:
            query = {"table_seats": {"$gte": seats_qty}, "reserved": False}
            table = self.tables_collection.find_one(query)
            reservation_id = self.collection.count_documents({}) + 1

            add_reservation = {
                "reservation_id": reservation_id,
                "client_name": client_name,
                "time": time,
                "table_id": table["table_id"],
            }

            update_table = {
                "$set": {
                    "reserved": True,
                    "reservation_id": reservation_id,
                    "reserved_by": client_name,
                    "reservation_time": time,
                }
            }
            query = {"table_id": table["table_id"]}

            result = self.collection.insert_one(add_reservation)
            self.tables_collection.update_one(query, update_table)
            return str(result.inserted_id)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_all_reservations(self):
        try:
            all_reservations = self.collection.find()
            return list(all_reservations)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def filter_client_reservations(self, reserved_by: str):
        try:
            query = {"client_name": {"$eq": reserved_by}}
            result = self.collection.find(query)
            return list(result)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None


class Menu:
    def __init__(self) -> None:
        self.database = db_session()
        self.collection = self.database["menu"]
        self.tables_collection = Tables().collection

    def create_menu_elements(self, menu_list: List[Dict]):
        try:
            for element in menu_list:
                self.collection.insert_one(element)

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_category_elements(self, category_name: str):
        try:
            query = {"cat": {"$eq": category_name}}
            result = self.collection.find(query)
            return result

        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None


class Restaurant(Base):
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

    # def add_to_order(self, reservation_id: int, food_name: str, qty: int):
    #     try:
    #         query =

    #     except CollectionInvalid as err:
    #         print("Collection creation error:", str(err))

    #     except PyMongoError as err:
    #         print("An error occurred:", str(err))
