# pylint: disable= missing-docstring
from backend import Restaurant, Reservation, Tables, Menu
from menu_list import menu

if __name__ == "__main__":
    restaurant = Restaurant()
    reservation_class = Reservation()
    table_class = Tables()
    menu_class = Menu()
    # restaurant.create_collection("orders")
    # restaurant.create_tables(tables_qty=5)
    # restaurant.create_menu_elements(menu)

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. Order food")
        print("5. Quit")

        choice = int(input("Enter your choice (1-4): "))

        if choice == 1:
            client_reservations = reservation_class.filter_client_reservations(
                reserved_by=name
            )
            for reservation in client_reservations:
                print(
                    f"Table [{reservation['table_id']}] reserved by {reservation['client_name']} at {reservation['time']}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            time = input("What time would you like to reserve? Enter time in HH:MM ")
            reservation_class.create_reservation(name, seats, time)

        elif choice == 3:
            all_tables = table_class.get_all_tables()
            for table in all_tables:
                print(
                    f"Table [{table['table_id']}] with {table['table_seats']} seats. Reserved status: {table['reserved']} "
                )

        elif choice == 4:
            while True:
                print("\nSelect category")
                print("1. Select reservation")
                print("2. Starter")
                print("3. Main_course")
                print("4. Desserts")
                print("5. Order")
                inside_choice = int(input("Enter your choice (1-3): "))
                if inside_choice == 1:
                    client_reservations = reservation_class.filter_client_reservations(
                        reserved_by=name
                    )
                    for reservation in client_reservations:
                        print(
                            f"Reservation ID [{reservation['reservation_id']}], time {reservation['time']}"
                        )
                    reservation_submit = int(input("Reservation ID: "))

                elif inside_choice == 2:
                    all_menu = menu_class.get_category_elements("starters")
                    for element in all_menu:
                        print(f'{element["name"]}, {element["price"]}')
                elif inside_choice == 3:
                    all_menu = menu_class.get_category_elements("main_course")
                    for element in all_menu:
                        print(f'{element["name"]}, {element["price"]}')
                elif inside_choice == 4:
                    all_menu = menu_class.get_category_elements("desserts")
                    for element in all_menu:
                        print(f'{element["name"]}, {element["price"]}')
                elif inside_choice == 1:
                    break

            all_menu = menu_class.get_category_elements("starters")
            for element in all_menu:
                print(f'{element["name"]}, {element["price"]}')

        elif choice == 5:
            break
