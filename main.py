from app import player
from app import match

def main_menu():
    while True:
        print("\n=== Round Robin ===")
        print("1. Add New Players")
        print("2. Start Match")
        print("3. Leaderboard")
        print("4. Rematch")
        print("5. Delete Player")
        print("6. Rename Player (Coming Soon)")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            player.add_players()
            match.generate_matches()
        elif choice == "2":
            match.start_match()
        elif choice == "3":
            player.retrieve_leaderboard()
        elif choice == "4":
            match.rematch()
        elif choice == "5":
            player.delete_player()
        elif choice == "6":
            # player.rename_player()
            print("⚠️ This feature is unavailable for now. Coming Soon!")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()