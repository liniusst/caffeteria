from typing import List

class Main:
    def __init__(self, visitor_name: str) -> None:
        self.visitor_name = visitor_name
        
    def get_visitor_name(self, name: str):
        self.visitor_name = name
        return self.visitor_name
    
    def get_visitor_seats(self, seats: int):
        self.seats = seats
        return self.seats


class Table(Main):
    def get_tables(self, table_list: List[str]):
        self.table_list = table_list
        return self.table_list

    def get_table_type(self, table: List[str]):
        self.table_type = table[0]
        return self.table_type
    
    def get_table_id(self, table: List[str]):
        self.table_id = table[1]
        return self.table_id
    
    def get_table_seats(self, table: List[str]):
        self.table_seats = table[2]
        return self.table_seats
    
    def get_reserved_by(self, table: List[str]):
        self.reserved_by = table[3]
        return self.reserved_by
    
    def get_reserved_time(self, table: List[str]):
        self.reserved_time = table[4]
        return self.reserved_time
    
    
class Reservation(Table):
    def __init__(self) -> None:
        pass

    def check_reservation(self):
        for table in self.table_list:
            if self.visitor_name == self.get_reserved_by(table) and self.get_reserved_by(table) != None:
                self.get_table_id(table)
                self.get_reserved_time(table)
                print(f"You are allready reserved Table {self.table_id} at {self.reserved_time}")
            else:
                print('varyk is cia, neturi rezervacijos')
                break
    
    def get_reservated_tables(self):
        for table in self.table_list:
            if self.get_reserved_by(table) != None:
                print(f"Table {self.get_table_id(table)} [{self.get_table_type(table)} - {self.get_table_seats(table)}] ppl - reserved by {self.get_reserved_by(table)} at {self.get_reserved_time(table)}")
            else:
                print(f"Table {self.get_table_id(table)} [{self.get_table_type(table)} - {self.get_table_seats(table)}] ppl - free")

    def assign_table(self, seats: int, time: str):
        for table in self.table_list:
            if self.get_reserved_by(table) != None:
                pass
            elif self.get_table_seats(table) == seats:
                table[3] = self.visitor_name
                table[4] = time
                break
            else:
                print("sorry neturim vietos")
                break

class Restaurant:
    pass


        
                



        
tables = [
    ["Single", 1, 1, "Linas", "18:00"],
    ["Single", 2, 2, "Toma", "19:00"],
    ["Double", 3, 4, None, None],
    ["Double", 4, 4, None, None],
    ["Family", 5, 5, None, None],
    ["Family", 6, 6, None, None],
]

# test.check_reservation()
# test.get_reservated_tables()
# test.check_free_table(5)
# print(test.assign_free_table("18:00"))

visit = Reservation()

print("Welcome to our Cafeteria!")
name = input("Please enter your name: ")
visit.get_visitor_name(name)
visit.get_tables(tables)


while True:
    print("\nWhat would you like to do?")
    print("1. Check my reservation")
    print("2. Reserve a table")
    print("3. View table status")
    print("4. Quit")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        visit.check_reservation()
        

    elif choice == 2:
        seats = int(input("How many people in your group? "))
        time = input("What time would you like to reserve? Enter time in HH:MM ")
        visit.assign_table(seats, time)
        # visit.assign_free_table(time)

    elif choice == 3:
        visit.get_reservated_tables()

    elif choice == 4:
        break


