# pylint: disable= missing-docstring
from typing import List


class Table:
    def __init__(self, table_type: str, table_id: int, table_seats: int) -> None:
        self.table_type = table_type
        self.table_id = table_id
        self.table_seats = table_seats

    def get_table_id(self) -> int:
        return self.table_id


class Menu:
    def __init__(
        self,
        menu_cat: str,
        menu_dish: str,
        menu_dish_price: float,
        menu_dish_kcal: float,
        menu_dish_qty: int,
    ) -> None:
        self.menu_cat = menu_cat
        self.menu_dish = menu_dish
        self.menu_dish_price = menu_dish_price
        self.menu_dish_kcal = menu_dish_kcal
        self.menu_dish_qty = menu_dish_qty


class Order:
    def __init__(self, order_dish: str, order_price: float, order_qty: int) -> None:
        self.order_dish = order_dish
        self.order_price = order_price
        self.order_qty = order_qty
        self.order = []


class Reservations:
    def __init__(self, reserved_by: str, table: Table, reserved_time: str) -> None:
        self.reserved_by = reserved_by
        self.table = table
        self.reserved_time = reserved_time


class Restaurant:
    tables_list = []
    reservation_list = []
    menu_list = []

    @classmethod
    def add_table(cls, table_list: Table) -> None:
        for table in table_list:
            cls.tables_list.append(table)

    @classmethod
    def add_menu_elements(cls, menu_list: Menu) -> None:
        for menu_element in menu_list:
            cls.menu_list.append(menu_element)

    def get_table_by_id(self, table_id: int) -> Table:
        for table in self.tables_list:
            if table.get_table_id() == table_id:
                return table
        return None

    @classmethod
    def get_tables_list(cls):
        return cls.tables_list

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

    def set_reservation(
        self, reserved_by: str, table_id: int, reserved_time: str
    ) -> bool:
        table_object = self.get_table_by_id(table_id)
        if table_object is None:
            return False

        for reservarion in self.reservation_list:
            if reservarion.table.get_table_id() == table_id:
                return False

        self.reservation_list.append(
            Reservations(reserved_by, table_object, reserved_time)
        )
        return True

    @classmethod
    def get_reservation_info(cls, table_obj: Table) -> Reservations:
        for reserv in cls.reservation_list:
            if reserv.table == table_obj:
                return reserv
        return None

    @classmethod
    def get_free_tables_by_seats(cls, needed_seats: int):
        free_tables = []
        for table in cls.tables_list:
            if table.table_seats >= needed_seats:
                if cls.get_reservation_info(table) is None:
                    free_tables.append(table)
        return free_tables

    def get_reservations(self) -> List[Reservations]:
        return self.reservation_list


if __name__ == "__main__":
    Restaurant.add_table(
        [
            Table("Single", table_id=1, table_seats=1),
            Table("Single", table_id=2, table_seats=2),
            Table("Double", table_id=3, table_seats=2),
            Table("Double", table_id=4, table_seats=3),
            Table("Double", table_id=5, table_seats=4),
            Table("Double", table_id=6, table_seats=5),
        ]
    )
    Restaurant.add_menu_elements(
        [
            Menu("Soups", "Agurkine", 1.99, 120, 10),
            Menu("Soups", "Kopustiene", 1.49, 900, 10),
            Menu("Karsti", "Kepsnys", 6.49, 1500, 10),
            Menu("Karsti", "Grilis", 6.49, 1500, 10),
            Menu("Uzkandziai", "Kepta duona", 6.49, 1500, 10),
        ]
    )

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View table status")
        print("4. Quit")
        print("5. Arived on time")

        choice = int(input("Enter your choice (1-4): "))
        restaurant = Restaurant()
        if choice == 1:
            for reservation in restaurant.get_reservations():
                print("Al reservations list: ")
                print(
                    f"Reserved by: {reservation.reserved_by}, time: {reservation.reserved_time}, table id: {reservation.table.get_table_id()}"
                )
        elif choice == 2:
            seats = int(input("How many people in your group? "))
            time = input("What time would you like to reserve? Enter time in HH:MM ")
            for free_table in restaurant.get_free_tables_by_seats(needed_seats=seats):
                print(
                    f"Type: {free_table.table_type}, id: {free_table.table_id}, seats: {free_table.table_seats}"
                )
            selected_table = int(input("Selected table ID: "))
            if restaurant.set_reservation(name, selected_table, time):
                print("ok")
            else:
                print("no")

        elif choice == 3:
            for rest_table in Restaurant.get_tables_list():
                info = restaurant.get_reservation_info(rest_table)
                if info is None:
                    print(
                        f"Type: {rest_table.table_type}, id: {rest_table.table_id}, seats: {rest_table.table_seats}"
                    )
                else:
                    print(
                        f"Type: {rest_table.table_type}, id: {rest_table.table_id}, seats: {rest_table.table_seats}. Reserved by: {info.reserved_by}"
                    )

        elif choice == 4:
            break

        elif choice == 5:
            print("Select your food categorie: ")

            categories = restaurant.get_menu_categories()
            for categorie in categories:
                print(categorie)

            selected_menu = input("Selected category: ")
            select = restaurant.get_menu_elements_by_category(needed_cat=selected_menu)
            for dish in select:
                print(dish.menu_dish)
            selected_dish = input("Selected dish: ")
