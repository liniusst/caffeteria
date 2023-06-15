# pylint: disable= missing-docstring
from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection
from modules.data import Table, Menu, Order, Reservations

client = MongoClient("mongodb://localhost:27017/")
db = client["caffeteria"]
# collection = db["your_collection_name"]


class Restaurant:
    # tables_list = []
    # reservation_list = []
    menu_list = []
    order_list = []

    # def add_table(self, table_list: Table) -> None:
    #     for table in table_list:
    #         self.tables_list.append(table)

    def add_menu_elements(self, menu_list: Menu) -> None:
        for menu_element in menu_list:
            self.menu_list.append(menu_element)

    def add_to_order(self, selected_name: str, selected_qty: float, table: int) -> None:
        for menu_element in self.menu_list:
            if selected_name == menu_element.menu_dish:
                self.order_list.append(
                    Order(
                        selected_name, menu_element.menu_dish_price, selected_qty, table
                    )
                )

    # def get_table_by_id(self, table_id: int) -> Table:
    #     for table in self.tables_list:
    #         if table.get_table_id() == table_id:
    #             return table
    #     return None

    def get_menu_list(self):
        return self.menu_list

    # def get_tables_list(self):
    #     return self.tables_list

    def get_menu_categories(self) -> List:
        categories_list = []
        for cat in self.menu_list:
            if cat.menu_cat not in categories_list:
                categories_list.append(cat.menu_cat)
        return categories_list

    def get_menu_elements_by_category(self, needed_cat: str) -> List:
        category_elements = []
        for menu_element in self.menu_list:
            if menu_element.menu_cat == needed_cat:
                category_elements.append(menu_element)
        return category_elements

    ##############

    def filter_free_tables(self, need_seats: int):
        collection = db["tables"]
        query = {"reserved_by": "", "table_seats": {"$gte": need_seats}}
        result = collection.find(query)
        return list(result)

    def filter_reservations_by_name(self, name: str):
        collection = db["reservations"]
        result = collection.find(
            {"reserved_by": name}, {"table_id": 1, "reserved_time": 1, "_id": 0}
        )
        return list(result)

    def set_reservation(self, reserved_by: str, table_id: int, reserved_time: str):
        collection = db["reservations"]
        query = {
            "table_id": table_id,
            "reserved_by": reserved_by,
            "reserved_time": reserved_time,
        }
        result = collection.insert_one(query)
        return result.inserted_id


if __name__ == "__main__":
    restaurant = Restaurant()

    # restaurant.add_menu_elements(
    #     [
    #         Menu("Soups", "Agurkine", 1.99, 120, 10),
    #         Menu("Soups", "Kopustiene", 1.49, 900, 10),
    #         Menu("Karsti", "Kepsnys", 6.49, 1500, 10),
    #         Menu("Karsti", "Grilis", 6.49, 1500, 10),
    #         Menu("Uzkandziai", "Kepta duona", 6.49, 1500, 10),
    #     ]
    # )

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. Start order")
        print("5. Get order list")
        print("6. Quit")

        choice = int(input("Enter your choice (1-4): "))

        if choice == 1:
            my_reservations = restaurant.filter_reservations_by_name(name)
            for reservation in my_reservations:
                print(
                    f"Table id: {reservation['table_id']}, time: {reservation['reserved_time']}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            time = input("What time would you like to reserve? Enter time in HH:MM ")
            free_tables = restaurant.filter_free_tables(seats)
            for table in free_tables:
                print(f"Table id: {table['table_id']}, seats: {table['table_seats']}")

        elif choice == 3:
            collection = db["tables"]
            all_tables = collection.find(
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
            print("Select your food categorie: ")

            categories = restaurant.get_menu_categories()

            for index, categorie in enumerate(categories, 1):
                print(f"{index}. {categorie}")

            selected_menu = input("Selected category: ")
            select = restaurant.get_menu_elements_by_category(needed_cat=selected_menu)

            for index, dish in enumerate(select, 1):
                print(f"{index}. {dish.menu_dish}")

            selected_dish = input("Selected dish: ")
            selected_dish_qty = input("Select qty: ")
            restaurant.add_to_order(selected_dish, selected_dish_qty, selected_table)

        elif choice == 5:
            for order in restaurant.order_list:
                print(
                    f"Table [{order.order_table}] ordered: {order.order_dish} - {order.order_qty} qty"
                )
        elif choice == 6:
            break
