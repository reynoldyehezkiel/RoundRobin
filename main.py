from app.player import *
from app.match import *
from app.team import *
from db.connection import *

def display_menu(title, options):
    while True:  # Keep showing menu until valid input
        print(f"\n=== {title} ===")
        for key, value in options.items():
            print(f"{key}. {value['label']}")
        choice = input("Select an option: ").strip()

        if choice in options:
            return choice  # Return choice instead of executing action

        print("Invalid choice. Please try again.")

def player_menu():
    options = {
        "1": {"label": "Add New Players", "action": add_players},
        "2": {"label": "Leaderboard", "action": view_leaderboard},
        "3": {"label": "Search Players", "action": search_players},
        "4": {"label": "Rename Player", "action": rename_player},
        "5": {"label": "Delete Player", "action": delete_player},
        "0": {"label": "Back"}
    }
    while True:
        choice = display_menu("Player Menu", options)
        if choice == "0":
            break  # Exit the menu when "Back" is chosen
        options[choice]["action"]()  # Execute the chosen action

def match_menu():
    options = {
        "1": {"label": "Start Match", "action": start_match},
        "2": {"label": "Rematch", "action": rematch},
        "0": {"label": "Back"}
    }
    while True:
        choice = display_menu("Match Menu", options)
        if choice == "0":
            break
        options[choice]["action"]()

def team_menu():
    options = {
        "1": {"label": "Create New Team", "action": create_team},
        "2": {"label": "Assign Player", "action": assign_player},
        "3": {"label": "View Team", "action": view_team},
        "4": {"label": "Search Teams", "action": search_teams},
        "5": {"label": "Rename Team", "action": rename_team},
        "6": {"label": "Delete Team", "action": delete_team},
        "0": {"label": "Back"}
    }
    while True:
        choice = display_menu("Team Menu", options)
        if choice == "0":
            break
        options[choice]["action"]()

def exit_program():
    print("\nClosing database...")
    connector.close()
    print("Goodbye!")
    exit()

def main_menu():
    options = {
        "1": {"label": "Player", "action": player_menu},
        "2": {"label": "Match", "action": match_menu},
        "3": {"label": "Team", "action": team_menu},
        "0": {"label": "Exit", "action": exit_program}
    }
    while True:
        choice = display_menu("Round Robin", options)
        options[choice]["action"]()  # Execute the selected menu

if __name__ == "__main__":
    main_menu()
