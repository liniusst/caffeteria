# pylint: disable= missing-docstring
from typing import List


class Table:
    def __init__(self, table_type: str, table_id: int, table_seats: int) -> None:
        self.table_type = table_type
        self.table_id = table_id
        self.table_seats = table_seats
        self.is_occupied = False

    # nurodom kokia state variablas
    def set_table_state(self, is_occupied: bool) -> None:
        self.is_occupied = is_occupied

    # gaunam state busena, po default uzdeta False. Pasikeisti turi pateikus rezervacija
    def get_table_state(self) -> bool:
        return self.is_occupied

    # gaunam table id, naudosiu kai inicializuosiu staliuku lista
    def get_table_id(self) -> int:
        return self.table_id


class Reservations:
    def __init__(self, reserved_by: str, table: Table, reserved_time: str) -> None:
        self.reserved_by = reserved_by
        self.table = table
        self.reserved_time = reserved_time


class Restaurant:
    def __init__(self) -> None:
        self.tables_list = []
        self.reservation_list = []

    # pasileidus restoranui,importuojam staliukus
    def add_table(self, table: Table) -> None:
        self.tables_list.append(table)

    # ieskomas table pagal savo id is self.tables_list
    def get_table_by_id(self, table_id: int) -> Table:
        for table in self.tables_list:
            if table.get_table_id() == table_id:
                return table
        return None

    def get_tables_list(self):
        return self.tables_list

    # setinam rezervacija
    def set_reservation(
        self, reserved_by: str, table_id: int, reserved_time: str
    ) -> bool:
        table_obj = self.get_table_by_id(table_id)
        if table_obj is None:
            return False

        for reservarion in self.reservation_list:
            if reservarion.table.get_table_id() == table_id:
                return False

        self.reservation_list.append(
            Reservations(reserved_by, table_obj, reserved_time)
        )
        return True

    def get_reservations(self) -> List[Reservations]:
        return self.reservation_list


restaurant = Restaurant()
restaurant.add_table(Table("Single", table_id=1, table_seats=1))
restaurant.add_table(Table("Double", table_id=2, table_seats=2))

# print(restaurant.get_table_by_id(1).get_table_state())

if restaurant.set_reservation("Marius", 1, "18:20"):
    print("ok")
else:
    print("no")
if restaurant.set_reservation("Linas", 1, "18:20"):
    print("ok")
else:
    print("no")


print("Al reservations list: ")
for reservation in restaurant.get_reservations():
    print(
        f"Reserved by: {reservation.reserved_by}, time: {reservation.reserved_time}, table id: {reservation.table.get_table_id()}"
    )
