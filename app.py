# pylint: disable= missing-docstring
from backend import Restaurant
from menu_list import menu

if __name__ == "__main__":
    restaurant = Restaurant()
    # restaurant.create_collection("reservations")
    # restaurant.create_tables(tables_qty=5)
    # restaurant.create_menu_elements(menu)

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. View all table status")
        print("5. Quit")

        choice = int(input("Enter your choice (1-4): "))

        if choice == 1:
            client_reservations = restaurant.filter_client_reservations(
                reserved_by=name
            )
            for reservation in client_reservations:
                print(
                    f"Table [{reservation['table_id']}] reserved by {reservation['client_name']} at {reservation['time']}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            time = input("What time would you like to reserve? Enter time in HH:MM ")
            restaurant.create_reservation(name, seats, time)

        elif choice == 3:
            all_tables = restaurant.get_all_tables()
            for table in all_tables:
                print(
                    f"Table [{table['table_id']}] with {table['table_seats']} seats. Reserved status: {table['reserved']} "
                )

        elif choice == 4:
            all_menu = restaurant.get_category_elements("starters")
            for element in all_menu:
                print(f'{element["name"]}, {element["price"]}')

        elif choice == 5:
            break
