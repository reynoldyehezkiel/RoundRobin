from app.player import *
from app.match import *
from query.connection import *

def main_menu():
    while True:
        print("\n=== Round Robin ===")
        print("1. Add New Players")
        print("2. Start Match")
        print("3. Leaderboard")
        print("4. Rematch")
        print("5. Delete Player")
        print("6. Rename Player (WIP)")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_players()
            generate_matches()
        elif choice == "2":
            start_match()
        elif choice == "3":
            retrieve_leaderboard()
        elif choice == "4":
            rematch()
        elif choice == "5":
            delete_player()
        elif choice == "6":
            rename_player()
            print("\n⚠️ This feature is under development!")
        elif choice == "0":
            print("\nClosing database...")
            connector.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()