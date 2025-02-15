from app.player import *
from app.match import *
from app.team import *
from db.connection import *

def main_menu():
    while True:
        print("\n=== Round Robin ===")
        print("1. Add New Players")
        print("2. Start Match")
        print("3. Leaderboard")
        print("4. Rematch")
        print("5. Rename Player")
        print("6. Delete Player")
        print("7. Create Team")
        print("8. View Team [🛠️ WIP] ")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_players()
        elif choice == "2":
            start_match()
        elif choice == "3":
            retrieve_leaderboard()
        elif choice == "4":
            rematch()
        elif choice == "5":
            rename_player()
        elif choice == "6":
            delete_player()
        elif choice == "7":
            create_team()
        elif choice == "8":
            view_team()
        elif choice == "0":
            print("\nClosing database...")
            connector.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()