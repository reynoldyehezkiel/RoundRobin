from app.player import *
from app.match import *
from app.team import *
from db.connection import *

def display_menu(title, options):
    print(f"\n=== {title} ===")
    for key, value in options.items():
        print(f"{key}. {value['label']}")
    choice = input("Select an option: ").strip()
    options.get(choice, {"action": invalid_choice})["action"]()

def player_menu():
    while True:
        options = {
            "1": {"label": "Add New Players", "action": add_players},
            "2": {"label": "Rename Player", "action": rename_player},
            "3": {"label": "Delete Player", "action": delete_player},
            "4": {"label": "Leaderboard", "action": view_leaderboard},
            "0": {"label": "Back", "action": lambda: None}
        }
        display_menu("Player Menu", options)

def match_menu():
    while True:
        options = {
            "1": {"label": "Start Match", "action": start_match},
            "2": {"label": "Rematch", "action": rematch},
            "0": {"label": "Back", "action": lambda: None}
        }
        display_menu("Match Menu", options)

def team_menu():
    while True:
        options = {
            "1": {"label": "Create New Team", "action": create_team},
            "2": {"label": "Assign Player to Team", "action": assign_player_to_team},
            "3": {"label": "View Team", "action": view_team},
            "0": {"label": "Back", "action": lambda: None}
        }
        display_menu("Team Menu", options)

def exit_program():
    print("\nClosing database...")
    connector.close()
    print("Goodbye!")
    exit()

def invalid_choice():
    print("Invalid choice. Please try again.")

def main_menu():
    menu_options = {
        "1": {"label": "Player", "action": player_menu},
        "2": {"label": "Match", "action": match_menu},
        "3": {"label": "Team", "action": team_menu},
        "0": {"label": "Exit", "action": exit_program}
    }
    while True:
        display_menu("Round Robin", menu_options)

if __name__ == "__main__":
    main_menu()
